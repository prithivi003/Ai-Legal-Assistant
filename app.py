import streamlit as st
from rag.loader import load_pdfs_from_folder
from rag.chunker import chunk_documents
from rag.embedder import create_vector_store
from rag.retriever import load_vector_store, get_retriever
from rag.llm import get_llm
from rag.pipeline import generate_answer
from rag.summary import generate_structured_summary
from rag.contribution import extract_contributions




st.set_page_config(page_title="AI Research Intelligence Platform", layout="wide")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Home", "AI Research Chatbot", "My Paper Assistant", "Settings"]
)
if page == "AI Research Chatbot":
    st.title("🤖 Global AI Research Chatbot")

    if st.button("Build Global Knowledge Base"):
        docs = load_pdfs_from_folder("data/global_papers")
        chunks = chunk_documents(docs)
        create_vector_store(chunks, "vector_store/global_db")
        st.success("Global Knowledge Base Created!")

    query = st.text_input("Ask a research question")

    if query:
        vectorstore = load_vector_store("vector_store/global_db")
        retriever = get_retriever(vectorstore)
        docs = retriever.invoke(query)

        if not docs:
            st.warning("No relevant research content found.")
        else:
            llm = get_llm()
            answer = generate_answer(llm, query, docs)

            st.subheader("Answer")
            st.write(answer)

            st.subheader("Sources")

            unique_sources = set()

            for doc in docs:
                source_path = doc.metadata.get("source", "Unknown")
                page_label = doc.metadata.get("page_label", None)
                file_name = source_path.split("\\")[-1]
                unique_sources.add((file_name, page_label))

            for file_name, page_label in unique_sources:
                if page_label:
                    st.write(f"- {file_name} (Page {page_label})")
                else:
                    st.write(f"- {file_name}")
elif page == "My Paper Assistant":

    import os
    import shutil

    st.title("📄 My Paper Assistant")

    uploaded_file = st.file_uploader(
        "Upload a research paper (PDF)",
        type="pdf"
    )

    if uploaded_file:

        #  Step 1: Clear old uploaded files
        if os.path.exists("data/session_uploads"):
            shutil.rmtree("data/session_uploads")

        os.makedirs("data/session_uploads", exist_ok=True)

        #  Step 2: Save uploaded file
        file_path = os.path.join("data/session_uploads", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("File uploaded and saved successfully!")

        #  Step 3: Clear old session vector DB
        if os.path.exists("vector_store/session_db"):
            shutil.rmtree("vector_store/session_db")

        #  Step 4: Build new session vector store
        docs = load_pdfs_from_folder("data/session_uploads")
        chunks = chunk_documents(docs)
        create_vector_store(chunks, "vector_store/session_db")

        st.success("Session Knowledge Base Built!")

        # -------------------------------
        # 🔵 QUESTION & ANSWER SECTION
        # -------------------------------

        query = st.text_input("Ask a question about this paper")

        if query:
            vectorstore = load_vector_store("vector_store/session_db")
            retriever = get_retriever(vectorstore)
            docs = retriever.invoke(query)

            if not docs:
                st.warning("No relevant content found in this paper.")
            else:
                llm = get_llm()
                answer = generate_answer(llm, query, docs)

                st.subheader("Answer")
                st.write(answer)

        # -------------------------------
        # 🔵 STRUCTURED SUMMARY SECTION
        # -------------------------------

        if st.button("📑 Generate Structured Summary"):

            vectorstore = load_vector_store("vector_store/session_db")

            # Increase retrieval depth for summary
            retriever = vectorstore.as_retriever(search_kwargs={"k": 12})
            docs = retriever.invoke("Summarize the entire research paper")

            if not docs:
                st.warning("Unable to retrieve sufficient content for summary.")
            else:
                llm = get_llm()
                summary = generate_structured_summary(llm, docs)

                st.subheader("Structured Summary")
                st.write(summary)

        if st.button("🧠 Extract Key Contributions"):

            vectorstore = load_vector_store("vector_store/session_db")

            retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
            docs = retriever.invoke("What are the key contributions of this paper?")

            if not docs:
                st.warning("Unable to retrieve content for contribution extraction.")
            else:
                  llm = get_llm()
                  contributions = extract_contributions(llm, docs)

                  st.subheader("Key Contributions")
                  st.write(contributions)        