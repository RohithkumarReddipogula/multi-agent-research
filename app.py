import streamlit as st
import os
import time
import logging
from graph.pipeline import run_research

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
)

st.title("Multi-Agent Research System")
st.markdown("**4 AI Agents Collaborating to Research Any Topic**")
st.markdown("*Built by Rohith Kumar Reddipogula | MSc Data Science | Berlin*")
st.markdown("---")

with st.sidebar:
    st.markdown("### How It Works")
    st.markdown("""
**4 Agents in sequence:**

1. **Search Agent**
   Searches web with DuckDuckGo

2. **Summarise Agent**
   Condenses results using Gemini

3. **Fact-Check Agent**
   Verifies reliability of findings

4. **Writer Agent**
   Produces final structured report
    """)
    st.markdown("---")
    st.markdown("**Portfolio:**")
    st.markdown(
        "[RAG Demo](https://rohith2026-hybrid-rag-demo.hf.space) | "
        "[AI Agent](https://rohith2026-ai-agent-react.hf.space) | "
        "[GitHub](https://github.com/RohithkumarReddipogula)"
    )

google_api_key = os.environ.get("GOOGLE_API_KEY")
if not google_api_key:
    st.error("GOOGLE_API_KEY not found. Please set it in your environment.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = google_api_key

examples = [
    "What is Retrieval-Augmented Generation and why is it important in 2026?",
    "What are the latest developments in LLM fine-tuning techniques?",
    "How does Kubernetes help with ML model deployment?",
    "What is the difference between LangChain and LangGraph?",
    "What are the best practices for LLM evaluation in production?",
]

st.markdown("### Ask Any Research Question")

selected = st.selectbox(
    "Example questions to try:",
    ["-- Select an example --"] + examples,
)

question = st.text_area(
    "Your research question:",
    value=selected if selected != "-- Select an example --" else "",
    placeholder="Enter any question you want researched...",
    height=80,
)

research_button = st.button(
    "Research This Question",
    type="primary",
    use_container_width=True,
)

if research_button and question.strip():
    st.markdown("---")
    st.markdown("## Research in Progress")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        s1 = st.empty()
    with col2:
        s2 = st.empty()
    with col3:
        s3 = st.empty()
    with col4:
        s4 = st.empty()

    s1.info("Agent 1: Searching...")
    s2.info("Agent 2: Waiting...")
    s3.info("Agent 3: Waiting...")
    s4.info("Agent 4: Waiting...")

    start_time = time.time()

    try:
        result = run_research(question)
        elapsed = time.time() - start_time

        s1.success("Agent 1: Done")
        s2.success("Agent 2: Done")
        s3.success("Agent 3: Done")
        s4.success("Agent 4: Done")

        st.markdown(f"*Completed in {elapsed:.1f} seconds*")
        st.markdown("---")
        st.markdown("## Final Research Report")
        st.markdown(result.get("final_report", "No report generated"))
        st.markdown("---")

        with st.expander("Agent 1 — Raw Search Results"):
            for i, r in enumerate(result.get("search_results", []), 1):
                st.markdown(f"**Result {i}:**")
                st.text(r)

        with st.expander("Agent 2 — Summary"):
            st.markdown(result.get("summary", "No summary"))

        with st.expander("Agent 3 — Fact-Check"):
            st.markdown(result.get("fact_check", "No fact-check"))

    except Exception as e:
        s1.error("Error")
        st.error(f"Error: {str(e)}")
        st.info("If quota error — wait 60 seconds and try again.")

elif research_button:
    st.warning("Please enter a research question.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:gray;font-size:12px'>"
    "Built by <b>Rohith Kumar Reddipogula</b> | MSc Data Science | Berlin<br>"
    "Stack: LangGraph · Google Gemini · DuckDuckGo · Streamlit · HuggingFace"
    "</div>",
    unsafe_allow_html=True,
)
