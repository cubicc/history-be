import asyncio
import json
from chains.node1_query_extractor import chain1 as query_extractor_chain

async def main():
    """
    This script tests the Node 1 Query Extractor.
    It takes a user query, invokes the chain, and prints the structured output.
    """
    # --- Define the user query you want to test ---
    user_query = "我已经两个月没有找到工作了"

    print(f"--- Testing Node 1: Query Extractor ---")
    print(f"Input Query: {user_query}")

    # Invoke the chain with the query
    extractor_output = await query_extractor_chain.ainvoke({"query": user_query})

    # Print the structured output
    print("\n--- Extractor Output ---")
    print(json.dumps(extractor_output.dict(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())