"""
Agent 1 — Search Agent.
Searches the web using DuckDuckGo and returns top 5 results.
No API key required — uses free DuckDuckGo search.
"""

from duckduckgo_search import DDGS
from graph.state import ResearchState
import logging

logger = logging.getLogger(__name__)


def search_agent(state: ResearchState) -> ResearchState:
    """
    Searches the web for information about the research question.
    Returns top 5 results as formatted text for the Summarise Agent.
    """
    question = state["question"]
    logger.info(f"Search Agent: searching for '{question}'")

    try:
        results = []
        with DDGS() as ddgs:
            search_results = list(ddgs.text(question, max_results=5))

        for r in search_results:
            result_text = f"Source: {r.get('href', 'Unknown')}\n"
            result_text += f"Title: {r.get('title', 'No title')}\n"
            result_text += f"Content: {r.get('body', 'No content')}\n"
            results.append(result_text)

        logger.info(f"Search Agent: found {len(results)} results")
        return {**state, "search_results": results}

    except Exception as e:
        logger.error(f"Search Agent error: {e}")
        return {
            **state,
            "search_results": [f"Search failed: {str(e)}"],
            "error": str(e),
        }
