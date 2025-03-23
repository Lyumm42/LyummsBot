import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters

load_dotenv()


async def cmd_start(update, context):
    await update.message.reply_text("Привет!")


async def cmd_help(update, context):
    help_text = (
        "Доступные команды:\n"
        "/start - начать общение\n"
        "/help - показать справку\n"
        "Отправьте любое сообщение, и бот его повторит."
    )
    await update.message.reply_text(help_text)


async def echo(update, context):
    user_text = update.message.text
    await update.message.reply_text(user_text)


def main():
    token = os.getenv("TOKEN")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("help", cmd_help))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()


if __name__ == "__main__":
    main()