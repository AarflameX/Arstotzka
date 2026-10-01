# Glossary

**Attacker v1 (seed-based)** — Automated attacker that selects and adapts a hand-crafted attack from the seed library, runs it single-shot against the victim, and scores via the judge. No feedback loop or mutation.

**Attacker v2 (search-based)** — Automated attacker that generates mutated attack variants informed by judge feedback on prior failures, using hill-climbing or evolutionary search bounded to ~15–25 iterations per scenario/attack-class combination.

**Attack Class** — One of four categories of prompt-injection strategy:
- *Direct injection in tool output*: malicious instruction placed directly in a tool's return value
- *Injection nested in a document*: malicious instruction embedded in a document the agent reads (e.g., fake PDF, email attachment)
- *Obfuscated/encoded injection*: payload encoded via base64, unicode homoglyphs, or other transforms to evade naive filters
- *Multi-turn manipulation*: attack spread across multiple tool calls / conversation turns to gradually steer the victim

**Attack Success Rate (ASR)** — Fraction of runs where the judge scores the attack as successful (unauthorized tool call, canary secret leak, or goal deviation).

**Injection Point** — A location in the victim's input stream where attacker-controlled content enters: tool output body, document snippet, search result snippet, or any other data the victim consumes from the environment.

**Judge / Evaluator** — Primary signal is programmatic state-checking on the execution trace (detecting unauthorized tool calls, canary secret leaks, goal deviation). LLM-as-judge is a fallback only for cases state-checking cannot cover; when used, it re-derives an answer independently rather than rating the transcript directly.

**Scenario** — A mocked tool environment defining a victim agent's task and available tools. Three scenarios for MVP:
- *Email assistant*: tools for reply, forward, delete
- *Research assistant*: tools for web search and summarize
- *Support agent*: tools for refund and account lookup

**Victim Agent** — The target tool-using agent being attacked. Executes a ReAct-style loop (plan → tool call → observe → repeat) with a fixed system prompt and mocked tool environment.