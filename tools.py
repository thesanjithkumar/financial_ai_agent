from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import tool

search_wrapper = GoogleSearchAPIWrapper()

@tool
def search(query: str) -> str:
    """Search the web for real-time financial data, market trends, and retirement planning news."""
    return search_wrapper.run(query)