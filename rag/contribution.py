def extract_contributions(llm, docs):

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an AI research analyst.

From the provided context, extract ONLY the key technical contributions of the paper.

Focus on:
- Novel ideas
- Architectural innovations
- Theoretical contributions
- Experimental improvements over prior work

Do NOT summarize the whole paper.
Do NOT include background.
Do NOT invent information.

Provide output in bullet points.

If contributions are unclear, write:
"Contributions not clearly specified in the paper."

Context:
{context}

Key Contributions:
"""

    response = llm.invoke(prompt)
    return response.content