import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from MARADMIN_Scraper import main as search

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Searching...")
    names = search()
    for i in names:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=i)

async def introduce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I am the MARADMIN Bot, When a new maradmin gets published simply enter /start\
                                                                            and I will compare it to and premade list of Marines and\
                                                                            tell you which one of your friends is getting promoted.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="None Yet")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6388000969:AAF0sFp3lzch6ecDf8WJ7U0ThooJBKUvRnU').build()

    start_handler = CommandHandler('start', start)
    intro_handler = CommandHandler('introduce', introduce)
    application.add_handler(start_handler)
    application.add_handler(intro_handler)

    application.run_polling()
    #6388000969