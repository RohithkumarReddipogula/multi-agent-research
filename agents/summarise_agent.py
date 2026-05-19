from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import ResearchState
import logging
import os

logger = logging.getLogger(__name__)


def summarise_agent(state: ResearchState) -> ResearchState:
    """
    Agent 2 — Summarise Agent.
    Takes raw search results from Agent 1 and condenses them
    into structured key findings using Google Gemini.
    Temperature 0.3 for factual consistency.
    """
    question = state["question"]
    search_results = state.get("search_results", [])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        temperature=0.3,
    )

    results_text = "\n\n---\n\n".join(search_results)

    messages = [
        SystemMessage(content=(
            "You are a research summariser. Extract the most important "
            "information from web search results as clear structured key "
            "points. Be factual and concise. Do not add information not "
            "present in the sources."
        )),
        HumanMessage(content=(
            f"Research question: {question}\n\n"
            f"Search results:\n{results_text}\n\n"
            f"Provide:\n"
            f"1. 5 key findings\n"
            f"2. Important facts and figures\n"
            f"3. Any conflicting information found"
        )),
    ]

    try:
        response = llm.invoke(messages)
        logger.info("Summarise Agent: complete")
        return {**state, "summary": response.content}
    except Exception as e:
        logger.error(f"Summarise Agent error: {e}")
        return {**state, "summary": f"Failed: {str(e)}", "error": str(e)}
