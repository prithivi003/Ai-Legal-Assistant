def generate_answer(llm, query, retrieved_docs, chat_history=None):

    if not retrieved_docs:
        return "I cannot find relevant legal information in the knowledge base."

    context = "\n\n".join([doc["text"] for doc in retrieved_docs])

    # Build conversation history string for context
    # The LAST assistant response is included in full (most important for follow-ups)
    # Older messages are truncated to keep prompt size manageable
    history_text = ""
    if chat_history and len(chat_history) >= 2:
        recent = chat_history[-10:]  # Last 5 exchanges
        for i, msg in enumerate(recent):
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"]
            # Truncate older assistant responses, keep the last one in full
            is_last_assistant = (msg["role"] == "assistant" and i == len(recent) - 1)
            if msg["role"] == "assistant" and not is_last_assistant:
                content = content[:800] + "..." if len(content) > 800 else content
            history_text += f"{role}: {content}\n"

    prompt = f"""
You are an AI legal information assistant.

Your job is to explain **legal procedures and general legal information** clearly.

You are NOT giving legal advice, only informational guidance based on documents.

Use the context below to answer the question. 

CRITICAL INSTRUCTION: If the context below does NOT contain the answer to the user's question, you MUST reply EXACTLY and ONLY with the phrase: NOT_IN_RAG
Do NOT apologize, explain, or output anything else. Just output: NOT_IN_RAG

If the question asks about legal procedures (like filing FIR, consumer complaint, tenant rights),
explain the steps clearly.

{f"Previous Conversation:{chr(10)}{history_text}" if history_text else ""}
Context:
{context}

Current Question:
{query}

Provide a clear explanation in simple steps. If the user is asking a follow-up question, use the conversation history above to understand what they are referring to.

At the end include this disclaimer:

⚠️ Disclaimer:
This AI provides general legal information and does not replace professional legal advice.
"""

    response = llm.invoke(prompt)

    return response.content