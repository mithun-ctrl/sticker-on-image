from pyrogram import Client, filters
from pyrogram.types import Message
import os

# Set up the Pyrogram client
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define a function to add a sticker to an image
async def add_sticker_to_image(message: Message, sticker_id: str):
    # Download the user's image
    image = await message.download()
    
    # Get the sticker from the Telegram API
    sticker = await app.get_sticker(sticker_id)
    
    # Add the sticker to the image
    await app.add_sticker_to_photo(image, sticker.file_id)
    
    # Send the modified image back to the user
    await message.reply_photo(image)

# Handle incoming image messages
@app.on_message(filters.photo)
async def handle_photo(_, message: Message):
    # Add a sticker to the image
    await add_sticker_to_image(message, "CAACAgUAAxkBAAOiZzOa1iLzvrUf6qKJIFyB2bQMZ1EAAmMPAAJ7VoBVav_8h5kAAXANNgQ")

if __name__ == "__main__":
    app.run()