import asyncio
from chains.node2_wiki_search import chain2b
from dotenv import load_dotenv

async def main():
    # Load environment variables
    load_dotenv()

    # A relevant Chinese search query to test the retriever
    test_query = "美国货币紧缩历史"
    print(f"--- Testing Node 2B (Wikipedia Retriever) with query: '{test_query}' ---")

    try:
        # Invoke the chain. The chain now expects a 'search_query' key.
        result = await chain2b.ainvoke({"search_query": test_query})

        # Print the structured result
        print("\n--- SUCCESS ---")
        print("Structured output from chain2b:")
        # The result is a Pydantic model, so we can print its dict representation
        print(result.dict())

    except Exception as e:
        print(f"\n--- ERROR ---")
        print(f"An error occurred during the test: {type(e).__name__}")
        print(f"Error details: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())