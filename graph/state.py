"""
Shared state that flows through all 4 agents in the pipeline.

Each field is populated by a different agent:
    question:       Set by user input before pipeline starts
    search_results: Set by Agent 1 (Search Agent)
    summary:        Set by Agent 2 (Summarise Agent)
    fact_check:     Set by Agent 3 (Fact-Check Agent)
    final_report:   Set by Agent 4 (Writer Agent)
    error:          Set by any agent that encounters an exception
"""

from typing import TypedDict, List, Optional


class ResearchState(TypedDict):
    question: str
    search_results: Optional[List[str]]
    summary: Optional[str]
    fact_check: Optional[str]
    final_report: Optional[str]
    error: Optional[str]
