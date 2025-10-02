from fastapi import FastAPI
import json
from datetime import datetime
from dotenv import load_dotenv

# Import models and chains from their modules
from models import UserQuery, Node4_FinalAnalysis
from chains.node1_planner import chain1 as planner_chain
from chains.node2_llm_search import chain2a as llm_search_chain
from chains.node2_wiki_search import chain2b as wiki_search_chain
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

@app.post("/analyse", response_model=Node4_FinalAnalysis)
async def analyse(query: UserQuery):
    """
    接收用户查询并执行一个动态的、模块化的四步分析工作流。
    """
    workflow_outputs = []

    # Node 1: Planner
    planner_output = await planner_chain.ainvoke({"query": query.query})
    workflow_outputs.append({"node": 1, "step": "Planner", "output": planner_output.dict()})

    # Node 2: Dynamic Execution with Fallback
    similar_events = None
    if planner_output.next_step == "wikipedia_search":
        print("--- Attempting Node 2B (Wikipedia) ---")
        try:
            similar_events = await wiki_search_chain.ainvoke({"search_query": planner_output.search_query})
            workflow_outputs.append({"node": 2, "step": "Wikipedia Search (Success)", "output": similar_events.dict()})
        except Exception as e:
            print(f"--- Wikipedia Tool Failed: {e} ---")
            print("--- Falling back to Node 2A (LLM) ---")
            workflow_outputs.append({"node": 2, "step": "Wikipedia Search (Failed)", "error": str(e)})
    
    if similar_events is None:
        print("--- Executing Node 2A (LLM) ---")
        similar_events = await llm_search_chain.ainvoke({"search_query": planner_output.search_query})
        workflow_outputs.append({"node": 2, "step": "LLM Search", "output": similar_events.dict()})

    # Node 3: Identify underlying patterns
    underlying_patterns_output = await pattern_identifier_chain.ainvoke({"historical_events": similar_events.json()})
    workflow_outputs.append({"node": 3, "step": "Identify Patterns", "output": underlying_patterns_output.dict()})

    # Node 4: Predict and advise
    final_analysis = await final_analyzer_chain.ainvoke({
        "analyzed_event": planner_output.json(),
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

    return final_analysis