from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from llm import llm
from models import Node3_UnderlyingPatterns

# --- Node 3: Identify Underlying Patterns ---
parser3 = PydanticOutputParser(pydantic_object=Node3_UnderlyingPatterns)
prompt3 = PromptTemplate(
    template="""分析以下历史事件列表，并总结出它们共同的内在规律或原理。
历史事件:
{historical_events}

{format_instructions}
请总结这些事件背后的深刻规律。""",
    input_variables=["historical_events"],
    partial_variables={"format_instructions": parser3.get_format_instructions()},
)
chain3 = prompt3 | llm | parser3