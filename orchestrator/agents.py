"""Specialist agents. Each takes a task string and returns a result string."""
from __future__ import annotations

from collections.abc import Callable

from orchestrator.ai_core import complete

SYSTEMS = {
    "research": "You are a research agent. Give a concise, factual brief on the task.",
    "code": "You are a coding agent. Return working code with a one-line explanation.",
    "sql": "You are a SQL agent. Return one correct, parameterized SQL query in a ```sql block.",
    "summarize": "You are a summarizer. Produce a tight, well-structured summary.",
}


def _make(system: str) -> Callable[[str], str]:
    return lambda task: complete(task, system=system)


AGENTS: dict[str, Callable[[str], str]] = {name: _make(sys) for name, sys in SYSTEMS.items()}


def run_agent(name: str, task: str) -> str:
    agent = AGENTS.get(name, AGENTS["summarize"])
    return agent(task)
