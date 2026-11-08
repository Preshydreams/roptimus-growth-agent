import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROUP_LINK = "https://t.me/+3pRtVRtD4m5lMDdk"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "Welcome to Roptimus AI Growth Agent!\n\n"
        "I'm here to help you discover Roptimus, "
        "understand the platform and connect with our community.\n\n"
        "Use /about to learn more or /community to join us."
    )
    await update.message.reply_text(message)


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Roptimus AI Growth Agent helps people discover "
        "information about Roptimus and its community.\n\n"
        "Always research investment opportunities carefully "
        "and understand the risks before committing funds."
    )


async def community(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Join the Roptimus community here:\n{GROUP_LINK}"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Thanks for your message! I'm being developed to provide "
        "helpful information about Roptimus. "
        "Use /community to access our Telegram group."
    )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("community", community))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("Roptimus Growth Agent is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
