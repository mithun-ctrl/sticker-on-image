from pyrogram import Client, filters
from pyrogram.types import Message
import os

# Set up the Pyrogram client
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define a function to add a sticker to a message
async def add_sticker_to_message(message: Message, sticker_id: str):
    # Get the sticker from the Telegram API
    sticker = await app.get_sticker(sticker_id)
    
    # Add the sticker to the message
    await message.reply_sticker(sticker.file_id)

# Handle incoming messages
@app.on_message(filters.text)
async def handle_text(_, message: Message):
    # Add a sticker to the message
    await add_sticker_to_message(message, "CAACAgQAAxkBAAEHgLhjXTg4fQX7OOqh4Gfxx3NzGwABlgAC8wADXvCIHdJKJCVwMGVMHwQ")

if __name__ == "__main__":
    app.run()