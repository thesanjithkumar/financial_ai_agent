import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from tools import search
from prompt import research_prompt, review_prompt
from agents import research_agent, reviewer_agent

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.environ.get('GOOGLE_API_KEY')
os.environ["GOOGLE_CSE_ID"] = os.environ.get('GOOGLE_CSE_ID')

llm = ChatGoogleGenerativeAI(
    model="gemma-3-12b-it", 
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

research_prompt = research_prompt()
review_prompt = review_prompt()

research_agent = research_agent(llm, search, research_prompt)
reviewer_agent = reviewer_agent(llm, review_prompt)

def run_financial_system(user_query):
    current_feedback = "None"
    iterations = 0
    max_iterations = 3

    while iterations < max_iterations:
        print(f"\n--- ROUND {iterations + 1} ---")
        
        # Step 1: Research
        research_input = f"Task: {user_query}\nPrevious Feedback: {current_feedback}"
        res_out = research_agent.invoke({"input": research_input})["output"]

        # Step 2: Review
        rev_out = reviewer_agent.invoke({"input": res_out})["output"]

        if "PASS" in rev_out.upper():
            return rev_out.replace("PASS", "").strip()
        else:
            current_feedback = rev_out
            iterations += 1
    
    return "Reached maximum attempts. Final Draft:\n" + res_out

if __name__ == "__main__":
    query = (
        "I'm a 23-year-old software engineer with 41k monthly salary. "
        "I want to retire at 50, don't own property, and want to build a large home."
    )
    results = run_financial_system(query)
    print("\n" + "="*30 + "\nFINAL VERIFIED PLAN:\n" + "="*30 + "\n", results)