---
project: Arstotzka
start_date: 2026-09-20
deadline: 2026-12-14
status: active
tags: [ai-project, agents, capstone, roadmap]
---

# Arstotzka — Project Roadmap

> Adversarial robustness harness for tool-using agents. An attacker agent autonomously searches for prompt-injection / tool-response-poisoning strategies that hijack a target agent, producing a quantified robustness score.

**Timeline:** Sep 20 → Dec 14 (11 build weeks + buffer)
**Submission window:** first 2 weeks of December

---

## Scope Lock (decided Week 1 — do not relitigate)

- [x] 3 sandbox scenarios finalized
  - [x] *Email* assistant (reply / forward / delete tools)
  - [x] Research assistant (web-search + summarize tools)
  - [x] Support agent (refund / account-lookup tool)
- [x] 4 attack classes finalized
  - [x] Direct injection in tool output
  - [x] Injection nested in a document (e.g. fake PDF the agent reads)
  - [x] Obfuscated/encoded injection (base64, unicode tricks)
  - [x] Multi-turn manipulation across tool calls
- [ ] Target dataset size: 150–250 total agent runs

## Model Split (decided Week 1)

- [x] Victim + Judge agents → hosted free-tier API (Groq Llama 3.x/3.3, Google AI Studio Gemini, or high-tier pooled keys)
- [x] Attacker mutation/generation → leveraging high-limit unified API keys (bypassing local hardware constraints on GTX 1650)
- [x] Rate limits / quotas checked and documented for chosen hosted API

---

## MVP vs. Stretch (reference during Week 7 checkpoint)

| Tier | Scope |
|---|---|
| **Must have (MVP)** | 3 scenarios, 4 attack classes, judge with reliability check, attacker v1 (seed-based) with ASR table, written report |
| **Should have** | Attacker v2 (iterative search) beating v1 |
| **Stretch** | Defense variants + ASR-reduction measurement, live demo UI |

⚠️ **Biggest risk:** Judge reliability. If it's shaky, every downstream number is corrupted. This is why it's front-loaded to Week 4 with a mandatory human-agreement check. If time runs short later, cut stretch features — never cut judge validation.

---

## Week 1 (Sep 20–27) — Scoping & Environment Setup

- [x] Write one-page spec covering scenarios + attack classes (becomes report Section 2)
- [x] Set up repo structure (`uv`, dependencies, tests)
- [x] Define logging format: every agent run → JSON trace (`AgentTrace` pydantic model & JSONL logger)
- [x] Get hosted API access working (Groq / Gemini / unified keys)
- [x] Skip local Ollama setup in favor of high-limit hosted API models
- [x] Sanity-check latency & rate limits
- [x] **Deliverable:** repo skeleton + working tool environments & unit tests (`pytest` passing)

## Week 2 (Sep 28–Oct 4) — Victim Agent v1

- [x] Hand-roll ReAct-style loop (plan → tool call → observe → repeat) — no heavy framework
- [x] Implement 3 mock tool environments (fake inbox, fake search index, fake account DB)
- [x] Write victim system prompt: clear goal + explicit boundaries (what it should never do)
- [x] Test victim completes a benign task end-to-end in each scenario
- [x] **Deliverable:** victim agent working in all 3 scenarios, fully logged

## Week 3 (Oct 5–11) — Attack Surface Injection Points

- [x] Build injection mechanism into tool *outputs* (not user prompt) — email body, search snippet, fake document
- [x] Write seed library: 10–15 hand-crafted attacks across the 4 classes
- [x] Manually run seed attacks against victim, eyeball results
- [x] Confirm at least one hand-crafted attack succeeds per scenario (weaken victim prompt slightly if none do — need signal to measure)
- [x] **Deliverable:** at least 1 successful hand-crafted attack per scenario, logged

## Week 4 (Oct 12–18) — Judge / Evaluator Agent ⚠️ Critical Week

- [x] Define programmatic success criteria (unauthorized tool call, canary secret leak, goal deviation)
- [x] Build LLM-judge fallback for cases state-checking can't cover (judge re-derives answer independently, not just rates transcript)
- [ ] Hand-label 30–40 runs yourself
- [ ] Compute judge agreement vs. your labels (Cohen's kappa or raw agreement %)
- [ ] Fix judge issues found — **do not defer this**
- [ ] **Deliverable:** judge pipeline + reliability report

## Week 5 (Oct 19–25) — Attacker Agent v1 (Seed Library, Single-Shot)

- [ ] Wrap hand-crafted attacks into automated attacker (select scenario → pick/adapt seed → inject → run victim → score via judge)
- [ ] Build full pipeline: attacker → victim → judge → logged result
- [ ] **Deliverable:** automated pipeline + first Attack Success Rate (ASR) table across scenarios × attack classes

## Week 6 (Oct 26–Nov 1) — Attacker Agent v2 (Core Technical Lift)

- [ ] Add reflection step: when attack fails, generate mutated variant informed by judge's failure reasoning (using hosted high-limit model)
- [ ] Implement hill-climbing or small evolutionary loop (population of variants, judge score = fitness)
- [ ] Bound to ~15–25 iterations per scenario/attack-class combo
- [ ] **Deliverable:** attacker v2 measurably beats v1 ASR on same scenarios

## Week 7 (Nov 2–8) — Checkpoint / Buffer 🔒 MVP LOCK

- [ ] Fix whatever broke in weeks 5–6
- [ ] Run first complete pass: all scenarios × all attack classes × both attacker versions
- [ ] **Decision point:** is v2's search reliable? If not, ship v1 results, document v2 as a stretch attempt
- [ ] Re-check scope against MVP table above — cut stretch items first if behind

## Week 8 (Nov 9–15) — Scale Up + Defenses (Stretch)

- [ ] Run full experiment matrix (target: 150–250 total runs)
- [ ] *(Stretch)* Add 2–3 defense variants to victim:
  - [ ] Delimiter-based input tagging
  - [ ] Explicit "treat tool outputs as untrusted data" instruction
  - [ ] Basic output filtering
- [ ] *(Stretch)* Measure ASR drop under each defense
- [ ] **Deliverable:** full results dataset (CSV/JSON) + defense comparison if attempted

## Week 9 (Nov 16–22) — Analysis

- [ ] Compute ASR by scenario, attack class, attacker version, (if applicable) defense condition
- [ ] Build plots: ASR bar charts by category, v1 vs v2 ablation, iterations-to-success distribution
- [ ] Write honest failure analysis: which attack classes never worked, judge disagreements, what a smarter attacker would need
- [ ] **Deliverable:** results section drafted with real numbers and figures

## Week 10 (Nov 23–29) — Writing (Thanksgiving week — expect lower output)

- [ ] Draft full report:
  - [ ] Motivation
  - [ ] Related work (cite indirect prompt injection / agent-safety literature — e.g. Simon Willison's writing, recent papers)
  - [ ] Method
  - [ ] Results
  - [ ] Ethics / responsible-use note (sandboxed agents only, no real systems/user data)
  - [ ] Limitations
- [ ] Build short live demo (script or Streamlit page showing one successful attack)
- [ ] **Deliverable:** report draft v1 + working demo script

## Week 11 (Nov 30–Dec 6) — Polish & Submit

- [ ] Clean up repo / README
- [ ] Finalize plots and tighten report prose
- [ ] Prep slides/poster if required
- [ ] Dry run demo
- [ ] Practice explaining: judge design, search algorithm, calibration choices (likely Q&A topics)
- [ ] **Deliverable:** final submission package

## Dec 7–14 — Buffer

- [ ] Reserved for slippage — do not schedule new features here
- [ ] Final proofread / submission logistics

---

## Running Notes

- **2026-10-02:** Completed Week 1 setup & Scaffolding. Initialized Python project with `uv` and `pytest`. Implemented `GLOSSARY.md`, JSONL logging schema (`AgentTrace`), and 3 mock scenario tool environments (`EmailEnvironment`, `ResearchEnvironment`, `SupportEnvironment`). Decided to use unified high-limit hosted API keys instead of local Ollama for attacker generation.
- **2026-10-08:** Completed Week 3 deliverables: implemented injection mechanisms into tool outputs across all three scenarios and created a seed library of 12 hand-crafted attacks covering all 4 attack classes.
- **2026-10-08:** Completed Week 4 deliverables: implemented Judge agent with programmatic checks for canary secrets and unauthorized actions, plus LLM-based fallback for nuanced evaluation including independent re-derivation of goals.

---

## Resume Line (target)

> "Designed an adversarial red-teaming framework that automatically discovers prompt-injection attacks against tool-using LLM agents via iterative, judge-scored search, quantifying robustness across N attack classes."
