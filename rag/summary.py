def generate_structured_summary(llm, docs):

    # Combine all retrieved chunks into one context string
    context = "\n\n".join([doc["text"] for doc in docs])

    prompt = f"""
You are a senior AI research analyst.

Based strictly on the provided context, generate a structured academic summary.

Format exactly as:

1. Problem Statement:
2. Background / Motivation:
3. Proposed Method:
4. Experimental Setup:
5. Results:
6. Key Contributions:
7. Limitations:
8. Future Work:

Be precise and technical.
Do not invent information.
If a section is missing, write "Not specified."

Context:
{context}

Structured Summary:
"""

    response = llm.invoke(prompt)
    return response.content