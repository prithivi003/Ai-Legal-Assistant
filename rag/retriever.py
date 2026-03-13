from rag.embedder import embed_text
from services.vector_service import index


def retrieve_documents(query, namespace="legal_kb", top_k=5):

    query_embedding = embed_text(query)

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )

    print("DEBUG Pinecone results:")
    print(results)

    docs = []

    for match in results.matches:

        if match.metadata and "text" in match.metadata:

            docs.append({
                "text": match.metadata.get("text"),
                "source": match.metadata.get("source"),
                "page": match.metadata.get("page")
            })

    print("DEBUG docs returned:", len(docs))

    return docs