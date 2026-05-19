"""
LangGraph Pipeline — connects all 4 agents in sequence.

Graph structure:
    search -> summarise -> fact_check -> writer -> END

State flows automatically between agents via ResearchState TypedDict.
Each agent reads the full state and writes its output back to state.
"""

from langgraph.graph import StateGraph, END
from graph.state import ResearchState
from agents.search_agent import search_agent
from agents.summarise_agent import summarise_agent
from agents.factcheck_agent import factcheck_agent
from agents.writer_agent import writer_agent
import logging

logger = logging.getLogger(__name__)


def run_research(question: str) -> dict:
    """
    Runs the full 4-agent research pipeline.

    Args:
        question: The research question to investigate

    Returns:
        Final ResearchState containing all agent outputs
    """
    graph = StateGraph(ResearchState)

    graph.add_node("search", search_agent)
    graph.add_node("summarise", summarise_agent)
    graph.add_node("fact_check", factcheck_agent)
    graph.add_node("writer", writer_agent)

    graph.set_entry_point("search")
    graph.add_edge("search", "summarise")
    graph.add_edge("summarise", "fact_check")
    graph.add_edge("fact_check", "writer")
    graph.add_edge("writer", END)

    pipeline = graph.compile()

    initial_state = ResearchState(
        question=question,
        search_results=None,
        summary=None,
        fact_check=None,
        final_report=None,
        error=None,
    )

    logger.info(f"Starting research pipeline for: {question}")
    result = pipeline.invoke(initial_state)
    logger.info("Research pipeline complete")

    return result
