# backend/app/agent.py
import os
from dotenv import load_dotenv
from llm import get_llm
from tools import support_tool_catalog, get_customer_profile, get_order_status
from rag import get_policy_retriever
from memory import recall_customer_context, add_customer_memory

load_dotenv()

def run_support_copilot(customer_id: str, current_ticket_text: str) -> dict:
    """
    Orchestrates RAG, Tools, and Memory to generate an automated,
    highly-contextual customer support draft.
    """
    # 1. Fetch historical memory records from Chroma
    print(f"\n[Agent Core] Fetching long-term memories for {customer_id}...")
    customer_memories = recall_customer_context(customer_id)
    
    # 2. Extract live data from SQLite tables using our tools directly
    print(f"[Agent Core] Executing backend CRM tool lookups...")
    profile_data = get_customer_profile.invoke({"customer_id": customer_id})
    
    # Try to scan the ticket text to see if an order number is explicitly specified
    # If found, run our order tracking tool automatically
    order_data = "No explicit order token searched."
    for word in current_ticket_text.replace("#", "").split():
        if word.startswith("ORD_"):
            order_data = get_order_status.invoke({"order_id": word})
            break

    # 3. Retrieve relevant company procedures via RAG
    print(f"[Agent Core] Running knowledge-base semantic vector search...")
    retriever = get_policy_retriever()
    relevant_docs = retriever.invoke(current_ticket_text)
    policy_context = "\n".join([f"- {doc.page_content}" for doc in relevant_docs])

    # 4. Construct a unified systemic prompt for our GitHub LLM
    print(f"[Agent Core] Assembling final context matrix and generating draft...")
    system_prompt = f"""
    You are an elite AI Customer Support Copilot assisting a human customer service agent.
    Your goal is to generate a comprehensive internal summary and a highly-polished, professional email response draft based strictly on the collected company metrics provided below.

    ### CRITICAL BUSINESS CONTEXT:
    * Live Customer CRM Profile: 
    {profile_data}
    
    * Operational Order/Tracking Status:
    {order_data}

    * Long-Term Memory Notes (Preferences/Habits):
    {customer_memories}

    * Retrieved Official Company Policies (RAG):
    {policy_context}

    ### INSTRUCTIONS:
    1. Address the customer by name if known.
    2. Respect all behavioral preferences listed in the Long-Term Memory section (e.g., communication channels, tone preferences).
    3. If an order is delayed, check if it qualifies for compensation based on retrieved policies.
    4. Provide your response in two distinct blocks: an 'INTERNAL SUMMARY' (bullet points for the human agent) and a 'PROPOSED EMAIL DRAFT' (ready to send to the client).
    """

    llm = get_llm()
    response = llm.invoke([
        ("system", system_prompt),
        ("human", current_ticket_text)
    ])
    
    # 5. Background Task: Feed the current conversation into our memory engine to update preferences
    print(f"[Agent Core] Queueing async update to customer background profile...")
    add_customer_memory(current_ticket_text, customer_id)

    return {
        "summary_and_draft": response.content,
        "profile": profile_data,
        "live_metrics": order_data,
        "remembered_history": customer_memories
    }

if __name__ == "__main__":
    # Test compilation flow
    test_ticket = "Hey, my order ORD_1042 hasn't arrived yet and I'm stressed! Can you check on it?"
    res = run_support_copilot("CUST_101", test_ticket)
    print("\n================= AGENT ENGINE OUTPUT =================")
    print(res["summary_and_draft"])