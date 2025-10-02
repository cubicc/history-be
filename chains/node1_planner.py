from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm import llm
from models import Node1_PlannerOutput

# --- Node 1: Planner ---
parser1 = PydanticOutputParser(pydantic_object=Node1_PlannerOutput)
prompt1 = PromptTemplate(
    template="""分析用户的查询，提取关键信息，并规划下一步。
对于时事、具体人物或技术性强的查询，规划使用维基百科。对于更抽象或概念性的查询，规划使用大模型内部知识。

{format_instructions}

用户查询: '{query}'""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser1.get_format_instructions()},
)
chain1 = prompt1 | llm | parser1