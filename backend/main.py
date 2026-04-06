from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict

# import agent classes from the package (absolute imports from backend root)
from backend.app.agents.doc_agent import DocumentAgent
from backend.app.agents.csr_agent import CSRClaimAgent
from backend.app.agents.finance_agent import FinanceAgent
from backend.app.agents.reasoning_agent import ReasoningAgent
from backend.app.agents.scoring_agent import ScoringAgent
from backend.app.agents.legal_agent import LegalAgent
from backend.app.agents.news_agent import NewsAgent

app = FastAPI(title="GreenTrace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "GreenTrace API is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


# include external API router
from backend.api.routes import router as api_router
app.include_router(api_router)


# instantiate lightweight agents (placeholders)
doc_agent = DocumentAgent()
csr_agent = CSRClaimAgent()
finance_agent = FinanceAgent()
reasoning_agent = ReasoningAgent()
scoring_agent = ScoringAgent()
legal_agent = LegalAgent()
news_agent = NewsAgent()


@app.get("/audit/{company_name}")
def audit_company(company_name: str) -> Dict[str, Any]:
    """Run a lightweight audit pipeline using the agent stubs.

    This is a placeholder wiring that calls each agent's public method
    and assembles the response. Replace agent internals with real
    implementations as available.
    """
    # placeholder pipeline using agent `run` methods; safe defaults used
    csr_text = ""
    fin_text = ""

    try:
        claims = csr_agent.run(csr_text)
    except Exception:
        claims = []

    try:
        financials = finance_agent.run(fin_text)
    except Exception:
        financials = {}

    try:
        news_hits = news_agent.run(company_name)
    except Exception:
        news_hits = []

    try:
        reasoning_result = reasoning_agent.run(claims, financials, news_hits)
        # reasoning_agent.run currently returns a dict containing
        # parsed outputs and a `consensus` list. ScoringAgent expects
        # a list of contradictions, so extract a list safely here.
        if isinstance(reasoning_result, dict):
            contradictions = (
                reasoning_result.get("consensus")
                or reasoning_result.get("groq")
                or reasoning_result.get("together")
                or []
            )
        else:
            contradictions = reasoning_result
    except Exception:
        contradictions = []

    try:
        score = scoring_agent.run(contradictions)
    except Exception:
        score = 0

    try:
        violations = legal_agent.run(contradictions)
    except Exception:
        violations = ""

    return {
        "company_name": company_name,
        "claims": claims,
        "financials": financials,
        "news_hits": news_hits,
        "contradictions": contradictions,
        "score": score,
        "violations": violations,
    }