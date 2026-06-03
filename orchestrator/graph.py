"""Execution engine: plan -> run each agent -> supervise. Yields step events."""
from __future__ import annotations

from collections.abc import Iterator

from orchestrator.agents import run_agent
from orchestrator.planner import plan
from orchestrator.supervisor import synthesize


def run(goal: str) -> Iterator[dict]:
    """Yield event dicts so an API/UI can stream progress."""
    yield {"type": "plan_start", "goal": goal}
    subtasks = plan(goal)
    yield {"type": "plan", "subtasks": subtasks}

    results: list[dict] = []
    for st in subtasks:
        yield {"type": "agent_start", "id": st["id"], "agent": st["agent"], "task": st["task"]}
        output = run_agent(st["agent"], st["task"])
        record = {"agent": st["agent"], "task": st["task"], "output": output}
        results.append(record)
        yield {"type": "agent_done", "id": st["id"], **record}

    final = synthesize(goal, results)
    yield {"type": "final", "answer": final}
