import streamlit as st
from rag.retriever import retrieve_documents
from rag.llm import get_llm
from rag.pipeline import generate_answer
from utils.intent_filter import detect_intent


# =========================================================
# Page Config
# =========================================================

st.set_page_config(
    page_title="Legal AI Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# Custom CSS — Premium Dark Theme
# =========================================================

st.markdown("""
<style>
    /* ===== Google Fonts ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ===== Global ===== */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ===== Hide default Streamlit elements ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ===== Sidebar Styling ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        border-right: 1px solid rgba(100, 100, 255, 0.1);
    }

    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #c8c8e0 !important;
        font-size: 0.9rem;
    }

    /* ===== Main Header ===== */
    .hero-header {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, rgba(15, 15, 40, 0.9) 0%, rgba(30, 30, 70, 0.7) 100%);
        border-radius: 20px;
        border: 1px solid rgba(100, 100, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #8888aa;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    /* ===== Search Box Styling ===== */
    .search-container {
        max-width: 750px;
        margin: 0 auto 2rem auto;
    }

    .stTextInput > div > div > input {
        background: rgba(25, 25, 50, 0.8) !important;
        border: 1px solid rgba(100, 100, 255, 0.2) !important;
        border-radius: 16px !important;
        padding: 1rem 1.4rem !important;
        font-size: 1.05rem !important;
        color: #e0e0ff !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: rgba(102, 126, 234, 0.6) !important;
        box-shadow: 0 0 25px rgba(102, 126, 234, 0.2), 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #6666888 !important;
    }

    /* ===== Answer Card ===== */
    .answer-card {
        background: linear-gradient(135deg, rgba(20, 20, 45, 0.9), rgba(30, 30, 65, 0.8));
        border: 1px solid rgba(100, 100, 255, 0.12);
        border-radius: 16px;
        padding: 1.8rem 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.5s ease-out;
    }

    .answer-card .answer-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #667eea;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 0.8rem;
    }

    .answer-card .answer-text {
        font-size: 1rem;
        color: #d0d0e8;
        line-height: 1.75;
    }

    /* ===== Source Card ===== */
    .source-card {
        background: rgba(15, 15, 35, 0.7);
        border: 1px solid rgba(100, 100, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        transition: all 0.2s ease;
    }

    .source-card:hover {
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.08);
    }

    .source-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        margin-bottom: 0.6rem;
        letter-spacing: 0.5px;
    }

    .source-text {
        font-size: 0.88rem;
        color: #9999bb;
        line-height: 1.6;
    }

    /* ===== Greeting Card ===== */
    .greeting-card {
        background: linear-gradient(135deg, rgba(25, 40, 60, 0.8), rgba(20, 25, 50, 0.8));
        border: 1px solid rgba(100, 200, 255, 0.15);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem auto;
        max-width: 600px;
        animation: fadeInUp 0.4s ease-out;
    }

    .greeting-card p {
        color: #b0c8e8;
        font-size: 1.05rem;
        line-height: 1.7;
    }

    /* ===== Warning Box ===== */
    .warning-box {
        background: rgba(40, 30, 15, 0.6);
        border: 1px solid rgba(255, 180, 50, 0.2);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 1.5rem 0;
        animation: fadeInUp 0.4s ease-out;
    }

    .warning-box p {
        color: #e8c880;
        font-size: 0.95rem;
    }

    /* ===== Feature Cards in Sidebar ===== */
    .feature-card {
        background: rgba(25, 25, 50, 0.5);
        border: 1px solid rgba(100, 100, 255, 0.1);
        border-radius: 10px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.6rem;
        transition: all 0.2s ease;
    }

    .feature-card:hover {
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateX(3px);
    }

    .feature-card .feature-icon {
        font-size: 1.3rem;
        margin-right: 0.5rem;
    }

    .feature-card .feature-text {
        color: #b0b0d0;
        font-size: 0.85rem;
    }

    /* ===== Expander Styling ===== */
    .streamlit-expanderHeader {
        background: rgba(20, 20, 45, 0.6) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(100, 100, 255, 0.1) !important;
        color: #9999cc !important;
        font-weight: 500 !important;
    }

    /* ===== Footer ===== */
    .custom-footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #555577;
        font-size: 0.78rem;
        letter-spacing: 0.3px;
    }

    /* ===== Animations ===== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }

    .loading-dots {
        animation: pulse 1.5s ease-in-out infinite;
        color: #667eea;
        font-size: 1.1rem;
    }

    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: rgba(15, 15, 30, 0.5); }
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.3);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(102, 126, 234, 0.5); }
</style>
""", unsafe_allow_html=True)


# =========================================================
# Sidebar
# =========================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 0.8rem 0;">
        <div style="font-size: 2.5rem;">⚖️</div>
        <div style="font-size: 1.2rem; font-weight: 700;
             background: linear-gradient(135deg, #667eea, #764ba2);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             background-clip: text; margin-top: 0.3rem;">
            Legal AI Assistant
        </div>
        <div style="font-size: 0.75rem; color: #6666888; margin-top: 0.3rem;">
            Powered by RAG + LLM
        </div>
    </div>
    <hr style="border: none; border-top: 1px solid rgba(100,100,255,0.1); margin: 1rem 0;">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-bottom: 1.2rem;">
        <div style="font-size: 0.72rem; font-weight: 600; color: #667eea;
             text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.8rem;">
            ✦ Capabilities
        </div>
        <div class="feature-card">
            <span class="feature-icon">📋</span>
            <span class="feature-text">Filing FIR & Police Complaints</span>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🏠</span>
            <span class="feature-text">Tenant & Landlord Rights</span>
        </div>
        <div class="feature-card">
            <span class="feature-icon">💼</span>
            <span class="feature-text">Employment & Labor Disputes</span>
        </div>
        <div class="feature-card">
            <span class="feature-icon">🛡️</span>
            <span class="feature-text">Consumer Protection Guidance</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="border: none; border-top: 1px solid rgba(100,100,255,0.1); margin: 1rem 0;">
    <div style="font-size: 0.72rem; font-weight: 600; color: #667eea;
         text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.8rem;">
        💡 Try asking
    </div>
    """, unsafe_allow_html=True)

    sample_questions = [
        "How to file an FIR in India?",
        "What are tenant rights?",
        "How to file a consumer complaint?",
        "What is the process for bail?"
    ]

    for q in sample_questions:
        if st.button(f"→  {q}", key=f"sample_{q}", use_container_width=True):
            st.session_state["user_query"] = q

    st.markdown("""
    <hr style="border: none; border-top: 1px solid rgba(100,100,255,0.1); margin: 1rem 0;">
    <div style="font-size: 0.72rem; color: #555577; text-align: center; padding: 0.5rem 0;">
        ⚠️ This AI provides general legal information<br>and does not replace professional legal advice.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# Main Content — Hero Header
# =========================================================

st.markdown("""
<div class="hero-header">
    <div class="hero-title">⚖️ Legal AI Assistant</div>
    <div class="hero-subtitle">Ask questions about legal procedures, rights, and regulations</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# Search Input
# =========================================================

# Prefill from sidebar sample question if clicked
default_query = st.session_state.get("user_query", "")

st.markdown('<div class="search-container">', unsafe_allow_html=True)
query = st.text_input(
    "Ask a legal question",
    value=default_query,
    placeholder="e.g. How do I file an FIR in India?",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# Clear the session state after using it
if "user_query" in st.session_state:
    del st.session_state["user_query"]


# =========================================================
# Query Processing
# =========================================================

if query:

    intent = detect_intent(query)

    # --- Greeting ---
    if intent == "greeting":
        st.markdown("""
        <div class="greeting-card">
            <p style="font-size: 1.8rem; margin-bottom: 0.5rem;">👋</p>
            <p>Hello! Welcome to the <strong>Legal AI Assistant</strong>.<br>
            You can ask about legal procedures such as filing complaints,
            tenant rights, employment disputes, or consumer complaints.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # --- Retrieve & Answer ---
    with st.spinner("Searching legal knowledge base..."):
        docs = retrieve_documents(query, namespace="legal_kb")

    if not docs:
        st.markdown("""
        <div class="warning-box">
            <p>⚠️ No relevant legal information found for your query. Try rephrasing
            or ask about a specific legal procedure.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        llm = get_llm()

        with st.spinner("Generating answer..."):
            answer = generate_answer(llm, query, docs)

        # --- Display Answer ---
        st.markdown(f"""
        <div class="answer-card">
            <div class="answer-label">✦ Answer</div>
            <div class="answer-text">{answer}</div>
        </div>
        """, unsafe_allow_html=True)

        # --- Display Sources ---
        with st.expander("🔎  View Sources Used to Generate This Answer"):
            for i, doc in enumerate(docs):
                source = doc.get("source", "Unknown document")
                page_num = doc.get("page")
                page_label = f" · Page {page_num}" if page_num else ""

                st.markdown(f"""
                <div class="source-card">
                    <div class="source-badge">📄 {source}{page_label}</div>
                    <div class="source-text">{doc["text"]}</div>
                </div>
                """, unsafe_allow_html=True)


# =========================================================
# Footer
# =========================================================

st.markdown("""
<div class="custom-footer">
    Built with Streamlit · Pinecone · Groq LLM · LangChain<br>
    ⚖️ Legal AI Assistant — For informational purposes only
</div>
""", unsafe_allow_html=True)