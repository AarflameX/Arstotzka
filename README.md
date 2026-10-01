# Arstotzka

> Adversarial robustness harness for tool-using agents. An attacker agent autonomously searches for prompt-injection and tool-response-poisoning strategies that hijack a target agent, producing a quantified robustness score.

## Project Setup & Running Tests

This project uses Python and [uv](https://github.com/astral-sh/uv) for dependency management and package building.

```bash
# Run tests
uv run pytest
```

## Structure

- `src/arstotzka/scenarios/` — Mock tool environments (email, research, support)
- `src/arstotzka/victim.py` — Target tool-using agent
- `src/arstotzka/logger.py` — JSON trace logging schema
- `GLOSSARY.md` — Domain glossary
- `tests/` — Test suite
