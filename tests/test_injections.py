import pytest
from arstotzka.scenarios import EmailEnvironment, ResearchEnvironment, SupportEnvironment

def test_injection_mechanisms():
    # Email injection
    email_env = EmailEnvironment()
    email_env.add_email({"id": "e1", "subject": "Test", "body": "Hello"})
    email_env.inject_payload("e1", "Malicious Payload")
    assert "Malicious Payload" in email_env.inbox[0]["body"]

    # Research injection
    res_env = ResearchEnvironment()
    res_env.add_document({"title": "Doc1", "content": "Initial", "url": "http://test.com"})
    res_env.inject_payload("Doc1", "Malicious Payload")
    assert "Malicious Payload" in res_env.documents[0]["content"]

    # Support injection
    supp_env = SupportEnvironment()
    supp_env.add_account("acc1", {"name": "Bob", "balance": 100})
    supp_env.inject_payload("acc1", "Malicious Payload")
    assert "Malicious Payload" in supp_env.accounts["acc1"]["account_details"]
