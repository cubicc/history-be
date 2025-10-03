from pydantic import BaseModel, Field
from typing import List, Literal

# --- Pydantic Models for Structured Output ---

class Node1_PlannerOutput(BaseModel):
    person: str = Field(description="关键人物")
    event_description: str = Field(description="事件的简要描述")
    search_query: str = Field(description="为下一步生成的优化搜索查询语句")

class Node1_5_WikiQueryOutput(BaseModel):
    wiki_search_term: str = Field(description="为维基百科优化的、最可能命中准确词条的搜索关键词")

class Node2_HistoricalEvent(BaseModel):
    year: int = Field(description="事件发生的年份")
    title: str = Field(description="历史事件的标题")
    type: str = Field(description="事件的类型，例如：金融危机、货币危机、战争等")
    description: str = Field(description="对历史事件的高度概括性描述")
    outcome: str = Field(description="历史事件的最终结果或长期影响")
    relevance_score: int = Field(description="该历史事件与用户原始查询的相关性评分，取值范围为 0 (完全不相关) 到 100 (极其相关)")
    details: str = Field(description="对事件的详细阐述，包括背景、过程和关键因素")

class Node2_SimilarEvents(BaseModel):
    historical_events: List[Node2_HistoricalEvent] = Field(description="相似历史事件的列表")

class Node3_UnderlyingPatterns(BaseModel):
    patterns: str = Field(description="从历史事件中总结出的内在规律")

class FuturePrediction(BaseModel):
    duration: str = Field(description="预测覆盖的时间范围，例如：未来1个月内、1-2年内")
    description: str = Field(description="对该时间范围内具体预测内容的描述")
    key_factors: List[str] = Field(description="影响该预测的关键因素列表")
    confidence: int = Field(description="分析师对该预测的信心指数，取值范围 0-100")
    probability: int = Field(description="该预测发生的客观概率估计，取值范围 0-100")

class FuturePredictionWithId(FuturePrediction):
    id: int = Field(description="从1开始顺序递增的唯一标识符")

class Node4_FinalAnalysis(BaseModel):
    overall_analysis: str = Field(description="基于所有历史事件和规律，对用户查询事件的宏观、整体性分析")
    future_predictions: List[FuturePrediction] = Field(description="对未来不同时间范围内的结构化预测列表")
    suggestion: str = Field(description="给用户的最终、可执行的建议")

class FullAnalysisResponse(BaseModel):
    historical_events: List[Node2_HistoricalEvent] = Field(description="与用户查询相似的历史事件列表")
    future_predictions: List[FuturePredictionWithId] = Field(description="对未来不同时间范围内的结构化预测列表")
    overall_analysis: str = Field(description="基于所有历史事件和规律，对用户查询事件的宏观、整体性分析")
    suggestion: str = Field(description="给用户的最终、可执行的建议")

# --- User Input Model ---

class UserQuery(BaseModel):
    query: str = Field(..., example="特朗普上台，发布货币紧缩政策")