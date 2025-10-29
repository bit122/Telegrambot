import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "8458645007:AAEZqduJx8_O0lKgZ1jd_cwK_H4KaCNkWxw"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
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

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    logger.info(f"/id from {update.effective_user.username} ({chat_id})")
    await update.message.reply_text(f"Your Chat ID is: {chat_id}")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/clear requested by {update.effective_user.username} in chat {update.message.chat_id}")
    chat_id = update.message.chat_id

async def clear_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"/clear requested by {update.effective_user.username} in chat {update.message.chat_id}")
    chat_id = update.message.chat_id

    deleted_count = 0

    # await the coroutine to get the Chat object, then call its get_history()
    chat = await context.bot.get_chat(chat_id)
    messages = await chat.get_history(limit=50)

    for message in messages:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
            deleted_count += 1
        except Exception as e:
            logger.warning(f"Failed to delete message {message.message_id}: {e}")
    await update.message.reply_text(f"Deleted {deleted_count} messages (if permitted).")
    logger.info(f"Deleted {deleted_count} messages in chat {chat_id}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id))
    app.add_handler(CommandHandler("clear", clear_messages))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, say_hello))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
