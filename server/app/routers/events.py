from fastapi import APIRouter, WebSocket, WebSocketDisconnect
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


@router.websocket("/ws")
async def websocket_echo(websocket: WebSocket):
    """WebSocket endpoint that echoes back any text message it receives."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        pass
