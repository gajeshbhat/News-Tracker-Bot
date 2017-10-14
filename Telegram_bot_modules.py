import logging
import commands
from os import getenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup ,ParseMode
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from news_modules import News_Modules

msgCmdupdater = Updater(token=getenv('NEWSBOTKEY'))
msgCmddispatcher = msgCmdupdater.dispatcher

start_msg ="""Welcome to Latest news curator. /manual to RTFM """

user_doc_msg="""
Welcome to Latest News manual.\n
Commands and arguments to be used:\n
/start - Displays the opening message\n
/manual -Displays the user documentation\n
/news paper-name - Returns an audio news summary
"""

#Methods that handle general commands
def start_bot(bot,update):
     bot.send_message(chat_id=update.message.chat_id, text=start_msg)
     return True

def manual_bot(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text=user_doc_msg)
    return True

def wrong_command(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="wrong command! type /manual for help")
    return True

def get_user_query(agency_name):
    summary_obj = News_Modules()
    return summary_obj.get_text_summary(agency_name)

def get_news_summary(bot,update,args):
    if len(args) < 1 or len(args) > 1:
        bot.send_message(chat_id=update.message.chat_id, text="wrong number of arguments! type /manual to view commands.")
        return False
    try:
        bot.send_message(chat_id=update.message.chat_id,text=get_user_query(str(args[0])),disable_web_page_preview=True,parse_mode=ParseMode.MARKDOWN)
        bot.send_audio(chat_id=update.message.chat_id, audio=open('audio_summary/'+ str(args[0]) +'-summary.mp3', 'rb'),text= "Audio summary.")
    except:
        bot.send_message(chat_id=update.message.chat_id,text="No Such news feed exist type /f to know news feed and tags")
    return True

#Handles commands passed by the bot
start_handler = CommandHandler('start',start_bot)
manual_handler = CommandHandler('manual',manual_bot)
news_handler = CommandHandler('news',get_news_summary,pass_args=True)
wrong_message_handler = MessageHandler(Filters.text,wrong_command)

#Adding Constructed command results
msgCmddispatcher.add_handler(start_handler)
msgCmddispatcher.add_handler(manual_handler)
msgCmddispatcher.add_handler(news_handler)
msgCmddispatcher.add_handler(wrong_message_handler)

#Setting up logging for Errors and Exceptions
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
