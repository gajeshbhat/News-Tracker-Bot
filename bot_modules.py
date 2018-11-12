import telegram
import logging
import os
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters
from pymongo import MongoClient
from side_utils import get_article_text_summary, get_agency_id

# Chat store
class Chats(object):

    def __init__(self):
        self.chats = []

    def add(self, user_chat_session_id):
        user_input = {
        "chat_id":user_chat_session_id.message.chat_id,
        "input":user_chat_session_id.message.text,
        }
        self.chats.append(user_input)

    def get(self, chat_id):
        for chat in self.chats:
            if chat['chat_id'] == chat_id:
                return chat['input']
        return {}

    def remove(self,chat_id):
        for chat in self.chats:
            if chat['chat_id'] == chat_id:
                self.chats.remove(chat)
                return True
        return False

# Bot and dispatcher initialization
news_bot = telegram.Bot(token=os.getenv('ZABDAKEY'))
message_handle_updater = Updater(token=os.getenv('ZABDAKEY'))
user_conversations = Chats()

# Initate dispatcher
news_dispatcher = message_handle_updater.dispatcher

# Command handling methods
def start_bot(news_bot, user_chat_session_id):
    news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Hello! Please type /help to view commands.")

def display_help(news_bot, user_chat_session_id):
    news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Help document.")

def other_messages(news_bot, user_chat_session_id):
    if user_chat_session_id.message.text == "Cancel":
        reply_markup = telegram.ReplyKeyboardRemove()
        news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Action aborted.",reply_markup=reply_markup)

    elif user_chat_session_id.message.text == "Text Summary" and user_conversations.get(user_chat_session_id.message.chat_id) != {}:
        send_text(user_chat_session_id)

    elif user_chat_session_id.message.text == "Audio Summary" and user_conversations.get(user_chat_session_id.message.chat_id) != {}:
        send_audio_summary(user_chat_session_id)

    elif  user_chat_session_id.message.text == "Both" and user_conversations.get(user_chat_session_id.message.chat_id) != {}:
        send_text(user_chat_session_id)
        send_audio_summary(user_chat_session_id)

    elif user_chat_session_id.message.text in get_menu_items():
        user_conversations.add(user_chat_session_id)
        reply_markup = get_options_markup()
        news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Select the format of the news.",reply_markup=reply_markup)

    else:
        news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Unknown Command! Click Cancel Button to exit from menu or type /help for instructions.")

def get_latest_news(news_bot, user_chat_session_id):
    source_list = get_menu_items()
    reply_markup = get_source_keyboard_markup(source_list)
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

#Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
#Helper methods
def get_options_markup():
    news_options =[["Text Summary"],["Audio Summary"],["Both"],["Cancel"]]
    reply_markup = telegram.ReplyKeyboardMarkup(news_options,resize_keyboard=True)
    return reply_markup

def get_menu_items():
    client = MongoClient('localhost',27017)
    news_db =  client.news_db
    news_sources = news_db.news_sources.find({})
    if news_sources == None:
        return []
    else:
        news_source_buttons = list()
        for source in news_sources:
            news_source_buttons.append(source['name'])
        return news_source_buttons

def get_source_keyboard_markup(list_items):
    markup_list = list()
    col_counter = 0
    temp_append_list = list()
    for idx in range(0,len(list_items)-1):
        if idx == 68:
            markup_list.append([list_items[idx+1],"Cancel"])
            break
        if col_counter == 3:
            markup_list.append(temp_append_list)
            col_counter = 0 ;
            temp_append_list =[]
        else:
            temp_append_list.append(list_items[idx])
            col_counter+=1
    return telegram.ReplyKeyboardMarkup(markup_list,resize_keyboard=True)

def send_text_summary(user_chat_session_id):
    text_news_summary = get_article_text_summary(user_conversations.get(user_chat_session_id.message.chat_id))
    user_conversations.remove(user_chat_session_id.message.chat_id)
    reply_markup = telegram.ReplyKeyboardRemove()
    news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text=text_news_summary,disable_web_page_preview=True,parse_mode=telegram.ParseMode.MARKDOWN)
    news_bot.send_message(chat_id=user_chat_session_id.message.chat_id, text="Check Back later for updates.",reply_markup=reply_markup)

def send_audio_summary(user_chat_session_id):
     bot.send_audio(chat_id=update.message.chat_id, audio=open('audio_summary/'+ str(get_agency_id(user_chat_session_id.message.text)) +'-summary.mp3', 'rb'),text= "Audio summary.")
