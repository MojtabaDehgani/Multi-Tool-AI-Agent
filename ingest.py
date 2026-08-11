import os
import json
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "faq.json")

with open(json_path, "r", encoding="utf-8") as file:
    faq_data = json.load(file)

documents = []
for item in faq_data:
    combined_text = f"Question: {item['question']}\nAnswer: {item['answer']}"
    doc = Document(page_content=combined_text)
    documents.append(doc)

print("\n***************************************************************************************")
print(f"{len(documents)} chunks were created successfully.")
print("***************************************************************************************\n")

model_path = os.path.join(base_dir, "bge-small-en-v1.5")

embeddings = HuggingFaceEmbeddings(
    model_name=model_path,
    model_kwargs={"device": "cpu"},
)

vector_db = FAISS.from_documents(documents, embeddings)

faiss_db_path = os.path.join(base_dir, "faiss_index")
vector_db.save_local(faiss_db_path)

print("\n***************************************************************************************")
print(f"Success! Vector database saved at: {faiss_db_path}")
print("***************************************************************************************\n")