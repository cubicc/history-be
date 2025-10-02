from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm import llm
from models import Node2_SimilarEvents

# --- Node 2A: Find Similar Historical Events (LLM) ---
parser2a = PydanticOutputParser(pydantic_object=Node2_SimilarEvents)
prompt2a = PromptTemplate(
    template="""根据以下查询，请从世界历史中找出5到10个高度相似的事件。
查询: {search_query}

{format_instructions}
请返回一个包含这些历史事件的列表。""",
    input_variables=["search_query"],
    partial_variables={"format_instructions": parser2a.get_format_instructions()},
)
chain2a = prompt2a | llm | parser2a