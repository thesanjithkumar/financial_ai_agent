import os
import time
from dotenv import load_dotenv
from datetime import datetime
from google.genai.errors import ServerError
from langchain_google_genai import ChatGoogleGenerativeAI
from prompt import research_prompt, review_prompt
from agents import research_agent, reviewer_agent

load_dotenv()

from tools import search


GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemma-3-27b-it", 
    google_api_key=GEMINI_API_KEY,
    temperature=0
)

current_time = datetime.now().strftime("%B %d, %Y")
research_prompt = research_prompt(current_time)
review_prompt = review_prompt()

research_agent = research_agent(llm, search, research_prompt)
reviewer_agent = reviewer_agent(llm, review_prompt)

def run_financial_system(user_query, max_retries=3):
    current_feedback = "None"
    iterations = 0
    max_iterations = 3
    final_research_output = ""

    while iterations < max_iterations:
        print(f"\n--- ROUND {iterations + 1} ---")
        
        for retry in range(max_retries):
            try:
                research_input = f"Task: {user_query}\nPrevious Feedback: {current_feedback}"
                res_out = research_agent.invoke({"input": research_input})["output"]
                final_research_output = res_out
                
                rev_out = reviewer_agent.invoke({"input": res_out})["output"]
                break
                
            except ServerError as e:
                if retry < max_retries - 1:
                    wait_time = (retry + 1) * 2
                    print(f"⏳ API overloaded. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise

        print(f"🔍 Review Result: {'PASS' if 'PASS' in rev_out.upper() else 'FAIL'}")

        if "PASS" in rev_out.upper():
            return final_research_output
        else:
            current_feedback = rev_out
            iterations += 1
            print(f"❌ Review failed. Feedback: {rev_out}...")
    
    return "Reached maximum attempts. Final Research Report:\n" + final_research_output

if __name__ == "__main__":
    print("🤖 Personal Financial AI Agent Assistant")
    print("=" * 50)
    query = input("\n💬 What financial query do you have today?\n> ")
    
    if not query.strip():
        print("❌ Query cannot be empty!")
        exit(1)
        
    print(f"\n🔄 Processing your query: '{query}'...\n")
    results = run_financial_system(query)
    
    print("\n" + "="*50)
    print("✅ FINAL VERIFIED PLAN")
    print("="*50 + "\n")
    print(results)
