from backend.app.agents.csr_agent import CSRClaimAgent
from backend.app.agents.finance_agent import FinanceAgent
from backend.app.agents.news_agent import NewsAgent
from backend.app.agents.reasoning_agent import ReasoningAgent
from backend.app.agents.scoring_agent import ScoringAgent
from backend.app.agents.legal_agent import LegalAgent


def main():
    csr_text = (
        "Company X claims: We run on 100% renewable energy. "
        "We have invested in solar farms and purchase renewable certificates."
    )
    fin_text = (
        "Company X financials: revenue grew 10% year over year; "
        "energy costs down; capital investments in green projects."
    )
    company = "Company X"

    csr_agent = CSRClaimAgent()
    finance_agent = FinanceAgent()
    news_agent = NewsAgent()
    reasoning = ReasoningAgent()
    scoring = ScoringAgent()
    legal = LegalAgent()

    print('Running CSR agent...')
    claims = csr_agent.run(csr_text)
    print('Running Finance agent...')
    financials = finance_agent.run(fin_text)
    print('Running News agent...')
    news = news_agent.run(company)
    print('Running Reasoning agent... (this will call LLMs)')
    contradictions = reasoning.run(claims, financials, news)
    print('Running Scoring agent...')
    score = scoring.run(contradictions)
    print('Running Legal agent...')
    legal_report = legal.run(contradictions)

    print('\n--- RESULTS ---')
    print('claims:', claims)
    print('financials:', financials)
    print('news:', news)
    print('contradictions:', contradictions)
    print('score:', score)
    print('legal:', legal_report)


if __name__ == '__main__':
    main()
