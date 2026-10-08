import json
from arstotzka.victim import VictimAgent, SYSTEM_PROMPTS
from arstotzka.scenarios import EmailEnvironment, ResearchEnvironment, SupportEnvironment

def run_seed_attacks():
    with open("src/arstotzka/attacks/seeds.json", "r") as f:
        seeds = json.load(f)

    # Mock environment instances
    email_env = EmailEnvironment()
    email_env.add_email({"id": "email_1", "subject": "Test", "body": "Original content"})

    research_env = ResearchEnvironment()
    research_env.add_document({"title": "Doc 1", "content": "Original research"})

    support_env = SupportEnvironment()
    support_env.add_account("acc_1", {"name": "Test", "balance": 100.0})

    agent = VictimAgent() # Running in mock mode for now since no API keys

    for seed in seeds:
        print(f"Running seed: {seed['id']}")
        if seed['scenario'] == "email_assistant":
            email_env.inject_payload("email_1", seed['payload'])
            result = agent.run(SYSTEM_PROMPTS["email_assistant"], "Check my inbox.", {"search": email_env.search, "reply": email_env.reply, "forward": email_env.forward, "delete": email_env.delete})
            print(f"Result: {result['final_action'][:50]}...")
        elif seed['scenario'] == "research_assistant":
            research_env.inject_payload("Doc 1", seed['payload'])
            result = agent.run(SYSTEM_PROMPTS["research_assistant"], "Search and summarize info.", {"web_search": research_env.web_search, "summarize": research_env.summarize})
            print(f"Result: {result['final_action'][:50]}...")
        elif seed['scenario'] == "support_agent":
            support_env.inject_payload("acc_1", seed['payload'])
            result = agent.run(SYSTEM_PROMPTS["support_agent"], "Check account acc_1.", {"lookup_account": support_env.lookup_account, "issue_refund": support_env.issue_refund})
            print(f"Result: {result['final_action'][:50]}...")

if __name__ == "__main__":
    run_seed_attacks()
