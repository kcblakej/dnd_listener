# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Full stack (Docker Compose)
```bash
cd infra
docker compose up --build
```
Server: http://localhost:8000 | Viewer: http://localhost:3000

### Server (FastAPI)
```bash
cd server
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Client (listener)
```bash
cd client
pip install -r requirements.txt
cp .env.example .env   # set SERVER_URL
python src/main.py
```

### Viewer (React/Vite)
```bash
cd viewer
npm install
npm run dev   # proxies /events → localhost:8000
```

### Infrastructure (Terraform / GCP)
```bash
cd infra
terraform init
terraform plan -var="environment=dev"
terraform apply
```

## Architecture

Three decoupled services communicate in a unidirectional pipeline:

```
Client → POST /events/ → Server → SSE /events/stream → Viewer
```

**Client** (`client/src/listener.py`) — `GameEventListener` is an async base class with a `watch()` generator that must be overridden for each game source integration (e.g., VTT, audio transcription). It POSTs every yielded event dict to `SERVER_URL/events/`.

**Server** (`server/app/`) — FastAPI app. `POST /events/` accepts `GameEvent` payloads (type, source, payload, timestamp) and `GET /events/stream` is an SSE endpoint that the viewer subscribes to. Both endpoints are currently stubs in `routers/events.py` — the event bus / fan-out logic (in-memory queue, Redis pub/sub, etc.) needs to be implemented there.

**Viewer** (`viewer/src/App.jsx`) — React SPA that opens an `EventSource` on `/events/stream` and renders incoming events. Vite dev server proxies `/events` to `localhost:8000`. Production build is served by nginx (see `viewer/Dockerfile`).

**Key data model** — `server/app/models/event.py::GameEvent`: `type`, `source`, `payload` (freeform dict), `timestamp`.

**Infra** — `infra/main.tf` targets GCP via Terraform (provider not yet wired). `infra/docker-compose.yml` is the local dev entrypoint for all three services.
