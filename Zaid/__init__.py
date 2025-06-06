import time
from datetime import datetime
import asyncio
from aiohttp import ClientSession
from pyrogram import Client
from config import (
    API_ID, API_HASH, SUDO_USERS, OWNER_ID, BOT_TOKEN,
    STRING_SESSION1, STRING_SESSION2, STRING_SESSION3, STRING_SESSION4,
    STRING_SESSION5, STRING_SESSION6, STRING_SESSION7, STRING_SESSION8,
    STRING_SESSION9, STRING_SESSION10
)

# Global variables
StartTime = time.time()
START_TIME = datetime.now()
CMD_HELP = {}
clients = []
ids = []
aiosession = None

# Ensure OWNER is included in SUDO_USERS
SUDO_USERS = list(set(SUDO_USERS + [OWNER_ID]))

# Fallback values
API_ID = API_ID or "23287799"
API_HASH = API_HASH or "9f4f17dae2181ee22c275b9b40a3c907"

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN is missing in config. Please provide it.")

# Strip any leading/trailing whitespace from session strings
session_strings = list(filter(None, [
    STRING_SESSION1.strip() if STRING_SESSION1 else None,
    STRING_SESSION2.strip() if STRING_SESSION2 else None,
    STRING_SESSION3.strip() if STRING_SESSION3 else None,
    STRING_SESSION4.strip() if STRING_SESSION4 else None,
    STRING_SESSION5.strip() if STRING_SESSION5 else None,
    STRING_SESSION6.strip() if STRING_SESSION6 else None,
    STRING_SESSION7.strip() if STRING_SESSION7 else None,
    STRING_SESSION8.strip() if STRING_SESSION8 else None,
    STRING_SESSION9.strip() if STRING_SESSION9 else None,
    STRING_SESSION10.strip() if STRING_SESSION10 else None,
]))

# Bot Client (main bot)
app = Client(
    name="app",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Zaid/modules/bot"),
    in_memory=True,
)

# User clients from session strings
for idx, session in enumerate(session_strings, 1):
    print(f"Client{idx}: Found.. Starting.. 📳")
    user_client = Client(
        name=f"user_{idx}",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session,
        plugins=dict(root="Zaid/modules")
    )
    clients.append(user_client)

# Create aiohttp session
async def create_aiosession():
    global aiosession
    if aiosession is None:
        aiosession = ClientSession()

# Start all clients
async def start_all():
    await create_aiosession()
    await app.start()
    print("✅ Bot client started.")

    for client in clients:
        await client.start()
        print(f"✅ {client.name} started.")

# Stop all clients
async def stop_all():
    await app.stop()
    for client in clients:
        await client.stop()
    if aiosession:
        await aiosession.close()
    print("🛑 All clients stopped.")

# Run everything
if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except KeyboardInterrupt:
        print("Interrupted. Shutting down...")
        asyncio.run(stop_all())
