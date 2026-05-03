import os
from dotenv import load_dotenv
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import tool

load_dotenv()

search_wrapper = GoogleSearchAPIWrapper(
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    google_cse_id=os.getenv("GOOGLE_CSE_ID")
)

@tool
def search(query: str) -> str:
    """Search the web for real-time financial data, market trends, and retirement planning news."""
    return search_wrapper.run(query)