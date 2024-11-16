import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class StickerBot:
    def __init__(self, token):
        """Initialize the bot with your Telegram token"""
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
        
    def setup_handlers(self):
        """Set up message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Message handlers - Fixed filters syntax
        self.application.add_handler(MessageHandler(filters.Sticker.ALL, self.handle_sticker))
        self.application.add_handler(MessageHandler(filters.Animation.ALL, self.handle_animation))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /start is issued."""
        welcome_message = (
            "👋 Welcome to the Sticker ID Bot!\n\n"
            "I can help you get information about stickers and animated stickers (GIFs).\n\n"
            "Just send me any sticker or GIF, and I'll tell you its ID and other details.\n\n"
            "Commands:\n"
            "/help - Show help message\n"
            "/start - Start the bot"
        )
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when the command /help is issued."""
        help_message = (
            "🔍 How to use this bot:\n\n"
            "1. Send any sticker to get its details\n"
            "2. Send any GIF to get its information\n\n"
            "You'll receive:\n"
            "- File ID\n"
            "- File Unique ID\n"
            "- Sticker Set Name (for stickers)\n"
            "- Sticker Emoji (for stickers)\n"
            "- File Size\n"
            "- Dimensions"
        )
        await update.message.reply_text(help_message)

    async def handle_sticker(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle sticker messages and return sticker information."""
        sticker = update.message.sticker
        
        info_message = (
            "🎯 Sticker Information:\n\n"
            f"📋 File ID:\n`{sticker.file_id}`\n\n"
            f"🆔 File Unique ID:\n`{sticker.file_unique_id}`\n\n"
            f"📦 Set Name:\n`{sticker.set_name if sticker.set_name else 'Not part of a set'}`\n\n"
            f"😀 Emoji: {sticker.emoji if sticker.emoji else 'No emoji'}\n"
            f"📏 Dimensions: {sticker.width}x{sticker.height}\n"
            f"💾 File Size: {sticker.file_size} bytes\n"
            f"🎨 Is Animated: {'Yes' if sticker.is_animated else 'No'}\n"
            f"🎬 Is Video: {'Yes' if sticker.is_video else 'No'}"
        )
        
        try:
            await update.message.reply_text(
                info_message,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error sending sticker info: {e}")
            await update.message.reply_text(
                "Sorry, there was an error processing this sticker. Please try again."
            )

    async def handle_animation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle animated stickers and GIFs."""
        animation = update.message.animation
        
        info_message = (
            "🎬 Animation Information:\n\n"
            f"📋 File ID:\n`{animation.file_id}`\n\n"
            f"🆔 File Unique ID:\n`{animation.file_unique_id}`\n\n"
            f"📏 Dimensions: {animation.width}x{animation.height}\n"
            f"⏱ Duration: {animation.duration}s\n"
            f"💾 File Size: {animation.file_size} bytes\n"
            f"📝 File Name: {animation.file_name if animation.file_name else 'Not available'}"
        )
        
        try:
            await update.message.reply_text(
                info_message,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error sending animation info: {e}")
            await update.message.reply_text(
                "Sorry, there was an error processing this animation. Please try again."
            )

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Log errors caused by updates."""
        logger.error(f"Update {update} caused error {context.error}")
        if update and isinstance(update, Update) and update.message:
            await update.message.reply_text(
                "Sorry, an error occurred while processing your request. Please try again later."
            )

    def run(self):
        """Start the bot."""
        logger.info("Starting bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    # Load environment variables
    load_dotenv()
    
    # Get bot token from environment variable
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        raise ValueError("No bot token found in environment variables!")
    
    # Create and run the bot
    sticker_bot = StickerBot(bot_token)
    sticker_bot.run()

if __name__ == '__main__':
    main()
