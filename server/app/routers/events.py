from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/stream")
async def stream_events():
    """SSE endpoint — viewer subscribes here for live events."""
    raise NotImplementedError


@router.post("/")
async def post_event(payload: dict):
    """Client posts game events here."""
    raise NotImplementedError
