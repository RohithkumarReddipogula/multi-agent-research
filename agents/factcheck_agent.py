from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from graph.state import ResearchState
import logging
import os

logger = logging.getLogger(__name__)


def factcheck_agent(state: ResearchState) -> ResearchState:
    """
    Agent 3 — Fact-Check Agent.
    Verifies the reliability of Agent 2 summary against original sources.
    Categorises claims as VERIFIED, UNCERTAIN, or MISSING.
    Temperature 0.1 for maximum precision and consistency.
    """
    question = state["question"]
    summary = state.get("summary", "")
    search_results = state.get("search_results", [])

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        temperature=0.1,
    )

    results_text = "\n\n".join(search_results[:3])

    messages = [
        SystemMessage(content=(
            "You are a fact-checker. Assess the reliability of research "
            "summaries. Be honest about uncertainty. Flag claims that are "
            "not well-supported by the original sources."
        )),
        HumanMessage(content=(
            f"Research question: {question}\n\n"
            f"Summary to verify:\n{summary}\n\n"
            f"Original sources:\n{results_text}\n\n"
            f"Provide:\n"
            f"VERIFIED: Claims supported by multiple sources\n"
            f"UNCERTAIN: Claims from single source or unclear\n"
            f"MISSING: Important information not found\n"
            f"CONFIDENCE: Overall confidence level High/Medium/Low with reason"
        )),
    ]

    try:
        response = llm.invoke(messages)
        logger.info("Fact-Check Agent: complete")
        return {**state, "fact_check": response.content}
    except Exception as e:
        logger.error(f"Fact-Check Agent error: {e}")
        return {**state, "fact_check": f"Failed: {str(e)}", "error": str(e)}
