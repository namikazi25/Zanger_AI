import os
import httpx
from typing import List, Dict, Any, Optional
from langchain_core.tools import BaseTool

BRAVE_API_URL = "https://api.search.brave.com/res/v1/web/search"

class BraveSearchTool(BaseTool):
    name: str = "brave_search"
    description: str = (
        "A wrapper around Brave Search API. "
        "Useful for when you need to answer questions about current events. "
        "Input should be a search query."
    )
    api_key: Optional[str] = None
    results_count: int = 5 # Default number of results, Brave API max is 20

    def __init__(self, api_key: Optional[str] = None, results_count: int = 5, **kwargs: Any):
        super().__init__(**kwargs)
        self.api_key = api_key or os.getenv("BRAVE_SEARCH_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Brave Search API key not found. "
                "Please set the BRAVE_SEARCH_API_KEY environment variable or pass it as an argument."
            )
        self.results_count = results_count

    def _run(self, query: str, **kwargs: Any) -> List[Dict[str, str]]:
        """Run the Brave search and return structured results."""
        if not query:
            raise ValueError("Query cannot be empty.")

        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key,
        }
        params = {
            "q": query,
            "count": self.results_count
        }

        try:
            with httpx.Client() as client:
                response = client.get(BRAVE_API_URL, headers=headers, params=params)
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
                results = response.json()
        except httpx.RequestError as e:
            return [{"error": f"HTTP Request failed: {e}"}]
        except Exception as e:
            return [{"error": f"An unexpected error occurred: {e}"}]

        # Process results
        processed_results = []
        if results.get("web") and results["web"].get("results"):
            for item in results["web"]["results"]:
                processed_results.append({
                    "title": item.get("title", "N/A"),
                    "url": item.get("url", "N/A"),
                    "snippet": item.get("description", "N/A") # Brave uses 'description' for snippet
                })
        
        if not processed_results and results.get("error"):
             return [{"error": f"API Error: {results.get('error')}"}]
        elif not processed_results:
            return [{"info": "No results found."}]

        return processed_results

    async def _arun(self, query: str, **kwargs: Any) -> List[Dict[str, str]]:
        """Run the Brave search asynchronously and return structured results."""
        if not query:
            raise ValueError("Query cannot be empty.")

        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key,
        }
        params = {
            "q": query,
            "count": self.results_count
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(BRAVE_API_URL, headers=headers, params=params)
                response.raise_for_status()
                results = response.json()
        except httpx.RequestError as e:
            return [{"error": f"HTTP Request failed: {e}"}]
        except Exception as e:
            return [{"error": f"An unexpected error occurred: {e}"}]

        processed_results = []
        if results.get("web") and results["web"].get("results"):
            for item in results["web"]["results"]:
                processed_results.append({
                    "title": item.get("title", "N/A"),
                    "url": item.get("url", "N/A"),
                    "snippet": item.get("description", "N/A")
                })
        
        if not processed_results and results.get("error"):
             return [{"error": f"API Error: {results.get('error')}"}]
        elif not processed_results:
            return [{"info": "No results found."}]

        return processed_results

# Example Usage (for testing purposes):
if __name__ == '__main__':
    import asyncio
    # Ensure BRAVE_SEARCH_API_KEY is set in your environment for this example to run
    if not os.getenv("BRAVE_SEARCH_API_KEY"):
        print("Please set the BRAVE_SEARCH_API_KEY environment variable to run this example.")
    else:
        search_tool = BraveSearchTool()
        
        # Synchronous test
        print("--- Synchronous Test ---")
        sync_results = search_tool._run("latest AI news")
        for res in sync_results:
            print(f"Title: {res.get('title')}\nURL: {res.get('url')}\nSnippet: {res.get('snippet')}\n")

        # Asynchronous test
        async def main_async():
            print("--- Asynchronous Test ---")
            async_results = await search_tool._arun("python programming best practices")
            for res in async_results:
                print(f"Title: {res.get('title')}\nURL: {res.get('url')}\nSnippet: {res.get('snippet')}\n")

        asyncio.run(main_async())