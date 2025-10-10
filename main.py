from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from datetime import datetime
from dotenv import load_dotenv

# Import models and chains from their modules
from models import UserQuery, Node2_SimilarEvents, Node4_FinalAnalysis, FullAnalysisResponse, FuturePredictionWithId
from chains.node1_query_extractor import chain1 as query_extractor_chain
# from chains.node1_5_wiki_query_optimizer import chain1_5 as wiki_query_optimizer_chain
from chains.node2_llm_search import chain2a as llm_search_chain
# from chains.node2_wiki_search import chain2b as wiki_search_chain
from chains.node3_pattern_identifier import chain3 as pattern_identifier_chain
from chains.node4_final_analyzer import chain4 as final_analyzer_chain

# Load environment variables
load_dotenv()

# Initialize the FastAPI app
app = FastAPI(
    title="以史为鉴 - AI Historical Analysis",
    description="An application that analyzes user queries, finds similar historical events, identifies patterns, and provides predictions and advice.",
    version="1.2.0", # Incremented version for the refactor
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/analyse", response_model=FullAnalysisResponse)
async def analyse(query: UserQuery):
    """
    接收用户查询并执行一个动态的、模块化的四步分析工作流。
    """
    workflow_outputs = []

    # Node 1: Extract Query
    extractor_output = await query_extractor_chain.ainvoke({"query": query.query})
    workflow_outputs.append({"node": 1, "step": "Query Extractor", "output": extractor_output.dict()})

    # # Node 1.5: Wikipedia Query Optimizer
    # print("--- Executing Node 1.5 (Wikipedia Query Optimizer) ---")
    # wiki_query_output = await wiki_query_optimizer_chain.ainvoke({
    #     "person": extractor_output.person,
    #     "event_description": extractor_output.event_description
    # })
    # workflow_outputs.append({"node": 1.5, "step": "Wikipedia Query Optimizer", "output": wiki_query_output.dict()})

    # # Node 2: Sequential Execution (Wiki then LLM)
    # print("--- Executing Node 2B (Wikipedia) ---")
    # wiki_events = await wiki_search_chain.ainvoke({"user_query": query.query, "search_query": wiki_query_output.wiki_search_term})
    # workflow_outputs.append({"node": 2, "step": "Wikipedia Search", "output": wiki_events.dict()})

    print("--- Executing Node 2A (LLM) ---")
    llm_events = await llm_search_chain.ainvoke({"search_query": extractor_output.search_query})
    workflow_outputs.append({"node": 2, "step": "LLM Search", "output": llm_events.dict()})

    # # Combine the results from both searches
    # combined_events_list = wiki_events.historical_events + llm_events.historical_events
    # similar_events = Node2_SimilarEvents(historical_events=combined_events_list)
    # workflow_outputs.append({"node": "2_combined", "step": "Combined Search Results", "output": similar_events.dict()})

    similar_events = llm_events

    # Node 3: Identify underlying patterns
    underlying_patterns_output = await pattern_identifier_chain.ainvoke({"historical_events": similar_events.json()})
    workflow_outputs.append({"node": 3, "step": "Identify Patterns", "output": underlying_patterns_output.dict()})

    # Node 4: Predict and advise
    final_analysis = await final_analyzer_chain.ainvoke({
        "analyzed_event": extractor_output.json(),
        "historical_events": similar_events.json(),
        "patterns": underlying_patterns_output.patterns
    })
    workflow_outputs.append({"node": 4, "step": "Final Analysis", "output": final_analysis.dict()})
    
    # Save the entire workflow output to a JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"workflow_output_{timestamp}.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(workflow_outputs, f, ensure_ascii=False, indent=4)
    
    print(f"Workflow output saved to {output_filename}")

    # Combine all results into the final response model, adding IDs to predictions
    predictions_with_ids = [
        FuturePredictionWithId(id=i+1, **p.dict())
        for i, p in enumerate(final_analysis.future_predictions)
    ]
    
    # Add predictions_with_ids to workflow_outputs
    workflow_outputs.append({
        "node": "final_response", 
        "step": "Predictions with IDs", 
        "output": [p.dict() for p in predictions_with_ids]
    })

    final_response = FullAnalysisResponse(
        historical_events=similar_events.historical_events,
        future_predictions=predictions_with_ids,
        overall_analysis=final_analysis.overall_analysis,
        suggestion=final_analysis.suggestion,
        practical_advice=final_analysis.practical_advice
    )

    return final_response