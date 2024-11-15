from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, InputFile, Message
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
    
    # Download the sticker
    sticker = await app.download_media(sticker_id)
    
    # Create an InputMediaPhoto with the sticker overlaid
    media = InputMediaPhoto(media=InputFile(image), file_attach_name="image_with_sticker.png")
    media.sticker = InputFile(sticker)
    
    # Send the modified image back to the user
    await message.edit_media(media)

# Handle incoming image messages
@app.on_message(filters.photo)
async def handle_photo(_, message: Message):
    # Add a sticker to the image
    await add_sticker_to_image(message, "CAACAgUAAxkBAAOiZzOa1iLzvrUf6qKJIFyB2bQMZ1EAAmMPAAJ7VoBVav_8h5kAAXANNgQ")

if __name__ == "__main__":
    app.run()