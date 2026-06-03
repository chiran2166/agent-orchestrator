"""FastAPI surface: POST /run for one-shot, WS /ws/run for live step streaming."""
from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from orchestrator.graph import run

app = FastAPI(title="AI Agent Orchestrator", version="0.1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


class RunRequest(BaseModel):
    goal: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/run")
def run_once(req: RunRequest) -> dict:
    events = list(run(req.goal))
    return {"events": events, "answer": events[-1].get("answer", "")}


@app.websocket("/ws/run")
async def ws_run(ws: WebSocket) -> None:
    await ws.accept()
    try:
        goal = (await ws.receive_json()).get("goal", "")
        for event in run(goal):
            await ws.send_json(event)
        await ws.close()
    except WebSocketDisconnect:
        return
