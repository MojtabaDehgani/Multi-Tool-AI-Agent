import os
import json
import datetime
from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
client = OpenAI(base_url="https://ai-gateway.mohaymen.ir/v1")

base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "bge-small-en-v1.5")

embeddings = HuggingFaceEmbeddings(
    model_name=model_path,
    model_kwargs={"device": "cpu"},
)
faiss_db_path = os.path.join(base_dir, "faiss_index")

vector_db = FAISS.load_local(
    faiss_db_path, 
    embeddings, 
    allow_dangerous_deserialization=True
)

def search_faq(query):
    retrieved_docs_with_scores = vector_db.similarity_search_with_score(query, k=3)
    DISTANCE_THRESHOLD = 1.7 
    valid_docs = []
    print("\n🔍 [RAG Debug] Checking database for:", query)
    
    for doc, score in retrieved_docs_with_scores:
        print(f"   -> Doc Score: {score:.3f}") 
        if score <= DISTANCE_THRESHOLD:
            valid_docs.append(f"- {doc.page_content}")
            
    if valid_docs:
        context = "\n".join(valid_docs)
        return context
    else:
        return "No relevant information found in the FAQ database for this query."

def calculator(operation, a, b):
    if operation == 'add': return str(a + b)
    elif operation == 'subtract': return str(a - b)
    elif operation == 'multiply': return str(a * b)
    elif operation == 'divide': 
        return str(a / b) if b != 0 else "Error: Division by zero"
    return "Invalid operation"

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_faq",
            "description": "ALWAYS use this tool FIRST for ANY question related to MBA, exams, preparation, universities, rules, or FAQs. You MUST check the database before answering. Evaluate if the retrieved context answers the query. If yes, answer conversationally using ONLY these facts. If no, say you don't know.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search keyword or query"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Used to perform basic mathematical operations (add, subtract, multiply, divide) on two numbers. If the user only provides one number or the operation is unclear, do NOT guess. Ask the user for clarification.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string", 
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "Type of mathematical operation"
                    },
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"}
                },
                "required": ["operation", "a", "b"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Used to get the current date and time.",
            "parameters": {"type": "object", "properties": {}},
        },
    }
]

SYSTEM_PROMPT = """You are a smart, friendly, and helpful assistant (Agent) equipped with external tools.
Your tasks:
1. Analyze the user's request.
2. STRICT TOOL USAGE RULE: For ANY question related to MBA, university exams, study plans, conditions, or general FAQs, you MUST use the 'search_faq' tool. You are FORBIDDEN from answering these questions using your internal knowledge. 
3. CRITICAL RULE FOR FAQ: When the 'search_faq' tool returns data, FIRST evaluate if the retrieved context actually answers the user's specific question. 
   - If it DOES answer the question: Use the information provided in the tool output to give a warm, friendly, and conversational response. You MUST rely strictly on the facts from the database. Do NOT add outside information or general knowledge, just rephrase the database facts naturally.
   - If it DOES NOT answer the question (irrelevant results): Politely and warmly inform the user that you couldn't find the exact information in your database. Do NOT make up an answer.
4. If the request is ambiguous, incomplete, or lacks necessary parameters, ask the user a clarifying question.
5. Only answer directly (without tools) for basic greetings (like "Hi", "How are you").
6. CRITICAL RULE (LANGUAGE): Always reply in the exact same language as the user's CURRENT message. If the current question is in English, reply entirely in English. If it is in Persian, reply entirely in Persian. Do not mix languages."""

conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

def agent_chat(user_input):
    global conversation_history
    
    conversation_history.append({"role": "user", "content": user_input})
    
    try:
        while True:
            response = client.chat.completions.create(
                model="openai/gpt-5.5",
                messages=conversation_history,
                tools=tools,
                tool_choice="auto", 
                temperature=0
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                print("\n⚙️ [Decision Logging]:")
                
                conversation_history.append(response_message)
                
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"   => Model decided to use the tool '{function_name}'.")
                    print(f"   => Input arguments: {function_args}")
                    
                    if function_name == "search_faq":
                        function_response = search_faq(function_args.get("query"))
                    elif function_name == "calculator":
                        function_response = calculator(
                            function_args.get("operation"), 
                            function_args.get("a"), 
                            function_args.get("b")
                        )
                    elif function_name == "get_time":
                        function_response = get_time()
                    else:
                        function_response = "Tool not found."
                        
                    print(f"   => Tool output:\n{function_response}\n")
                    
                    conversation_history.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })

            else:
                final_reply = response_message.content
                
                conversation_history.append({"role": "assistant", "content": final_reply})
                return final_reply

    except Exception as e:
        return f"Error communicating with API: {e}"

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 Agent chatbot is running ... (Type 'exit' to quit)")
    print("="*60 + "\n")

    while True:
        user_text = input("You: ").strip()
        
        if not user_text:
            continue
            
        if user_text.lower() in ['exit', 'quit']:
            print("\nAgent: Goodbye! 👋")
            break
            
        reply = agent_chat(user_text)
        print(f"\nAgent: {reply}\n")
        print("-" * 60)