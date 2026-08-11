# 🤖 Multi-Tool AI Agent

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AI Agent](https://img.shields.io/badge/AI-Agent-success)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

## 🎥 Demo
*(Here is a quick demonstration of the agent routing tools dynamically)*
<p align="center">
  <img src="demo.gif" width="700" alt="Multi-Tool AI Agent Demo">
</p>

## 🎯 Objective
To deeply understand the core concept of **Autonomous AI Agents** and **Tool Calling/Usage**.

## 📖 Task Description
Build an intelligent assistant capable of dynamically selecting and utilizing appropriate tools based on user requests.

## 🛠️ Required Tools (Capabilities)
The agent is equipped with the following functional tools:
*   **🧮 Calculator:** Performs basic arithmetic operations (Addition, Subtraction, Multiplication, Division).
*   **🔍 Text Search:** Searches through specific documents (e.g., FAQ retrieval).
*   **🕒 Time & Date (Optional):** Retrieves and displays the current system time and date.

## ⚙️ Implementation Steps
1.  **Tool Development:** Implemented each tool as an isolated, standalone function.
2.  **Schema Definition:** Defined clear input and output schemas/signatures for every tool.
3.  **Intent Recognition:** Utilized an LLM to parse the user's prompt and determine their underlying need.
4.  **Dynamic Routing:** Programmed the system to automatically select the most appropriate tool and execute it.
5.  **Synthesis:** Combined the raw tool execution results into a natural, conversational final response.

## 💡 Input Examples & Routing

| User Query | Action Taken / Routing |
| :--- | :--- |
| *"What is 5 multiplied by 12?"* | ➡️ **Uses Calculator** |
| *"What are the conditions for registration?"* | ➡️ **Uses Text Search (FAQ)** |
| *"What time is it right now?"* | ➡️ **Uses Time/Date Tool** |

## 🏆 Expected Output
A robust system capable of autonomous decision-making to determine *when* to use a tool, *which* tool to use, and how to deliver the most appropriate and accurate response to the user.

## 🚀 Advanced Features
*   **Clarification Requests:** The agent proactively asks follow-up questions if the user's prompt is ambiguous or lacks required parameters.
*   **Direct Answering:** Bypasses tool execution entirely for standard conversational queries that don't require external data.
*   **Decision Logging:** Maintains a detailed log of the agent's thought process, tool selection, and routing decisions for debugging and transparency.

---
*This project was developed as a Task for building Multi-Tool Agents.*
