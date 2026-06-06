# backend/app/test_memory.py
from memory import add_customer_memory, recall_customer_context

def test_memory_lifecycle():
    print("🚀 Starting the Custom Long-Term Memory Engine Test...")
    test_user = "CUST_101"
    
    # 1. Simulate customer preference statement
    print(f"\n[Step 1] Simulating customer comment for {test_user}...")
    conversation_1 = "Hi, I am Alex Rivera. Please make sure to contact me via email. I do not answer phone calls."
    add_customer_memory(conversation_1, customer_id=test_user)

    # 2. Verify retrieval immediately
    print(f"\n[Step 2] Recalling current customer memory dashboard for {test_user}:")
    current_memory = recall_customer_context(test_user)
    print(current_memory)

    # 3. Simulate another preference update later in time
    print(f"\n[Step 3] Simulating subsequent follow-up statement...")
    conversation_2 = "By the way, I prefer delivery to my office headquarters instead of my residential home."
    add_customer_memory(conversation_2, customer_id=test_user)

    # 4. Final Output Readout showing both compiled historical facts
    print(f"\n[Step 4] Reading final compiled profile record from disk storage:")
    updated_memory = recall_customer_context(test_user)
    print(updated_memory)

if __name__ == "__main__":
    test_memory_lifecycle()