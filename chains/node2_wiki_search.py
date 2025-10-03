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
    template="""你是一位严谨的历史学家。你的任务是仔细阅读和分析下面的维基百科内容，并根据用户的原始查询，从中提取出3至5个相关的历史事件。

对于你提取的每一个事件，你都必须按照以下格式提供详尽的信息：
- **year**: 事件发生的四位数年份。
- **title**: 事件的官方或通用标题。
- **type**: 对事件性质的分类，例如：金融危机、货币危机、地缘政治冲突、技术革命等。
- **description**: 一句话高度概括事件的核心内容。
- **outcome**: 事件的最终结果或长期的、深远的影响。
- **relevance_score**: 评估该历史事件与用户查询的相似度和参考价值，给出一个0到100之间的整数评分。100分表示极其相关和重要。
- **details**: 基于维基百科内容，提供一段详细的阐述（约100-150字），深入解释事件的背景、过程和关键触发因素。

{format_instructions}

用户的原始查询: {user_query}
维基百科内容:
{wiki_content}

请严格按照上述要求，返回一个包含这些历史事件详细信息的列表。""",,
    input_variables=["user_query", "wiki_content"],
    partial_variables={"format_instructions": parser2b.get_format_instructions()},
)

# 4. Construct the final chain, using the tool
chain2b = (
    { 
        "wiki_content": (lambda x: wikipedia_tool.run(x["search_query"])),
        "user_query": (lambda x: x["user_query"])
    }
    | prompt2b
    | llm
    | parser2b
)