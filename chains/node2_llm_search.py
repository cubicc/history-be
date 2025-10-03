from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm import llm
from models import Node2_SimilarEvents

# --- Node 2A: Find Similar Historical Events (LLM) ---
parser2a = PydanticOutputParser(pydantic_object=Node2_SimilarEvents)
prompt2a = PromptTemplate(
    template="""你是一位资深的历史学家和金融分析师。你的任务是根据用户的查询，从世界历史中找出3至5个高度相似或具有重要参考价值的事件。

对于你找出的每一个事件，你都必须按照以下格式提供详尽的信息：
- **year**: 事件发生的四位数年份。
- **title**: 事件的官方或通用标题。
- **type**: 对事件性质的分类，例如：金融危机、货币危机、地缘政治冲突、技术革命等。
- **description**: 一句话高度概括事件的核心内容。
- **outcome**: 事件的最终结果或长期的、深远的影响。
- **relevance_score**: 评估该历史事件与用户查询的相似度和参考价值，给出一个0到100之间的整数评分。100分表示极其相关和重要。
- **details**: 提供一段详细的阐述（约100-150字），深入解释事件的背景、过程、关键触发因素以及它为何与用户查询的事件具有可比性。

{format_instructions}

用户的查询是: '{search_query}'

请严格按照上述要求，返回一个包含这些历史事件详细信息的列表。""",
    input_variables=["search_query"],
    partial_variables={"format_instructions": parser2a.get_format_instructions()},
)
chain2a = prompt2a | llm | parser2a