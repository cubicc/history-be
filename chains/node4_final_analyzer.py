from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm import llm
from models import Node4_FinalAnalysis

# --- Node 4: Predict and Advise ---
parser4 = PydanticOutputParser(pydantic_object=Node4_FinalAnalysis)
prompt4 = PromptTemplate(
    template="""综合以下所有信息，为用户的原始查询提供最终分析。

原始事件分析:
{analyzed_event}

相似历史事件:
{historical_events}

历史规律总结:
{patterns}

{format_instructions}

请基于以上信息，分析用户当前事件可能遵循的规律，预测未来结果，并给出建议。""",
    input_variables=["analyzed_event", "historical_events", "patterns"],
    partial_variables={"format_instructions": parser4.get_format_instructions()},
)
chain4 = prompt4 | llm | parser4