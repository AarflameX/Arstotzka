# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

- **Project:** Arstotzka — Adversarial robustness harness for tool-using agents.
- **Language:** Python 3.14+
- **Dependency Manager:** `uv` (`pyproject.toml`)
- **Testing Framework:** `pytest` (run via `uv run pytest`)
- **Core Components:**
  - `src/arstotzka/scenarios/` — Mock tool environments (Email, Research, Support)
  - `src/arstotzka/victim.py` — Target tool-using agent (ReAct loop)
  - `src/arstotzka/logger.py` — JSONL trace logging (`AgentTrace`)
  - `GLOSSARY.md` — Domain vocabulary and canonical terms
  - `Arstotzka.md` — Complete project roadmap and weekly progress tracker

## Project facts

- **License:** GNU GPLv3 — all code contributed must be compatible with GPLv3.
- **Models:** Hosted API models (Groq / Gemini / unified high-limit tokens) for victim, attacker, and judge.
- **Development Status:** Week 1 complete (scaffolding, mock environments, logging, unit tests). Moving to Week 2 (Victim Agent v1 ReAct loop & tool-calling integration).
