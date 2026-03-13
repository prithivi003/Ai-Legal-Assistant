import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Connect to index
index = pc.Index(PINECONE_INDEX_NAME)


def upsert_embedding(doc_id, embedding, text, source=None, page=None, namespace="legal_kb"):

    metadata = {
        "text": text
    }

    if source is not None:
        metadata["source"] = str(source)

    if page is not None:
        metadata["page"] = int(page)

    index.upsert(
        vectors=[
            {
                "id": doc_id,
                "values": embedding,
                "metadata": metadata
            }
        ],
        namespace=namespace
    )


def clear_namespace(namespace):

    try:
        index.delete(
            delete_all=True,
            namespace=namespace
        )
    except Exception:
        # namespace does not exist yet
        pass