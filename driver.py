import os
import time
from dotenv import load_dotenv
from datetime import datetime
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

from prompt import research_prompt, review_prompt
from agents import research_agent_factory, reviewer_agent_factory, AgentState
from tools import search


GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemma-3-27b-it", google_api_key=GEMINI_API_KEY, temperature=0)

current_time = datetime.now().strftime("%B %d, %Y")
res_prompt = research_prompt(current_time)
rev_prompt = review_prompt()

research_executor = research_agent_factory(llm, search, res_prompt)
review_executor = reviewer_agent_factory(llm, rev_prompt)


def call_researcher(state: AgentState):
    print(f"\n--- RESEARCH ROUND {state.get('iterations', 0) + 1} ---")
    research_input = f"Task: {state['input']}\nPrevious Feedback: {state.get('review_feedback', 'None')}"
    
    # Simple retry logic for API Overload
    for retry in range(3):
        try:
            res_out = research_executor.invoke({"input": research_input})["output"]
            return {
                "research_output": res_out,
                "iterations": state.get("iterations", 0) + 1
            }
        except Exception as e:
            if "503" in str(e) and retry < 2:
                time.sleep(5)
                continue
            raise e

def call_reviewer(state: AgentState):
    print("--- REVIEWING REPORT ---")
    rev_out = review_executor.invoke({"input": state["research_output"]})["output"]
    return {"review_feedback": rev_out}

def router(state: AgentState):
    feedback = state["review_feedback"].upper()
    if "PASS" in feedback or state["iterations"] >= state["max_iterations"]:
        return "end"
    else:
        print(f"❌ Review failed. Feedback: {state['review_feedback']}")
        return "continue"


workflow = StateGraph(AgentState)

workflow.add_node("researcher", call_researcher)
workflow.add_node("reviewer", call_reviewer)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "reviewer")

workflow.add_conditional_edges(
    "reviewer",
    router,
    {
        "continue": "researcher",
        "end": END
    }
)

app = workflow.compile()


def run_financial_system(user_query):
    initial_state = {
        "input": user_query,
        "max_iterations": 3,
        "iterations": 0,
        "review_feedback": "None"
    }
    
    final_output = app.invoke(initial_state)
    
    report = final_output["research_output"]
    if "PASS" not in final_output["review_feedback"].upper():
        return f"⚠️ Note: Max iterations reached without a full PASS.\n\n{report}"
    return report

if __name__ == "__main__":
    query = input("\n💬 What financial query do you have today?\n> ")
    if query.strip():
        print(run_financial_system(query))