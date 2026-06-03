"""Planner: turn a high-level goal into an ordered list of subtasks."""
from __future__ import annotations

import json

from orchestrator.ai_core import complete

PLANNER_SYSTEM = """You are a planning agent. Break the user's goal into 2-5 concrete subtasks.
Return ONLY a JSON array of objects: [{"id": 1, "agent": "research|code|sql|summarize", "task": "..."}].
No prose, no markdown fences."""


def plan(goal: str) -> list[dict]:
    raw = complete(goal, system=PLANNER_SYSTEM)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: a single summarize task so the pipeline still completes.
        return [{"id": 1, "agent": "summarize", "task": goal}]
