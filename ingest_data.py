import os
import argparse
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Load environment variables from the parent directory's .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "vectorstore")


def main():
    parser = argparse.ArgumentParser(
        description="Ingest a document into the ChromaDB vector store."
    )
    parser.add_argument(
        "file_path", type=str, help="Path to the PDF or text file to ingest."
    )
    args = parser.parse_args()

    file_path = args.file_path
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    print(f"Loading document from {file_path}...")
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.lower().endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        print("Error: Unsupported file format. Please provide a .pdf or .txt file.")
        return

    documents = loader.load()
    print(f"Loaded {len(documents)} document pages/sections.")

    print("Splitting document into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Initializing embedding model and saving to ChromaDB...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # Create and persist the vectorstore mapped directly to CHROMA_PATH
    Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)

    print(
        f"Successfully ingested {len(chunks)} chunks into the vector store at {CHROMA_PATH}"
    )


if __name__ == "__main__":
    main()
