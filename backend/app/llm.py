# backend/app/llm.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables from .env
load_dotenv()

def get_llm():
    """
    Initializes and returns the ChatOpenAI model configured 
    to use the free GitHub Models API endpoint.
    """
    gh_token = os.getenv("GITHUB_TOKEN")

    if not gh_token:
        raise ValueError("GITHUB_TOKEN not found in .env file.")

    # Setting up ChatOpenAI to route to GitHub's free model catalog
    llm = ChatOpenAI(
        model="gpt-4o-mini", # You can also use "gpt-4o"
        api_key=gh_token,
        base_url="https://models.inference.ai.azure.com",
        temperature=0.2
    )
    return llm

# Simple verification test block
if __name__ == "__main__":
    try:
        print("Testing connection to GitHub Models...")
        model = get_llm()
        response = model.invoke("Hello! Confirm you are running via GitHub Models.")
        print("\nSuccess! Model Response:")
        print(response.content)
    except Exception as e:
        print(f"\nInitialization failed: {e}")