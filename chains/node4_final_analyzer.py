from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm import llm
from models import Node4_FinalAnalysis

# --- Node 4: Predict and Advise ---
parser4 = PydanticOutputParser(pydantic_object=Node4_FinalAnalysis)
prompt4 = PromptTemplate(
template="""角色：你是一位精通预测的智者，擅长依据已有事件、相似历史事件、内涵规律，预测未来结果，并给出中肯建议。
      
任务：请你综合以下所有信息，为用户的原始查询提供最终分析。注意，每个事件都有可能包含多条事件发展路径，你要准确预测最有可能的结局。

原始事件分析:
{analyzed_event}

相似历史事件:
{historical_events}

历史规律总结:
{patterns}

{format_instructions}

输出：
预测结果：充分遵循已有信息，准确预测未来结果，并富有逻辑和情感的解释
建议：针对用户本人给出一句浓缩的谏言，要求有逻辑性和说服力，但不要过于具体，给用户引导，类似于名人名言
    例如："机会很快会到来，始终留在牌桌上", "谨慎加仓核心资产，回避高杠杆高贝塔标的，耐心是最好的操作" """,
    input_variables=["analyzed_event", "historical_events", "patterns"],
    partial_variables={"format_instructions": parser4.get_format_instructions()},
)
chain4 = prompt4 | llm | parser4