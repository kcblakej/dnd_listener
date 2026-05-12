import asyncio
import os
from dotenv import load_dotenv
from listener import GameEventListener

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")


if __name__ == "__main__":
    listener = GameEventListener(server_url=SERVER_URL)
    asyncio.run(listener.run())
