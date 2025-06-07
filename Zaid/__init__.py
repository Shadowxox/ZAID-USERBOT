import time
import asyncio
from datetime import datetime
from aiohttp import ClientSession
from pyrogram import Client
from config import (
    API_ID, API_HASH, SUDO_USERS, OWNER_ID, BOT_TOKEN,
    STRING_SESSION1, STRING_SESSION2, STRING_SESSION3, STRING_SESSION4,
    STRING_SESSION5, STRING_SESSION6, STRING_SESSION7, STRING_SESSION8,
    STRING_SESSION9, STRING_SESSION10
)

# ─── Globals ─────────────────────────────────────────────────────────
StartTime = time.time()
START_TIME = datetime.now()
CMD_HELP = {}
clients = []
ids = []
aiosession = None

# ─── SUDO Users ──────────────────────────────────────────────────────
SUDO_USERS = list(set(SUDO_USERS + [OWNER_ID]))
SUDO_USER = SUDO_USERS

# ─── Config Validation ───────────────────────────────────────────────
if not API_ID or not API_HASH or not BOT_TOKEN:
    raise RuntimeError("❌ Missing API_ID, API_HASH, or BOT_TOKEN in config!")

# ─── Fallback Defaults (Optional) ────────────────────────────────────
API_ID = API_ID or "23287799"
API_HASH = API_HASH or "9f4f17dae2181ee22c275b9b40a3c907"

# ─── User Session Strings ────────────────────────────────────────────
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

# ─── Main Bot Client ────────────────────────────────────────────────
app = Client(
    name="app",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="Zaid/modules/bot"),
    in_memory=True,
)

# ─── Create User Clients ─────────────────────────────────────────────
for idx, session in enumerate(session_strings, 1):
    print(f"Client{idx}: Found.. Starting.. 📳")
    user_client = Client(
        name=f"user_{idx}",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session,
        plugins=dict(root="Zaid/modules"),
    )
    clients.append(user_client)

# ─── aiohttp Session ────────────────────────────────────────────────
async def create_aiosession():
    global aiosession
    if aiosession is None:
        aiosession = ClientSession()

# ─── Start All Clients ───────────────────────────────────────────────
async def start_all():
    await create_aiosession()
    await app.start()
    print("✅ Main bot started.")

    for client in clients:
        await client.start()
        print(f"✅ {client.name} started.")

# ─── Stop All Clients ────────────────────────────────────────────────
async def stop_all():
    print("🛑 Shutting down...")
    await app.stop()
    for client in clients:
        await client.stop()
    if aiosession:
        await aiosession.close()
    print("✅ All clients stopped cleanly.")

# ─── Main Runner ─────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except KeyboardInterrupt:
        print("❗ Keyboard Interrupt received.")
        # Use a new event loop to stop safely
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(stop_all())
