from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import events

app = FastAPI(title="DnD Listener API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router, prefix="/events", tags=["events"])


@app.get("/health")
async def health():
    return {"status": "ok"}
