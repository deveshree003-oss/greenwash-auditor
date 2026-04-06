from backend.app.agents.doc_agent import DocumentAgent
from backend.app.agents.csr_agent import CSRClaimAgent
from backend.app.agents.finance_agent import FinanceAgent
from backend.app.agents.reasoning_agent import ReasoningAgent
from backend.app.agents.scoring_agent import ScoringAgent
from backend.app.agents.legal_agent import LegalAgent
from backend.app.agents.news_agent import NewsAgent

class AuditOrchestrator:
    def run(self, csr_file, finance_file, company):

        doc = DocumentAgent()
        csr_agent = CSRClaimAgent()
        finance_agent = FinanceAgent()
        reasoning = ReasoningAgent()
        scoring = ScoringAgent()
        legal = LegalAgent()
        news_agent = NewsAgent()

        csr_text = doc.run(csr_file)
        fin_text = doc.run(finance_file)

        claims = csr_agent.run(csr_text)
        financials = finance_agent.run(fin_text)
        news = news_agent.run(company)

        contradictions = reasoning.run(claims, financials, news)

        # Normalize contradictions: reasoning.run may return a dict
        # containing 'consensus', 'groq', and 'together' keys. Ensure
        # downstream agents receive a list of contradiction dicts.
        if isinstance(contradictions, dict):
            contradictions_list = (
                contradictions.get("consensus")
                or contradictions.get("groq")
                or contradictions.get("together")
                or []
            )
        else:
            contradictions_list = contradictions or []

        score = scoring.run(contradictions_list)
        legal_report = legal.run(contradictions_list)

        return {
            "claims": claims,
            "financials": financials,
            "news": news,
            "contradictions": contradictions_list,
            "score": score,
            "legal": legal_report
        }