from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from llm import llm
from models import Node2_SimilarEvents

# --- Node 2B: Find Similar Historical Events (Wikipedia) ---

# 1. Initialize the API wrapper with the specific Chinese Wikipedia API endpoint
api_wrapper = WikipediaAPIWrapper(
    lang="zh",
    top_k_results=3,
    doc_content_chars_max=1500
)

# 2. Create the tool instance
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# 3. Define the prompt for the LLM to process the retrieved content
parser2b = PydanticOutputParser(pydantic_object=Node2_SimilarEvents)
prompt2b = PromptTemplate(
    template="""你是一位历史学家。请仔细分析以下维基百科摘要，并从中提取出5到10个与用户原始查询相关的历史事件。

维基百科内容:
{wiki_content}

{format_instructions}
请将提取的历史事件构造成一个列表。""",
    input_variables=["wiki_content"],
    partial_variables={"format_instructions": parser2b.get_format_instructions()},
)

# 4. Construct the final chain, using the tool
chain2b = (
    { "wiki_content": (lambda x: wikipedia_tool.run(x["search_query"])) }
    | prompt2b
    | llm
    | parser2b
)