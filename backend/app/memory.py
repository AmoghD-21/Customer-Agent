# backend/app/memory.py
import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from llm import get_llm

# Load environment variables
load_dotenv()

# Use the exact same free embedding engine from Phase 2
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
MEMORY_DIR = os.path.join(os.path.dirname(__file__), "../../data/customer_memories_db")

def get_memory_db():
    """Initializes and returns our local persistent memory collection store."""
    return Chroma(
        persist_directory=MEMORY_DIR,
        embedding_function=embedding_model,
        collection_name="user_preferences"
    )

def add_customer_memory(text: str, customer_id: str):
    """
    Extracts customer behavioral traits using our free GitHub model,
    then logs them permanently into our local data storage folder.
    """
    llm = get_llm()
    db = get_memory_db()

    prompt = f"""
    Analyze the following customer service conversation history. 
    Extract long-term behavioral facts, explicit communication preferences, or shipping habits.
    Ignore temporary information like greetings, random questions, or specific tracking numbers.
    Provide your output as individual short sentences separated by newlines. 
    If no long-term preferences are found, reply strictly with the word 'NONE'.

    Text: "{text}"
    Extracted facts:
    """

    try:
        response = llm.invoke(prompt)
        extracted_facts = response.content.strip()

        if "NONE" in extracted_facts or not extracted_facts:
            return

        # Clean and filter individual bullet lines
        facts = [line.strip("- ").strip() for line in extracted_facts.split("\n") if line.strip()]

        if facts:
            # Add text documents metadata-tagged to this specific unique customer id
            db.add_texts(
                texts=facts,
                metadatas=[{"user_id": customer_id} for _ in facts]
            )
            print(f"✅ Extracted and recorded {len(facts)} memory metrics for {customer_id}")

    except Exception as e:
        print(f"❌ Core memory logging failure: {e}")

def recall_customer_context(customer_id: str) -> str:
    """Queries our vector layer for all memory records matching the customer ID code."""
    db = get_memory_db()
    
    # Retrieve matching vector metrics filtered by our metadata key
    results = db.get(where={"user_id": customer_id})

    if not results or not results["documents"]:
        return "No prior chronicled memory profile notes recorded for this customer."

    # Return documents compiled neatly as bulleted profiles
    fact_list = [f"- {doc}" for doc in results["documents"]]
    return "\n".join(fact_list)