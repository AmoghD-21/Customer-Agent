# backend/app/test_tools.py
from llm import get_llm
from tools import support_tool_catalog

def test_tool_binding():
    print("Initializing LLM engine...")
    llm = get_llm()
    
    # Force bind the tool specifications directly into the model instance
    print("Binding custom SQLite lookup tools into the LLM definition...")
    llm_with_tools = llm.bind_tools(support_tool_catalog)
    
    # Ask a natural question targeting our order status tool
    user_query = "Hey, could you tell me what's going on with order ORD_1042?"
    print(f"\nSending sample query: '{user_query}'")
    
    response = llm_with_tools.invoke(user_query)
    
    # Check if the LLM correctly decided to call a tool
    if response.tool_calls:
        print("\n🎉 Success! The LLM successfully determined it needs a tool call.")
        for call in response.tool_calls:
            print(f"-> Executing Tool Name: '{call['name']}'")
            print(f"-> Extracted Target Arguments: {call['args']}")
    else:
        print("\n❌ The LLM skipped tool calling and returned raw text instead:")
        print(response.content)

if __name__ == "__main__":
    test_tool_binding()