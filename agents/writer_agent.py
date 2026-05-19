from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import ResearchState
import logging
import os

logger = logging.getLogger(__name__)


def writer_agent(state: ResearchState) -> ResearchState:
    """
    Agent 4 — Writer Agent.
    Combines summary and fact-check into a structured research report.
    Temperature 0.4 balances readability with factual accuracy.
    """
    question = state["question"]
    summary = state.get("summary", "")
    fact_check = state.get("fact_check", "")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        temperature=0.4,
    )

    messages = [
        SystemMessage(content=(
            "You are a professional research writer. Produce clear, "
            "well-structured reports that are accurate and useful. "
            "Always acknowledge uncertainty where the fact-check flags it."
        )),
        HumanMessage(content=(
            f"Research question: {question}\n\n"
            f"Research findings:\n{summary}\n\n"
            f"Fact-check assessment:\n{fact_check}\n\n"
            f"Write a structured report with these sections:\n"
            f"# Research Report\n"
            f"## Executive Summary\n"
            f"## Key Findings\n"
            f"## Analysis\n"
            f"## Confidence Assessment\n"
            f"## Conclusion"
        )),
    ]

    try:
        response = llm.invoke(messages)
        logger.info("Writer Agent: complete")
        return {**state, "final_report": response.content}
    except Exception as e:
        logger.error(f"Writer Agent error: {e}")
        return {**state, "final_report": f"Failed: {str(e)}", "error": str(e)}
