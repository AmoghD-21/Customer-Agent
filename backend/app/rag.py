# backend/app/rag.py
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICY_PATH = os.path.join(BASE_DIR, "../data/policies.txt")
CHROMA_PATH = os.path.join(BASE_DIR, "../data/chroma_db")

# Initialize a completely free, local embedding model
# This runs locally on your CPU/GPU without needing an API key
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_policies():
    """Reads policies.txt, splits it into digestible chunks, and indexes it in ChromaDB."""
    if not os.path.exists(POLICY_PATH):
        raise FileNotFoundError(f"Could not find company policies at {POLICY_PATH}")

    print("Loading policy document...")
    loader = TextLoader(POLICY_PATH)
    documents = loader.load()

    # Split text into small chunks so the agent retrieves highly specific context
    print("Splitting text into structural chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # Initialize and save the vector store locally
    print(f"Creating vector database at {CHROMA_PATH}...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH
    )
    print("Knowledge Base RAG successfully indexed!")
    return vector_store

def get_policy_retriever():
    """Loads the existing vector database and returns it as a retriever object."""
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model
    )
    return vector_store.as_retriever(search_kwargs={"k": 2}) # Fetches top 2 most relevant chunks

if __name__ == "__main__":
    # Run standalone ingest and testing script
    ingest_policies()
    
    # Simple search verification test
    print("\n--- Testing RAG Engine Retrieval ---")
    retriever = get_policy_retriever()
    query = "What happens if my package is delayed?"
    relevant_docs = retriever.invoke(query)
    
    print(f"Query: '{query}'")
    print(f"Retrieved Context Found:\n")
    for doc in relevant_docs:
        print(f"- {doc.page_content}\n")