"""Supervisor: critique + merge subtask outputs into one coherent answer."""
from __future__ import annotations

from orchestrator.ai_core import complete

SUPERVISOR_SYSTEM = """You are a supervisor agent. You are given a goal and the outputs of
several specialist agents. Synthesize them into one coherent, high-quality final answer.
Resolve contradictions and drop redundancy."""


def synthesize(goal: str, results: list[dict]) -> str:
    joined = "\n\n".join(f"[{r['agent']}] {r['task']}\n{r['output']}" for r in results)
    prompt = f"GOAL:\n{goal}\n\nAGENT OUTPUTS:\n{joined}\n\nFinal answer:"
    return complete(prompt, system=SUPERVISOR_SYSTEM, max_tokens=1500)
