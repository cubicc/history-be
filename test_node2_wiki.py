import asyncio
from chains.node2_wiki_search import chain2b
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# A relevant Chinese search query to test the retriever
test_query = "特朗普发布货币紧缩政策"
api_wrapper = WikipediaAPIWrapper(
    lang="zh",
    top_k_results=3,
    doc_content_chars_max=1500
)

# 2. Create the tool instance
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

res = wikipedia_tool.run(test_query)
print(res)