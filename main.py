from telegram.ext import Updater
import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from glossary.classes import Glossary


updater = Updater(token='Your token', use_context=True)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dispatcher = updater.dispatcher
g = Glossary()


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me any English word :)")


def echo(update: Update, context: CallbackContext):
    string = g.get_and_build(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=string)


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
start_handler = CommandHandler('start', start)


dispatcher.add_handler(echo_handler)
dispatcher.add_handler(start_handler)
updater.start_polling()

updater.idle()
