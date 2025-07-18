import asyncio
from SUHANIMUSIC import app
from config import OWNER_ID
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from SUHANIMUSIC.utils.database import get_assistant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Assuming Userbot is defined elsewhere

last_checked_time = None

BOT_LIST = ["Venom_X_Music_bot","Suhani_X_Music_bot"]


@app.on_message(filters.command("botschk") & filters.user(OWNER_ID))
async def bots_chk(_, message):
    global last_checked_time

    # Start the Pyrogram client
    userbot = await get_assistant(message.chat.id)

    # Get current time before sending messages
    start_time = datetime.now()

    msg = await message.reply_photo(photo="https://telegra.ph/file/4d303296e4fac9a40ea07.jpg", caption="**ᴄʜᴇᴄᴋɪɴɢ ʙᴏᴛs sᴛᴀᴛs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ...**")
    response = "**ᴄʜᴇᴄᴋɪɴɢ ʙᴏᴛs sᴛᴀᴛs ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ**\n\n"
    for bot_username in BOT_LIST:
        try:
            bot = await app.get_users(bot_username)
            bot_id = bot.id
            await asyncio.sleep(2)
            await userbot.send_message(bot_id, "/start")
            await asyncio.sleep(5)
            async for bot_message in userbot.get_chat_history(bot_id, limit=1):
                if bot_message.from_user.id == bot_id:
                    response += f"╭⎋ {bot.mention}\n╰⊚ **sᴛᴀᴛᴜs: ᴏɴʟɪɴᴇ ✨**\n\n"
                else:
                    response += f"╭⎋ {bot.mention}\n╰⊚ **sᴛᴀᴛᴜs: ᴏғғʟɪɴᴇ ❄**\n\n"
        except Exception:
            response += f"╭⎋ {bot_username}\n╰⊚ **sᴛᴀᴛᴜs: ᴇʀʀᴏʀ ❌**\n\n"

        # Update last checked time
        last_checked_time = start_time.strftime("%d-%m-%Y")
    
    await msg.edit_text(f"{response}⏲️ ʟᴀsᴛ ᴄʜᴇᴄᴋ: {last_checked_time}")
                