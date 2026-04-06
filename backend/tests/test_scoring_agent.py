import pytest

from backend.app.agents.scoring_agent import ScoringAgent


def test_scoring_with_list_of_dicts():
    agent = ScoringAgent()
    contradictions = [
        {"severity": "High"},
        {"severity": "Medium"},
        {"severity": "Low"},
    ]

    score = agent.run(contradictions)
    # High=30, Medium=15, Low=5 => total 50
    assert score == 50


def test_scoring_with_dict_shape():
    agent = ScoringAgent()
    # dict returned by reasoning with consensus list
    contradictions = {"consensus": [{"severity": "High"}, {"severity": "High"}]}

    score = agent.run(contradictions)
    # 2 * High = 60
    assert score == 60


def test_scoring_with_string_items():
    agent = ScoringAgent()
    contradictions = ["This is High severity issue", "medium risk noted"]

    score = agent.run(contradictions)
    # High -> 30, medium -> 15 => 45
    assert score == 45


def test_scoring_fallback_for_unexpected_input():
    agent = ScoringAgent()
    # e.g., None or unexpected object should return fallback 50
    assert agent.run(None) == 50
    assert agent.run(12345) == 50
