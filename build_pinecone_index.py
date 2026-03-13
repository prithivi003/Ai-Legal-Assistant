import os
import re
from rag.loader import load_pdfs_from_folder
from rag.chunker import chunk_documents
from rag.embedder import embed_text
from services.vector_service import upsert_embedding

DATA_PATH = "data/legal_documents"


# -----------------------------
# Clean text before embedding
# -----------------------------
def clean_text(text):

    # remove emails
    text = re.sub(r'\S+@\S+', '', text)

    # remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # remove common website headers / login text
    text = re.sub(r'LAWYERSCLUBINDIA.*', '', text)
    text = re.sub(r'Sign in.*', '', text)
    text = re.sub(r'Google.*', '', text)

    # remove non-ASCII / strange unicode characters
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def build_index():

    print("Loading legal documents...")

    docs = load_pdfs_from_folder(DATA_PATH)

    print("Chunking documents...")

    chunks = chunk_documents(docs)

    print(f"Total chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks):

        # convert to string
        text = str(chunk.page_content)

        # ⭐ clean text before embedding
        text = clean_text(text)

        # skip small or noisy chunks
        if len(text) < 40:
            continue

        # skip login / UI noise chunks
        if any(word in text.lower() for word in ["sign in", "login", "subscribe"]):
            continue

        try:

            embedding = embed_text(text)

            doc_id = f"legal_doc_{i}"

            upsert_embedding(
                doc_id,
                embedding,
                text,
                namespace="legal_kb"
            )

            print(f"Indexed chunk {i}")

        except Exception as e:
            print(f"Skipping chunk {i} due to error: {e}")

    print("Indexing complete!")


if __name__ == "__main__":
    build_index()