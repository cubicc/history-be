from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm import llm
from models import Node4_FinalAnalysis

# --- Node 4: Predict and Advise ---
parser4 = PydanticOutputParser(pydantic_object=Node4_FinalAnalysis)
prompt4 = PromptTemplate(
template="""角色：你是一位精通预测的智者，擅长依据已有事件、相似历史事件、内涵规律，预测未来结果，并给出中肯建议。
任务：请你综合以下所有信息，为用户的原始查询提供最终分析。注意，每个事件都有可能包含多条事件发展路径，你要准确预测最有可能的结局。
**输入信息:**
1.  **原始事件分析:**
    {analyzed_event}
2.  **相似历史事件:**
    {historical_events}
3.  **历史规律总结:**
    {patterns}

**输出要求:**
请严格按照以下JSON格式进行输出，不要有任何额外的解释或说明：
{format_instructions}

**输出内容的具体指引:**
1.  **overall_analysis**: 撰写一段宏观的、全局性的分析。这段分析需要融合历史规律和当前事件的特点，深刻揭示事件的核心驱动因素和潜在的演变路径。语言要精炼、深刻，展现出战略高度。
2.  **future_predictions**: 提供一个包含2到3个结构化预测的列表。每个预测都需要覆盖不同的时间维度（例如：短期、中期、长期），并包含以下所有字段：
    *   `duration`: 预测的时间范围 (例如: "未来1-3个月", "未来1年内")。
    *   `description`: 对该时间段内可能发生情况的具体描述。
    *   `key_factors`: 影响此预测实现的关键因素列表（单条不超过 8 字，用核心名词 / 短语表述，无需括号补充说明）。
    *   `confidence`: 你作为分析师，对这个预测的信心指数 (0-100)。
    *   `probability`: 基于数据和模型，该预测发生的客观概率 (0-100)。
3.  **suggestion**: 针对用户本人给出一句浓缩的谏言，要求有逻辑性和说服力，但不要过于具体，给用户引导，类似于名人名言
    例如："机会很快会到来，始终留在牌桌上", "谨慎加仓核心资产，回避高杠杆高贝塔标的，耐心是最好的操作"
4.  **practical_advice**: 基于事件分析，给出具有公益性的，可执行的、可操作的、对个人的实际建议。要求具体、实用、可操作性强。
    例如：煤气爆炸事件返回防火守则和应急措施；货币危机返回具体的理财建议和资产配置方案
""",
    input_variables=["analyzed_event", "historical_events", "patterns"],
    partial_variables={"format_instructions": parser4.get_format_instructions()},
)
chain4 = prompt4 | llm | parser4