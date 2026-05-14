---
name: testing-dnd-listener-server
description: Test the DnD Listener FastAPI server end-to-end. Use when verifying server endpoints (REST, SSE, WebSocket).
---

# Testing the DnD Listener Server

## Local Dev Setup

```bash
cd server
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check: `curl http://localhost:8000/health` should return `{"status":"ok"}`.

## Architecture

The events router is mounted at `/events` (see `server/app/main.py`). Endpoints:
- `POST /events/` — accepts game event payloads
- `GET /events/stream` — SSE stream for the viewer
- `WS /events/ws` — WebSocket echo endpoint

## Testing WebSocket Endpoints

Install the `websockets` Python library (`pip install websockets`) and use it to connect programmatically:

```python
import asyncio, websockets

async def test():
    async with websockets.connect('ws://localhost:8000/events/ws') as ws:
        await ws.send('hello world')
        resp = await ws.recv()
        assert resp == 'hello world'

asyncio.run(test())
```

Key test scenarios for WebSocket endpoints:
1. **Basic echo** — send a message, verify exact response
2. **Sequential messages** — send multiple on the same connection, verify order
3. **Empty / special characters** — send edge-case strings (empty, unicode, emoji)
4. **Graceful disconnect** — close client, reconnect, verify server still works
5. **Path correctness** — verify the endpoint is only reachable at the correct path (e.g. `/events/ws` works, `/ws` does not)

All WebSocket tests are shell-based (no browser recording needed).

## Testing REST / SSE Endpoints

Use `curl` for REST endpoints:
```bash
curl -X POST http://localhost:8000/events/ -H 'Content-Type: application/json' -d '{...}'
curl -N http://localhost:8000/events/stream
```

Note: The POST and SSE endpoints may be stubs (`raise NotImplementedError`) — check the current implementation before testing.

## Devin Secrets Needed

None — the server runs locally without authentication.

## Notes

- The default branch is `master` (not `main`).
- No pre-commit hooks or linters are configured in the repo.
- The `websockets` package is not in `server/requirements.txt` — install it separately for testing.
