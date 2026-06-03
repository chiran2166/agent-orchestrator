# AI Agent Orchestrator

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DC382D?logo=redis&logoColor=white) ![Anthropic](https://img.shields.io/badge/Anthropic-191919?logo=anthropic&logoColor=white)

Multi-agent pipeline: a **planner** decomposes a goal into subtasks, **specialist agents** execute them, and a **supervisor** merges the outputs into one answer. Progress streams over a WebSocket. Reuses the ai_core foundation from the [AI SQL/Code Assistant](../ai-sql-assistant).

```
goal ─▶ planner ─▶ [research|code|sql|summarize agents] ─▶ supervisor ─▶ answer
                         (steps streamed live over /ws/run)
```

## Layout

```
agent-orchestrator/
├── orchestrator/
│   ├── ai_core.py     # shared AI layer (same as Project 1)
│   ├── planner.py     # goal -> JSON subtasks
│   ├── agents.py      # specialist agent registry
│   ├── supervisor.py  # merge/critique
│   ├── graph.py       # run engine (yields step events)
│   └── bus.py         # optional Redis run-log
└── api/main.py        # /health · /run · ws /ws/run
```

## What's wired vs. stubbed

- ✅ End-to-end plan → execute → synthesize pipeline (real LLM calls)
- ✅ WebSocket step streaming
- 🚧 Agents are single LLM calls — extend with real tools (web search, the SQL prompt from Project 1)
- 🚧 Redis is optional run persistence; grow it into a pub/sub bus for distributed agents

## Run

```bash
cp .env.example .env          # add ANTHROPIC_API_KEY
pip install -e ".[dev]"
uvicorn api.main:app --reload --port 8001
# or: docker compose up --build   (also starts Redis)

curl -s localhost:8001/run -H 'content-type: application/json' \
  -d '{"goal":"compare REST vs GraphQL and give a migration checklist"}'
```

## Deploy

Container + managed Redis (Upstash / Redis Cloud). Set ANTHROPIC_API_KEY.

## Env

| Variable | Required | Default |
|----------|----------|---------|
| ANTHROPIC_API_KEY | ✅ | — |
| ANTHROPIC_MODEL | — | claude-3-5-sonnet-latest (see https://docs.claude.com) |
| REDIS_URL | — | redis://localhost:6379/0 |
