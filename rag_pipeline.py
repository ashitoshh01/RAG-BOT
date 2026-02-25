import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "vectorstore")


def get_rag_chain():
    # Initialize embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # Load the vector store from disk
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

    # Create the retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # Create the prompt template focusing on strictly answering from context
    prompt_template = """You are the official AI Customer Support Assistant for DoOrDue.

Your responsibility is to answer user questions strictly and only using the information provided in the context.

Rules you MUST follow:

1. Answer ONLY using the provided context.
2. Do NOT use outside knowledge.
3. Do NOT assume or infer missing details.
4. Do NOT fabricate features, policies, numbers, or explanations.
5. If the answer cannot be found directly in the context, you must politely and naturally explain that you don't have that specific information, acting as a helpful customer support agent.
6. Do NOT mention the word "context" or "resources" explicitly as if you're an AI reading a prompt.
7. Do NOT explain your technical AI limitations.
8. Do NOT add extra information beyond what is written.
9. If the question is completely unrelated to DoOrDue, politely steer the conversation back to helping with DoOrDue issues.

Maintain a professional, clear, and official tone at all times.

Context:
{context}

Question:
{input}

Answer:"""

    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "input"]
    )

    # Create chains
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    return retrieval_chain


def ask_question(question: str) -> str:
    chain = get_rag_chain()
    response = chain.invoke({"input": question})
    return response["answer"]
