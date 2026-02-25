import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

DOC_PATH = os.path.join(os.path.dirname(__file__), "documents", "context.txt")
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "vectorstore")


def ingest_documents():
    print(f"Loading document from {DOC_PATH}...")
    if not os.path.exists(DOC_PATH):
        print("Error: Context document not found!")
        return

    loader = TextLoader(DOC_PATH, encoding="utf-8")
    docs = loader.load()

    print("Splitting text into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, length_function=len
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks.")

    print("Creating embeddings and storing in Vector DB...")
    embeddings = OpenAIEmbeddings()

    # Create and persist vectorstore
    Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=CHROMA_PATH
    )
    print("Ingestion complete. Vector store created at", CHROMA_PATH)


if __name__ == "__main__":
    ingest_documents()
