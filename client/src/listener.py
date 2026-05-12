import asyncio
import httpx
from typing import AsyncIterator


class GameEventListener:
    """Watches a game source and forwards events to the server."""

    def __init__(self, server_url: str):
        self.server_url = server_url

    async def watch(self) -> AsyncIterator[dict]:
        """Yield raw game events from the source. Override per integration."""
        raise NotImplementedError

    async def run(self):
        async with httpx.AsyncClient() as client:
            async for event in self.watch():
                await client.post(f"{self.server_url}/events/", json=event)
