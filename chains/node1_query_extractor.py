from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm import llm
from models import Node1_PlannerOutput

# --- Node 1: Planner ---
parser1 = PydanticOutputParser(pydantic_object=Node1_PlannerOutput)
prompt1 = PromptTemplate(
    template="""从用户的查询中提取关键人物和事件描述，并生成一个优化的、简洁的搜索查询语句，用于后续的知识库检索。

{format_instructions}

用户查询: '{query}'""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser1.get_format_instructions()},
)
chain1 = prompt1 | llm | parser1