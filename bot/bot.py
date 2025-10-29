import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from datetime import datetime

load_dotenv()
BOT_TOKEN = os.getenv("BOT-TOKEN")

base_log_dir = "logs"

list = [
    'hello there', 'hi', 'hey', 'yo', 'sup', 'howdy', 'greetings', 'what\'s up', 'hiya', 'good day'
]

now = datetime.now()
year_folder = now.strftime("%Y")
day_folder = now.strftime("%Y-%m-%d")
log_dir = os.path.join(base_log_dir, year_folder, day_folder)
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(log_dir, "bot.log")

if os.path.exists(log_filename):
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    archived_log = os.path.join(log_dir, f"bot_{timestamp}.log")
    os.rename(log_filename, archived_log) 


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/start from {update.effective_user.username} ({update.effective_user.id})")
    await update.message.reply_text("Hello")

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Message from {update.effective_user.username}: {update.message.text}")
    await update.message.reply_text("Hello there")

async def whoareyou(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/whoareyou from {update.effective_user.username} ({update.effective_user.id})")
    await update.message.reply_text("Hi im femboy")
    
async def exit_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/exit from {update.effective_user.username} ({update.effective_user.id})")
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="exit_yes"),
            InlineKeyboardButton("No", callback_data="exit_no"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("are you sure you want to exit the bot?", reply_markup=reply_markup)

async def button_callbacK(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "exit_yes":
        await query.edit_message_text(text="Exiting... Goodbye!")
        logger.info(f"Bot exited by {update.effective_user.username} ({update.effective_user.id})")
        os._exit(0)
    else:
        await query.edit_message_text(text="Exit cancelled.")
        logger.info(f"Exit cancelled by {update.effective_user.username} ({update.effective_user.id})")

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    logger.info(f"/id from {update.effective_user.username} ({chat_id})")
    await update.message.reply_text(f"Your Chat ID is: {chat_id}")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("exit", exit_bot))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("whoami", whoareyou))
    app.add_handler(CallbackQueryHandler(button_callbacK))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, say_hello))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
