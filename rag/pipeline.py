def generate_answer(llm, query, retrieved_docs):

    if not retrieved_docs:
        return "I cannot find relevant legal information in the knowledge base."

    context = "\n\n".join([doc["text"] for doc in retrieved_docs])

    prompt = f"""
You are an AI legal information assistant.

Your job is to explain **legal procedures and general legal information** clearly.

You are NOT giving legal advice, only informational guidance based on documents.

Use the context below to answer the question.

If the question asks about legal procedures (like filing FIR, consumer complaint, tenant rights),
explain the steps clearly.

Context:
{context}

Question:
{query}

Provide a clear explanation in simple steps.

At the end include this disclaimer:

⚠️ Disclaimer:
This AI provides general legal information and does not replace professional legal advice.
"""

    response = llm.invoke(prompt)

    return response.content