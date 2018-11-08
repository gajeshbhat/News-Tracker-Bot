import telegram
import logging
import os
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters

# Bot and dispatcher initialization
news_bot = telegram.Bot(token=os.getenv('TELEKEY'))
message_handle_updater = Updater(token=os.getenv('TELEKEY'))

# Initate dispatcher
news_dispatcher = message_handle_updater.dispatcher

# Command handling methods
def start_bot(news_bot, user_chat_session_id):
    news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Hello! Please type /help to view commands.")

def display_help(news_bot, user_chat_session_id):
    news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Help document.")

def other_messages(news_bot, user_chat_session_id):
    news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Unknown Command! type /help for instructions.")

def get_latest_news(news_bot, user_chat_session_id):
    custom_keyboard = [['ANI News','Reuters Global'],['Cancel']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Click on the feed",reply_markup=reply_markup)

# Create handlers
start_handler = CommandHandler('start', start_bot)
display_help_handler = CommandHandler('help',display_help)
latest_news_handler = CommandHandler('latest',get_latest_news)
other_message_handlers = MessageHandler(Filters.text, other_messages)

# Add handlers
news_dispatcher.add_handler(start_handler)
news_dispatcher.add_handler(display_help_handler)
news_dispatcher.add_handler(latest_news_handler)
news_dispatcher.add_handler(other_message_handlers)
