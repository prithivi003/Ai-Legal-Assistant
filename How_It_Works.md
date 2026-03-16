# How the AI Legal Assistant Works (Simple Explanation)

Welcome to the **AI Legal Assistant**! This document explains exactly how this project works behind the scenes, written in plain English so you don't need a computer science degree to understand it.

---

## 1. The Core Idea
Imagine you hire a brilliant legal intern (the AI) who is very smart but hasn't memorized the entire Indian legal code. 

To make sure this intern gives you accurate answers instead of guessing, you give them two tools:
1. **A Filing Cabinet** full of verified, stamped legal PDF documents.
2. **A Computer** with internet access.

When you ask the intern a question, you instruct them to *always check the filing cabinet first*. If the answer isn't in the filing cabinet, they are allowed to use the computer to search the internet. 

This is exactly how this application works!

---

## 2. The "Filing Cabinet" (RAG System)
In the tech world, the "filing cabinet" is called **RAG** (Retrieval-Augmented Generation).

Here is how it works:
- We took a bunch of thick legal PDFs and fed them into the system.
- The system chopped those PDFs into tiny paragraphs and stored them in a highly-organized digital filing cabinet called **Pinecone** (a "Vector Database").
- When you ask a question like *"What are my rights as a tenant?"*, the system rapidly scans the Pinecone cabinet and pulls out the exact paragraphs that mention tenant rights.
- It hands those paragraphs to the AI "brain" (called **Groq/Llama 3**) and says: *"Read these paragraphs, summarize them, and answer the user's question."*

Because the AI is reading directly from your trusted PDFs, it doesn't hallucinate or make things up.

---

## 3. The "Internet Computer" (MCP Fallback System)
Sometimes, you might ask a question that *isn't* in the PDFs you uploaded. For example, a question about a law that was passed yesterday, or a random topic not covered in the documents.

This is where the **MCP** (Model Context Protocol) comes in. Think of MCP as a USB cable that plugs real-world tools into the AI's brain.

In this project, you created `mcp_legal_server.py`. This file acts as an intelligent "Internet Search tool" powered by DuckDuckGo.

Here is the flow:
1. You ask a question.
2. The AI checks the Pinecone filing cabinet (RAG).
3. The AI realizes: *"Uh oh, the answer isn't in these documents."* It throws a special flag (`NOT_IN_RAG`).
4. Your application sees this flag, pauses, and says: *"Okay, let's use the MCP Internet Tool."*
5. The application fires up `mcp_legal_server.py`, searches DuckDuckGo for your question, and grabs the top 3 live internet results.
6. It hands those live internet results back to the AI brain and says: *"Okay, the filing cabinet failed, but here is what the live internet says. Answer the user based on this."*

---

## 4. The Final Result (Streamlit UI)
The user interface you see on your screen is built using **Streamlit**. 

Streamlit is the front desk where you interact with the intern. It's the sleek, dark-themed webpage where you type your questions. 

Streamlit handles the logic of deciding whether to show you a greeting ("Hello!"), an answer from the Pinecone filing cabinet, or an answer fetched from the live internet via the MCP tool. It also explicitly shows you its "Sources" at the bottom of every answer, so you always know exactly where the information came from.

### Summary of the Flow:
**You Ask → Intent Check (is it a greeting?) → Pinecone Database Search → (If missing) → MCP Internet Search → AI Summarizes Results → Streamlit Displays Answer and Sources.**
