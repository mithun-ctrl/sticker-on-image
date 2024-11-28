import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Set up the Pyrogram client
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Welcome to the Sticker ID Bot!\n\n"
        "Just send me any sticker and I'll tell you its ID and details."
    )
    await update.message.reply_text(welcome_message)

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sticker = update.message.sticker
    
    info_message = (
        "🎯 Sticker Information:\n\n"
        f"📋 File ID:\n`{sticker.file_id}`\n\n"
        f"🆔 File Unique ID:\n`{sticker.file_unique_id}`\n\n"
        f"📦 Set Name:\n`{sticker.set_name if sticker.set_name else 'Not part of a set'}`\n\n"
        f"😀 Emoji: {sticker.emoji if sticker.emoji else 'No emoji'}"
    )
    
    try:
        await update.message.reply_text(info_message, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error sending sticker info: {e}")
        await update.message.reply_text("Sorry, there was an error. Please try again.")

def main():
    # Load environment variables
    load_dotenv()
    
    # Get bot token from environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        raise ValueError("No bot token found in environment variables!")
    
    # Create application
    application = Application.builder().token(bot_token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    
    # Start bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
