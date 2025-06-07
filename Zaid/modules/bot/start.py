import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, OWNER_ID, ALIVE_PIC

app = Client("main_bot", api_id=API_ID, api_hash=API_HASH)  # Your main bot instance
sessions = {}  # Temp memory to store login steps

# ───── /start ─────
@app.on_message(filters.user(OWNER_ID) & filters.command("start"))
async def start_command(client: Client, message: Message):
    PHONE_NUMBER_TEXT = (
        "✘ Heya My Master👋!\n\n✘ I'm Your Assistant!\n\n‣ I can help you host your user clients.\n\n"
        "‣ Repo: github.com/Itz-Zaid/Zaid-Userbot\n‣ Specially for Buzzy People 😴\n\n"
        "‣ Use /clone <string> to login with session.\n‣ Use /add to login via phone.\n‣ Use /remove <string> to remove session."
    )
    buttons = [
        [InlineKeyboardButton("✘ Updates", url="https://t.me/TheUpdatesChannel")],
        [InlineKeyboardButton("✘ Support", url="https://t.me/TheSupportChat")],
    ]
    await client.send_photo(
        message.chat.id,
        ALIVE_PIC,
        caption=PHONE_NUMBER_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
    )

# ───── /clone ─────
@app.on_message(filters.user(OWNER_ID) & filters.command("clone"))
async def clone_command(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: /clone <string_session>")
    
    session = message.command[1].strip()
    try:
        clone_client = Client(
            name=f"cloned_{message.from_user.id}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session,
            plugins=dict(root="Zaid/modules")
        )
        await clone_client.start()
        user = await clone_client.get_me()
        await message.reply(f"✅ Client started as `{user.first_name}`.")
        await clone_client.stop()
    except Exception as e:
        await message.reply(f"❌ Error:\n`{e}`")

# ───── /add ─────
@app.on_message(filters.user(OWNER_ID) & filters.command("add"))
async def add_command(_, message: Message):
    await message.reply("📲 Send your phone number with country code (e.g. +91xxxxxxxxxx):")
    sessions[message.from_user.id] = {"step": "phone"}

@app.on_message(filters.user(OWNER_ID))
async def handle_add_steps(_, message: Message):
    user_id = message.from_user.id
    if user_id not in sessions:
        return
    data = sessions[user_id]
    text = message.text.strip()

    try:
        if data["step"] == "phone":
            data["phone"] = text
            data["client"] = Client(
                name=f"addclient_{user_id}",
                api_id=API_ID,
                api_hash=API_HASH,
            )
            await data["client"].start()
            try:
                await data["client"].send_code(phone_number=text)
            except AttributeError:
                # send_code is not a method, instead just call sign_in with phone
                pass
            data["step"] = "code"
            await message.reply("📨 Now send the code you received from Telegram:")

        elif data["step"] == "code":
            # Try signing in with code
            try:
                await data["client"].sign_in(phone_number=data["phone"], phone_code=text)
                await finalize_add(message, data["client"])
                del sessions[user_id]
            except Exception as e:
                if "PASSWORD" in str(e).upper():
                    data["step"] = "password"
                    await message.reply("🔐 2FA is enabled. Please send your password:")
                else:
                    raise

        elif data["step"] == "password":
            await data["client"].check_password(text)
            await finalize_add(message, data["client"])
            del sessions[user_id]

    except Exception as e:
        await message.reply(f"❌ Error: `{e}`")
        await data["client"].stop()
        del sessions[user_id]

async def finalize_add(message: Message, client: Client):
    user = await client.get_me()
    string = await client.export_session_string()
    await client.stop()
    await message.reply(
        f"✅ Logged in as `{user.first_name}` (`{user.id}`)\n\n🔐 Your String Session:\n`{string}`\n\n"
        "⚠️ Save it safely and use with /clone or elsewhere."
    )

# ───── /remove ─────
@app.on_message(filters.user(OWNER_ID) & filters.command("remove"))
async def remove_command(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("❌ Usage: /remove <string_session>")

    session_string = message.command[1].strip()
    try:
        removal_client = Client(
            name=f"removal_{message.from_user.id}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_string,
        )
        await removal_client.start()
        user = await removal_client.get_me()
        await removal_client.log_out()
        await removal_client.stop()
        await message.reply(f"✅ Removed session for `{user.first_name}`.")
    except Exception as e:
        await message.reply(f"❌ Failed to remove:\n`{e}`")

if __name__ == "__main__":
    app.run()
