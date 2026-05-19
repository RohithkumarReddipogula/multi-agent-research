# Multi-Agent Research System

A production-grade multi-agent AI pipeline where 4 specialised agents
collaborate to research any topic and produce a structured, fact-checked report.
Built with LangGraph for agent orchestration and Google Gemini as the judge LLM.

Live Demo: https://rohith2026-multi-agent-research.hf.space

---

## What This Project Does

Most AI assistants generate answers from training data alone. This system
does something different — it searches the live web, summarises findings,
verifies reliability, and writes a structured report. Four specialised agents
handle one step each, passing results through a LangGraph state graph.

This is the architecture pattern used in enterprise AI pipelines at companies
building serious LLM products.

---

## Architecture

    User Question
          |
          v
    +----------------------+
    | Agent 1: Search      |
    | DuckDuckGo web search|
    | Returns top 5 results|
    +----------------------+
          |
          v
    +----------------------+
    | Agent 2: Summarise   |
    | Gemini condenses     |
    | results into key     |
    | findings             |
    +----------------------+
          |
          v
    +----------------------+
    | Agent 3: Fact-Check  |
    | Verifies claims      |
    | Flags uncertainty    |
    | Scores confidence    |
    +----------------------+
          |
          v
    +----------------------+
    | Agent 4: Writer      |
    | Produces structured  |
    | research report      |
    +----------------------+
          |
          v
    Final Research Report
    - Executive Summary
    - Key Findings
    - Analysis
    - Confidence Assessment
    - Conclusion

---

## LangGraph State Flow

Each agent reads from and writes to a shared ResearchState object.
LangGraph manages state transitions automatically.

    ResearchState:
        question:       str          Set by user input
        search_results: List[str]    Set by Agent 1
        summary:        str          Set by Agent 2
        fact_check:     str          Set by Agent 3
        final_report:   str          Set by Agent 4

The graph is compiled once and invoked with the initial state.
This is the production pattern for stateful multi-agent systems.

---

## Project Structure

    multi-agent-research/
    |-- app.py                      Streamlit UI
    |-- requirements.txt            Python dependencies
    |-- Dockerfile                  Container configuration
    |-- agents/
    |   |-- __init__.py
    |   |-- search_agent.py         Agent 1 - web search
    |   |-- summarise_agent.py      Agent 2 - summarisation
    |   |-- factcheck_agent.py      Agent 3 - fact checking
    |   |-- writer_agent.py         Agent 4 - report writing
    |-- graph/
    |   |-- __init__.py
    |   |-- state.py                Shared ResearchState TypedDict
    |   |-- pipeline.py             LangGraph pipeline
    |-- .gitignore
    |-- LICENSE
    |-- README.md

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Agent orchestration | LangGraph | State graph and agent routing |
| Search | DuckDuckGo Search | Real-time web search, no API key needed |
| LLM | Google Gemini 2.0 Flash | Summarisation, fact-checking, writing |
| LLM framework | LangChain | LLM abstraction layer |
| UI | Streamlit | Interactive web interface |
| Deployment | HuggingFace Spaces + Docker | Public cloud hosting |
| Language | Python 3.11 | Core language |

---

## Why 4 Agents Instead of 1

A single LLM call could attempt all 4 tasks. Using 4 agents is better for
three reasons.

First, specialisation. Each agent has a focused system prompt for its task.
The fact-checker uses temperature 0.1 for precision. The writer uses 0.4
for readable prose. One agent cannot be optimal for both simultaneously.

Second, transparency. Each agent's output is stored separately in state.
Users can expand the intermediate results to see exactly what the search
found, how Gemini summarised it, and what the fact-check flagged. This
explainability is critical for trust in production AI systems.

Third, modularity. Any agent can be swapped independently. The search
agent could be replaced with a Bing or Google search API. The LLM agent
could switch from Gemini to Claude or GPT-4. The pipeline structure
remains identical.

---

## Agent Design Decisions

Search Agent uses DuckDuckGo because it requires no API key and returns
real-time results. The agent extracts title, URL, and body text for each
result and formats them for the next agent.

Summarise Agent uses temperature 0.3 for factual consistency while
allowing some paraphrasing. Higher temperature would introduce
hallucinations in the summary.

Fact-Check Agent uses temperature 0.1 — the lowest reasonable value.
Fact-checking requires precision and consistency. It categorises each
claim as VERIFIED, UNCERTAIN, or MISSING based on source support.

Writer Agent uses temperature 0.4 to balance readability with accuracy.
It receives both the summary and the fact-check assessment, so it knows
which claims to present with confidence versus caution.

---

## How to Run Locally

Clone the repository:

    git clone https://github.com/RohithkumarReddipogula/multi-agent-research
    cd multi-agent-research

Install dependencies:

    pip install -r requirements.txt

Set your Google API key:

    export GOOGLE_API_KEY=your_key_from_aistudio.google.com

Run the app:

    streamlit run app.py

---

## How to Deploy

Build and run with Docker:

    docker build -t multi-agent-research .
    docker run -p 7860:7860 -e GOOGLE_API_KEY=your_key multi-agent-research

Or deploy to HuggingFace Spaces:
- Create a new Space with Docker SDK
- Add GOOGLE_API_KEY as a secret in Space settings
- Push this repository

---

## What I Learned

The most important insight from building this system was about state
management in multi-agent pipelines. Each agent needs to receive all
previous context — not just the output of the agent immediately before it.
The Writer Agent needs both the summary AND the fact-check to write a
calibrated report. LangGraph's TypedDict state pattern handles this
elegantly because every agent has read access to everything.

The second insight was about temperature configuration. Running all agents
at the same temperature produces worse results than tuning each agent
for its specific task. A fact-checker at temperature 0.7 introduces
inconsistency. A writer at temperature 0.1 produces robotic prose.

The third insight was about failure handling. In a 4-agent pipeline,
one agent failing silently can corrupt all downstream outputs. Every
agent wraps its LLM call in a try-except and writes the error to state
rather than raising an exception. This means the pipeline always completes
and the user sees a meaningful error message rather than a crash.

---

## Related Projects

| Project | Description | Live |
|---------|-------------|------|
| [Hybrid RAG System](https://github.com/RohithkumarReddipogula/AI-Powered-Rag-System) | BM25 + dense · 93% Recall@10 · 8.84M passages | [Demo](https://rohith2026-hybrid-rag-demo.hf.space) |
| [AI Agent](https://github.com/RohithkumarReddipogula/ai-agent-project) | ReAct agent · LangGraph · 3 tools | [Demo](https://rohith2026-ai-agent-react.hf.space) |
| [LLM Fine-Tuning](https://github.com/RohithkumarReddipogula/llm-finetune-project) | QLoRA · TinyLlama 1.1B · HuggingFace | [Model](https://huggingface.co/Rohith2026/nlp-rag-expert) |
| [LLM Evaluation](https://github.com/RohithkumarReddipogula/llm-evaluation-project) | RAGAS · 5 metrics · Streamlit dashboard | [Dashboard](https://rohith2026-llm-evaluation-dashboard.hf.space) |
| [AWS EC2 Deployment](https://github.com/RohithkumarReddipogula/aws-deployment-project) | FastAPI · systemd · production | [API](http://3.71.32.203:8000/docs) |
| [Kubernetes Deployment](https://github.com/RohithkumarReddipogula/k8s-rag-deployment) | 2 replicas · rolling updates · health checks | GitHub |
| Multi-Agent Research (this) | 4 agents · LangGraph · Gemini | [Demo](https://rohith2026-multi-agent-research.hf.space) |

---

## Author

Rohith Kumar Reddipogula
MSc Data Science — University of Europe for Applied Sciences, Berlin

LinkedIn: https://linkedin.com/in/rohith-kumar-reddipogula-a6692030b
GitHub: https://github.com/RohithkumarReddipogula
HuggingFace: https://huggingface.co/Rohith2026
Email: rohithkumar336699@gmail.com
