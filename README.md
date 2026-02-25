# Expert RAG Chatbot

This project is an AI-powered customer support assistant built using **FastAPI** for the backend, **LangChain** with **ChromaDB** for Retrieval-Augmented Generation (RAG), and a simple **HTML/CSS/JS** frontend.

The application serves both the API endpoints and the frontend static files on the same server for simplicity.

## Project Structure

```text
RAG/
├── main.py                # FastAPI application and routes
├── rag_pipeline.py        # LangChain setup and querying logic
├── ingest_data.py         # Script to ingest new PDF/TXT into ChromaDB
├── vectorstore/           # Directory containing the ChromaDB embeddings
├── index.html             # User interface
├── script.js              # Logic to handle user chat and API communication
├── style.css              # Styling for the chatbot UI
├── .env                   # Environment variables
└── requirements.txt       # Python dependencies
```

## Prerequisites

- Python 3.8+
- An OpenAI API key

## Setup Instructions

### 1. Clone or Navigate to the Project Directory

```bash
cd RAG
```

### 2. Create and Activate a Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Create the Environment File

Create a `.env` file in the root directory (`RAG/`) if it doesn't already exist, and add your **OpenAI API key**. 
*(Note: Your current `.env` file seems to have a Google-style API key starting with `AIzaSy`. It must be a valid OpenAI API key starting with `sk-`)*

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Add Your Vector Store Data

We have created an ingestion script (`ingest_data.py`) for you, which will take a PDF or Text file, split it into chunks, and store it in ChromaDB automatically.

Make sure your virtual environment is activated, then run:

```bash
# To ingest a PDF file
python ingest_data.py path/to/your/document.pdf

# Or to ingest a Text file
python ingest_data.py path/to/your/document.txt
```

This will embed the file's contents and create the `vectorstore` directory for you.

## Running the Application

To start the server, use `uvicorn`. The application auto-serves both your API and frontend files automatically.

**Run from the root directory:**

```bash
uvicorn main:app --reload
```

## Accessing the Chatbot

Once the server is running, open your web browser and navigate to:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

You can now start interacting with the Expert Support Assistant through the chat interface.

## Notes

- The system uses the `gpt-4o-mini` model with zero temperature to provide accurate answers strictly restricted to the contextual data provided in the Chroma vector store.
- If the required context is missing, the AI is programmed to fallback gracefully without hallucinating.
