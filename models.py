from pydantic import BaseModel, Field
from typing import List, Literal

# --- Pydantic Models for Structured Output ---

class Node1_PlannerOutput(BaseModel):
    person: str = Field(description="关键人物")
    event_description: str = Field(description="事件的简要描述")
    next_step: Literal["llm_search", "wikipedia_search"] = Field(description="规划下一步是使用大模型内部知识搜索还是调用维基百科进行搜索")
    search_query: str = Field(description="为下一步生成的优化搜索查询语句")

class Node2_HistoricalEvent(BaseModel):
    year: str = Field(description="事件发生的年份")
    event_name: str = Field(description="历史事件的名称")
    description: str = Field(description="历史事件的简要描述")
    outcome: str = Field(description="历史事件的最终结果")

class Node2_SimilarEvents(BaseModel):
    historical_events: List[Node2_HistoricalEvent] = Field(description="相似历史事件的列表")

class Node3_UnderlyingPatterns(BaseModel):
    patterns: str = Field(description="从历史事件中总结出的内在规律")

class Node4_FinalAnalysis(BaseModel):
    likely_patterns: str = Field(description="用户查询的事件最可能遵循的规律")
    future_outcome: str = Field(description="对未来的预测结果")
    advice: str = Field(description="给用户的具体建议")

# --- User Input Model ---

class UserQuery(BaseModel):
    query: str = Field(..., example="特朗普上台，发布货币紧缩政策")