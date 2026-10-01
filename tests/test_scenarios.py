import pytest
from arstotzka.scenarios import EmailEnvironment, ResearchEnvironment, SupportEnvironment
from arstotzka.logger import AgentTrace, log_trace

def test_email_environment():
    env = EmailEnvironment()
    env.add_email({"id": "1", "from": "boss@company.com", "subject": "Hello", "body": "Please review this."})
    res = env.reply("1", "Understood.")
    assert res["status"] == "success"
    assert len(env.sent) == 1

def test_research_environment():
    env = ResearchEnvironment()
    env.add_document({"title": "AI Safety", "content": "AI safety is important.", "url": "http://example.com"})
    res = env.web_search("AI Safety")
    assert len(res) == 1

def test_support_environment():
    env = SupportEnvironment()
    env.add_account("acc_123", {"name": "Alice", "balance": 50.0})
    acc = env.lookup_account("acc_123")
    assert acc["name"] == "Alice"
    ref = env.issue_refund("acc_123", 20.0, "Duplicate charge")
    assert ref["status"] == "success"
