from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_vector_store(chunks, save_path):

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(save_path)

    return vectorstore


def embed_text(text):
    return embeddings.embed_query(text)