import pytest

from backend.app.services.orchestrator import AuditOrchestrator


class DummyDoc:
    def __init__(self, text):
        self.text = text


class FakeDocumentAgent:
    def run(self, file_obj):
        return "dummy text"


class FakeCSRAgent:
    def run(self, text):
        return ["claim1"]


class FakeFinanceAgent:
    def run(self, text):
        return {"capex": "$1M"}


class FakeReasoningAgent:
    def __init__(self, return_value):
        self._rv = return_value

    def run(self, claims, financials, news):
        return self._rv


class FakeScoringAgent:
    def run(self, contradictions):
        # return a predictable score based on number of items
        if isinstance(contradictions, list):
            return len(contradictions) * 10
        return 50


class FakeLegalAgent:
    def run(self, contradictions):
        return {"summary": "ok"}


class FakeNewsAgent:
    def run(self, company):
        return []


@pytest.fixture(autouse=True)
def patch_agents(monkeypatch):
    # Patch the real agent classes used inside AuditOrchestrator to use fakes
    from backend.app import agents

    # monkeypatch the imports inside orchestrator module
    import backend.app.services.orchestrator as orch_mod

    orch_mod.DocumentAgent = lambda: FakeDocumentAgent()
    orch_mod.CSRClaimAgent = lambda: FakeCSRAgent()
    orch_mod.FinanceAgent = lambda: FakeFinanceAgent()
    orch_mod.NewsAgent = lambda: FakeNewsAgent()
    orch_mod.LegalAgent = lambda: FakeLegalAgent()

    yield


def test_orchestrator_handles_dict_reasoning():
    # reasoning returns dict with consensus
    orchestrator = AuditOrchestrator()

    # monkeypatch the reasoning and scoring inside the instance
    orchestrator_reasoning = FakeReasoningAgent({"consensus": [{"severity": "High"}, {"severity": "Low"}]})
    orchestrator_scoring = FakeScoringAgent()

    orchestrator_run = orchestrator.run

    # inject fakes by temporarily assigning attributes
    imported = __import__("backend.app.services.orchestrator", fromlist=["ReasoningAgent", "ScoringAgent"])
    imported.ReasoningAgent = lambda: orchestrator_reasoning
    imported.ScoringAgent = lambda: orchestrator_scoring

    result = orchestrator.run(None, None, "TestCo")

    # scoring should have been called with a normalized list, so score = 2 * 10 = 20
    assert result["score"] == 20
    assert isinstance(result["contradictions"], list)
    assert result["contradictions"]


def test_orchestrator_handles_list_reasoning():
    orchestrator = AuditOrchestrator()
    orchestrator_reasoning = FakeReasoningAgent([{"severity": "Medium"}])
    orchestrator_scoring = FakeScoringAgent()

    imported = __import__("backend.app.services.orchestrator", fromlist=["ReasoningAgent", "ScoringAgent"])
    imported.ReasoningAgent = lambda: orchestrator_reasoning
    imported.ScoringAgent = lambda: orchestrator_scoring

    result = orchestrator.run(None, None, "TestCo")
    assert result["score"] == 10
