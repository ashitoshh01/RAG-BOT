# 🤖 RAG Chatbot — Expert AI Support Assistant

An AI-powered customer support chatbot built with **FastAPI**, **LangChain**, **ChromaDB**, and a clean HTML/CSS/JS frontend.

It uses **Retrieval-Augmented Generation (RAG)** to answer questions strictly from your own documents — no hallucinations.

---

## 🤖 AI Stack

| Component     | Provider / Model                              |
|---------------|-----------------------------------------------|
| **LLM**       | [Groq](https://groq.com) → `llama-3.3-70b-versatile` |
| **Embeddings**| Google Generative AI → `gemini-embedding-001` |
| **Vector DB** | ChromaDB (local, persisted to `vectorstore/`) |
| **Framework** | LangChain                                     |
| **Backend**   | FastAPI + Uvicorn                             |

---

## 📁 Project Structure

```text
RAG/
├── main.py            # FastAPI app — API routes & static file serving
├── rag_pipeline.py    # RAG logic: embeddings, retrieval, Groq LLM
├── ingest_data.py     # Script to ingest PDF/TXT into ChromaDB
├── index.html         # Chat UI (served at GET /)
├── script.js          # Frontend chat logic
├── style.css          # Chat UI styles
├── favicon.png        # Browser tab icon
├── vectorstore/       # ChromaDB persisted vector store (auto-generated)
├── documents/         # Place your source documents here
├── .env               # API keys (never commit this!)
└── requirements.txt   # Python dependencies
```

> 📌 See [SITEMAP.md](./SITEMAP.md) for a full detailed breakdown of every file.

---

## ⚙️ Setup Instructions

### 1. Clone / Navigate to the Project

```bash
cd RAG
```

### 2. Create & Activate a Virtual Environment

```bash
# macOS / Linux
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install langchain-groq langchain-google-genai langchain-chroma
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

- Get your **Groq API key**: [https://console.groq.com](https://console.groq.com)
- Get your **Google API key**: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 5. Ingest Your Documents

Place your PDF or TXT files in the `documents/` folder, then run:

```bash
# Ingest a PDF
python ingest_data.py path/to/your/document.pdf

# Ingest a TXT
python ingest_data.py path/to/your/document.txt
```

This creates the `vectorstore/` directory with the embeddings.

---

## 🚀 Running the Application

```bash
uvicorn main:app --reload
```

> ⚠️ Make sure your **venv is activated** before running.

Then open your browser at:

**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Serves the chat UI |
| `POST` | `/chat` | Send `{ "message": "..." }`, receive `{ "answer": "..." }` |

---

## 📝 Notes

- The LLM answers **only** from the context stored in ChromaDB — it will not hallucinate or use outside knowledge.
- If the answer isn't in the documents, the bot gracefully says it doesn't have that information.
- Temperature is set to `0` for deterministic, factual responses.
