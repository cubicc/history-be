from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm import llm
from models import Node1_5_WikiQueryOutput

# --- Node 1.5: Wikipedia Query Optimizer ---
parser1_5 = PydanticOutputParser(pydantic_object=Node1_5_WikiQueryOutput)
prompt1_5 = PromptTemplate(
    template="""你是一个维基百科搜索专家。你的任务是将用户提供的事件描述，转换成一个最可能在维基百科上找到精确匹配词条的搜索关键词。

你的输出需要遵循以下原则：
1. **精确性**: 关键词应该尽可能地具体和独特，以避免歧义。例如，对于“美国登月”，优化为“阿波罗11号登月计划”。
2. **核心实体**: 专注于事件的核心人物、地点或专有名词。例如，对于“那个发明了电话的人”，优化为“亚历山大·格拉汉姆·贝尔”。
3. **简洁**: 去除所有不必要的描述性词语，只保留核心关键词。

{format_instructions}

待优化的事件信息:
人物: {person}
事件描述: {event_description}
""",
    input_variables=["person", "event_description"],
    partial_variables={"format_instructions": parser1_5.get_format_instructions()},
)
chain1_5 = prompt1_5 | llm | parser1_5