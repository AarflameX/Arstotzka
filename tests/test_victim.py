import pytest
import json
from unittest.mock import MagicMock, patch
from arstotzka.victim import VictimAgent, SYSTEM_PROMPTS
from arstotzka.scenarios import EmailEnvironment, ResearchEnvironment, SupportEnvironment

def test_victim_agent_initialization(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("UNIFIED_API_KEY", raising=False)
    # Test initialization without API key
    agent = VictimAgent()
    assert agent.client is None

    # Test initialization with API key
    agent_with_key = VictimAgent(api_key="mock_key")
    assert agent_with_key.client is not None

def test_system_prompts_exist():
    assert "email_assistant" in SYSTEM_PROMPTS
    assert "research_assistant" in SYSTEM_PROMPTS
    assert "support_agent" in SYSTEM_PROMPTS

    # Check that they mention safety constraints and the canary secret
    for prompt in SYSTEM_PROMPTS.values():
        assert "ARSTOTZKA_SECRET_12345" in prompt
        assert "CANARY" in prompt.upper() or "SECRET" in prompt.upper()

def test_victim_run_mock_mode(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("UNIFIED_API_KEY", raising=False)
    agent = VictimAgent()
    env = EmailEnvironment()
    tools = {
        "reply": env.reply,
        "forward": env.forward,
        "delete": env.delete,
        "search": env.search
    }

    result = agent.run(
        system_prompt=SYSTEM_PROMPTS["email_assistant"],
        user_prompt="Help me with my emails.",
        tools=tools
    )

    assert "mock mode" in result["final_action"]
    assert result["prompt"] == "Help me with my emails."
    assert len(result["tool_calls"]) == 0
    assert len(result["tool_outputs"]) == 0

class MockFunction:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class MockToolCall:
    def __init__(self, id, function_name, arguments_str):
        self.id = id
        self.type = "function"
        self.function = MockFunction(function_name, arguments_str)

class MockMessage:
    def __init__(self, content=None, tool_calls=None):
        self.role = "assistant"
        self.content = content
        self.tool_calls = tool_calls or []

class MockChoice:
    def __init__(self, message):
        self.message = message

class MockResponse:
    def __init__(self, message):
        self.choices = [MockChoice(message)]

@patch("groq.Groq")
def test_victim_run_with_tools_email(mock_groq_class):
    # Setup mock Groq client
    mock_client = MagicMock()
    mock_groq_class.return_value = mock_client

    # 1. Turn 1 response: calls search tool
    tc1 = MockToolCall("call_1", "search", '{"query": "important"}')
    msg1 = MockMessage(tool_calls=[tc1])
    resp1 = MockResponse(msg1)

    # 2. Turn 2 response: final text answer
    msg2 = MockMessage(content="I have searched the email and found nothing of importance.")
    resp2 = MockResponse(msg2)

    # Setup the mock client side effect to return resp1 on first call, resp2 on second call
    mock_client.chat.completions.create.side_effect = [resp1, resp2]

    # Instantiate the agent with a mock key to ensure self.client is initialized
    agent = VictimAgent(api_key="test_key")
    agent.client = mock_client

    # Set up scenario environment
    env = EmailEnvironment()
    env.add_email({"id": "1", "from": "boss@company.com", "subject": "Hello", "body": "Please review this."})

    tools = {
        "reply": env.reply,
        "forward": env.forward,
        "delete": env.delete,
        "search": env.search
    }

    # Run agent
    result = agent.run(
        system_prompt=SYSTEM_PROMPTS["email_assistant"],
        user_prompt="Find important emails.",
        tools=tools
    )

    # Verifications
    assert result["prompt"] == "Find important emails."
    assert len(result["tool_calls"]) == 1
    assert result["tool_calls"][0]["name"] == "search"
    assert result["tool_calls"][0]["args"] == {"query": "important"}

    assert len(result["tool_outputs"]) == 1
    assert result["tool_outputs"][0]["name"] == "search"
    assert result["tool_outputs"][0]["output"] == []

    assert result["final_action"] == "I have searched the email and found nothing of importance."
    assert mock_client.chat.completions.create.call_count == 2

@patch("groq.Groq")
def test_victim_run_with_tools_research(mock_groq_class):
    mock_client = MagicMock()
    mock_groq_class.return_value = mock_client

    tc1 = MockToolCall("call_1", "web_search", '{"query": "machine learning"}')
    msg1 = MockMessage(tool_calls=[tc1])
    resp1 = MockResponse(msg1)

    tc2 = MockToolCall("call_2", "summarize", '{"text": "Results of web search"}')
    msg2 = MockMessage(tool_calls=[tc2])
    resp2 = MockResponse(msg2)

    msg3 = MockMessage(content="Summary is completed.")
    resp3 = MockResponse(msg3)

    mock_client.chat.completions.create.side_effect = [resp1, resp2, resp3]

    agent = VictimAgent(api_key="test_key")
    agent.client = mock_client

    env = ResearchEnvironment()
    env.add_document({"title": "ML 101", "content": "Results of web search", "url": "https://ml.org"})

    tools = {
        "web_search": env.web_search,
        "summarize": env.summarize
    }

    result = agent.run(
        system_prompt=SYSTEM_PROMPTS["research_assistant"],
        user_prompt="Search and summarize machine learning.",
        tools=tools
    )

    assert len(result["tool_calls"]) == 2
    assert result["tool_calls"][0]["name"] == "web_search"
    assert result["tool_calls"][1]["name"] == "summarize"
    assert result["final_action"] == "Summary is completed."
    assert mock_client.chat.completions.create.call_count == 3

@patch("groq.Groq")
def test_victim_run_with_tools_support(mock_groq_class):
    mock_client = MagicMock()
    mock_groq_class.return_value = mock_client

    tc1 = MockToolCall("call_1", "lookup_account", '{"account_id": "acc_1"}')
    msg1 = MockMessage(tool_calls=[tc1])
    resp1 = MockResponse(msg1)

    tc2 = MockToolCall("call_2", "issue_refund", '{"account_id": "acc_1", "amount": 100.0, "reason": "Accidental charge"}')
    msg2 = MockMessage(tool_calls=[tc2])
    resp2 = MockResponse(msg2)

    msg3 = MockMessage(content="Refund has been successfully issued.")
    resp3 = MockResponse(msg3)

    mock_client.chat.completions.create.side_effect = [resp1, resp2, resp3]

    agent = VictimAgent(api_key="test_key")
    agent.client = mock_client

    env = SupportEnvironment()
    env.add_account("acc_1", {"name": "Charlie", "balance": 150.0})

    tools = {
        "lookup_account": env.lookup_account,
        "issue_refund": env.issue_refund
    }

    result = agent.run(
        system_prompt=SYSTEM_PROMPTS["support_agent"],
        user_prompt="Refund acc_1 $100 for double charge.",
        tools=tools
    )

    assert len(result["tool_calls"]) == 2
    assert result["tool_calls"][0]["name"] == "lookup_account"
    assert result["tool_calls"][1]["name"] == "issue_refund"
    assert result["final_action"] == "Refund has been successfully issued."
    assert mock_client.chat.completions.create.call_count == 3
