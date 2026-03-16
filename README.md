<div align="center">

# ⚖️ Ai-Legal-Assistant

### AI-Powered Legal Information System Using RAG

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Pinecone](https://img.shields.io/badge/Pinecone-000000?style=for-the-badge&logo=pinecone&logoColor=white)](https://pinecone.io)
[![Groq](https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)

> An intelligent legal information assistant that uses **Retrieval-Augmented Generation (RAG)** supplemented by a **Model Context Protocol (MCP)** internet fallback to answer questions about legal procedures, rights, and regulations — powered by Pinecone vector search, DuckDuckGo live search, Groq LLM (Llama 3.1), and a premium dark-themed Streamlit interface.

---

[Features](#-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [Project Structure](#-project-structure) · [API Keys](#-api-keys-required)

</div>

---

## ✨ Features

- 🔍 **Semantic Search** — Retrieves the most relevant legal documents using vector similarity search via Pinecone
- 🌐 **MCP Internet Fallback** — Uses DuckDuckGo to search the live internet via an MCP Server (`mcp_legal_server.py`) when the RAG database misses the answer
- 🤖 **AI-Powered Answers** — Generates clear, step-by-step legal guidance using Groq's Llama 3.1 LLM
- 📄 **PDF Ingestion Pipeline** — Automatically loads, chunks, embeds, and indexes legal PDF documents
- 🎨 **Premium Dark UI** — Sleek glassmorphism design with smooth animations and gradient accents
- 💡 **Smart Intent Detection** — Recognizes greetings vs. legal queries for natural conversation flow
- 📋 **Source Attribution** — Displays the exact source documents and pages used to generate each answer
- ⚡ **Lightning Fast** — Groq's inference engine delivers answers in milliseconds

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌──────────────────┐
│  Intent Filter   │  ← Detects greetings/farewells vs legal queries
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌────────────────────┐
│  HuggingFace     │────▶│  Pinecone Vector   │
│  Embeddings      │     │  Database (RAG)    │
└──────────────────┘     └────────┬───────────┘
                                  │
                   ┌──────────────┴───────────────┐
                   │                              │
          [Context Found]                  [Context Missed]
                   │                              │
                   ▼                              ▼
        ┌────────────────────┐         ┌────────────────────┐
        │  Groq LLM Context  │         │ MCP Search Server  │
        │  (Top-K Documents) │         │ (DuckDuckGo Search)│
        └────────┬───────────┘         └────────┬───────────┘
                 │                              │
                 └──────────────┬───────────────┘
                                ▼
                       ┌────────────────────┐
                       │  Groq LLM Setup    │
                       │  (Llama 3.1 8B)    │
                       └────────┬───────────┘
                                │
                                ▼
                       ┌────────────────────┐
                       │  Streamlit UI      │
                       │ (Answer + Sources) │
                       └────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Pinecone](https://pinecone.io) account (free tier works)
- [Groq](https://console.groq.com) API key (free tier available)

### 1. Clone the Repository

```bash
git clone https://github.com/prithivi003/Ai-Legal-Assistant.git
cd Ai-Legal-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_pinecone_index_name
```

### 5. Add Legal Documents

Place your legal PDF documents in the `data/legal_documents/` folder.

### 6. Build the Pinecone Index

```bash
python build_pinecone_index.py
```

This will:
- Load all PDFs from `data/legal_documents/`
- Split them into chunks (1000 chars with 200 overlap)
- Generate embeddings using HuggingFace `all-MiniLM-L6-v2`
- Upsert embeddings into your Pinecone index

### 7. Run the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🎉

---

## 📁 Project Structure

```text
Ai-Legal-Assistant/
├── app.py                      # Main Streamlit application (UI + query handling)
├── mcp_legal_server.py         # MCP server providing DuckDuckGo internet fallback tool
├── build_pinecone_index.py     # Script to ingest PDFs and build vector index
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not tracked)
├── .gitignore                  # Ignored files for version control
│
├── ai_research_platform/       # AI Research Modules
├── config/                     # Configuration/settings directories
├── features/                   # Additional Features & Extensions
├── ui/                         # User Interface specific components
│
├── rag/                        # RAG pipeline components
│   ├── loader.py               # Loads PDFs using LangChain PyPDFLoader
│   ├── chunker.py              # Splits documents into chunks (RecursiveCharacterTextSplitter)
│   ├── embedder.py             # Generates embeddings (HuggingFace MiniLM-L6-v2)
│   ├── retriever.py            # Queries Pinecone for relevant document chunks
│   ├── pipeline.py             # Constructs prompt and generates LLM answer
│   └── llm.py                  # Initializes Groq LLM (Llama 3.1 8B Instant)
│
├── services/                   # Service layer interacting with external APIs
│   ├── vector_service.py       # Pinecone client initialization, upsert & delete ops
│   ├── metadata_service.py     # Document metadata handling
│   └── storage_service.py      # File storage utilities
│
├── utils/                      # Helper Utilities
│   └── intent_filter.py        # Simple intent detection (greeting vs legal query)
│
└── data/                       # Data storage
    ├── legal_documents/        # Place legal PDF files here
    └── session_uploads/        # Temporary user uploads
```

---

## 🔑 API Keys Required

| Service | Purpose | Get Key |
|---------|---------|---------|
| **Groq** | LLM inference (Llama 3.1 8B) | [console.groq.com](https://console.groq.com) |
| **Pinecone** | Vector database for semantic search | [pinecone.io](https://app.pinecone.io) |

> **Note:** Both services offer generous free tiers sufficient for development and small-scale usage.

---

## 🎨 UI Preview

The application features a **premium dark theme** with:
- 🌌 Glassmorphism cards with blur effects
- 🎆 Gradient text and animated transitions
- 🔎 Elegant search input with glow focus effect
- 📱 Responsive sidebar with capabilities overview and sample questions
- 📄 Expandable source attribution cards

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit + Custom CSS |
| **LLM** | Groq (Llama 3.1 8B Instant) |
| **Embeddings** | HuggingFace `sentence-transformers/all-MiniLM-L6-v2` |
| **Vector DB** | Pinecone |
| **Agent fallback** | MCP Server (`mcp`, `duckduckgo_search`/`ddgs`) |
| **Framework** | LangChain |
| **PDF Parsing** | PyPDFLoader |
| **Text Splitting** | RecursiveCharacterTextSplitter |

---

## 📌 Topics Covered

The assistant can help with questions about:
- 📋 Filing FIR & Police Complaints
- 🏠 Tenant & Landlord Rights
- 💼 Employment & Labor Disputes
- 🛡️ Consumer Protection & Complaints
- ⚖️ Bail Procedures
- 📝 General Legal Procedures in India

---

## ⚠️ Disclaimer

> This AI provides **general legal information only** and does **not** replace professional legal advice. Always consult a qualified lawyer for specific legal matters.

<div align="center">

**Built with** ❤️ **using Streamlit · Pinecone · Groq · LangChain**

</div>