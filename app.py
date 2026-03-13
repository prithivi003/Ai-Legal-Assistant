import streamlit as st
import os
import shutil

from rag.loader import load_pdfs_from_folder
from rag.chunker import chunk_documents
from rag.embedder import embed_text
from rag.retriever import retrieve_documents
from rag.llm import get_llm
from rag.pipeline import generate_answer
from rag.summary import generate_structured_summary
from rag.contribution import extract_contributions
from utils.intent_filter import detect_intent

from services.vector_service import upsert_embedding, clear_namespace


st.set_page_config(page_title="Legal AI Assistant", layout="wide")

# -----------------------------
# Sidebar Navigation
# -----------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Legal AI Assistant", "Document Analyzer"]
)

# =========================================================
# ⚖️ LEGAL AI ASSISTANT
# =========================================================

if page == "Legal AI Assistant":

    st.title("⚖️ Legal AI Assistant")

    query = st.text_input("Ask a legal question")

    if query:

        intent = detect_intent(query)

        # Greeting
        if intent == "greeting":
            st.write(
                "Hello! 👋 You can ask questions about legal procedures such as filing complaints, tenant rights, employment disputes, or consumer complaints."
            )
            st.stop()

        # Retrieve from legal knowledge base
        docs = retrieve_documents(query, namespace="legal_kb")

        if not docs:
            st.warning("No relevant legal information found.")
        else:

            llm = get_llm()
            answer = generate_answer(llm, query, docs)

            st.subheader("Answer")
            st.write(answer)

            # Sources
            with st.expander("🔎 See Sources Used to Generate Answer"):

                for doc in docs:

                    source = doc.get("source", "Unknown document")
                    page_num = doc.get("page")

                    if page_num:
                        st.markdown(f"**Source:** {source} (Page {page_num})")
                    else:
                        st.markdown(f"**Source:** {source}")

                    st.write(doc["text"])
                    st.divider()


# =========================================================
# 📄 DOCUMENT ANALYZER
# =========================================================

elif page == "Document Analyzer":

    st.title("📄 Legal Document Analyzer")

    uploaded_file = st.file_uploader(
        "Upload a legal document (PDF)",
        type="pdf"
    )

    # ==============================
    # One-time indexing (runs only on first upload)
    # ==============================

    if uploaded_file and "doc_indexed" not in st.session_state:

        # Clear previous uploads
        if os.path.exists("data/session_uploads"):
            shutil.rmtree("data/session_uploads")

        os.makedirs("data/session_uploads", exist_ok=True)

        file_path = os.path.join("data/session_uploads", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded successfully!")

        # Clear Pinecone namespace
        clear_namespace("session_docs")

        # Load & chunk document
        docs = load_pdfs_from_folder("data/session_uploads")
        chunks = chunk_documents(docs)

        st.success("Document processed!")

        # Index chunks
        for i, chunk in enumerate(chunks):

            text = str(chunk.page_content)

            if len(text.strip()) < 40:
                continue

            embedding = embed_text(text)

            doc_id = f"session_doc_{i}"

            upsert_embedding(
                doc_id,
                embedding,
                text,
                source=uploaded_file.name,
                page=chunk.metadata.get("page"),
                namespace="session_docs"
            )

        st.success("Document indexed! You can now ask questions below.")
        st.session_state.doc_indexed = True

    # ==============================
    # Q&A + Analysis (persists across Streamlit reruns)
    # ==============================

    if "doc_indexed" in st.session_state:

        # Reset button to allow re-uploading
        if st.button("🔄 Reset / Upload New Document"):
            del st.session_state["doc_indexed"]
            st.rerun()

        query = st.text_input("Ask a question about this document")

        if query:

            docs = retrieve_documents(query, namespace="session_docs")

            if not docs:
                st.warning("No relevant content found.")
            else:

                llm = get_llm()
                answer = generate_answer(llm, query, docs)

                st.subheader("Answer")
                st.write(answer)

                with st.expander("🔎 See Sources Used to Generate Answer"):

                    for doc in docs:

                        source = doc.get("source", "Uploaded document")
                        page_num = doc.get("page")

                        if page_num:
                            st.markdown(f"**Source:** {source} (Page {page_num})")
                        else:
                            st.markdown(f"**Source:** {source}")

                        st.write(doc["text"])
                        st.divider()

        # ==============================
        # Structured Summary
        # ==============================

        if st.button("Generate Structured Summary"):

            docs = retrieve_documents(
                "Summarize the entire document",
                namespace="session_docs"
            )

            if docs:

                llm = get_llm()
                summary = generate_structured_summary(llm, docs)

                st.subheader("Structured Summary")
                st.write(summary)

        # ==============================
        # Key Points
        # ==============================

        if st.button("Extract Key Points"):

            docs = retrieve_documents(
                "What are the key points of this document?",
                namespace="session_docs"
            )

            if docs:

                llm = get_llm()
                contributions = extract_contributions(llm, docs)

                st.subheader("Key Points")
                st.write(contributions)