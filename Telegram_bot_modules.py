import logging
import commands
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from os import getenv

msgCmdupdater = Updater(token=getenv('NEWSDEL'))
msgCmddispatcher = msgCmdupdater.dispatcher

start_msg ="""Welcome to Latest news curator. /manual to RTFM"""

user_doc_msg="""
Welcome to Latest News manual.\n
Commands and arguments to be used:\n
/start - Displays the opening message\n
/manual -Displays the user documentation\n
/world - Returns an audio news summary
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
def get_world_summary(bot,update):
    bot.send_audio(chat_id=update.message.chat_id, audio=open('CurrentSummary.mp3', 'rb'),text="Todays news summary.")
    return True

#Handles commands passed by the bot
start_handler = CommandHandler('start',start_bot)
manual_handler = CommandHandler('manual',manual_bot)
world_news_handler = CommandHandler('world',get_world_summary)

#Adding Constructed command results
msgCmddispatcher.add_handler(start_handler)
msgCmddispatcher.add_handler(manual_handler)
msgCmddispatcher.add_handler(world_news_handler)

#Setting up logging for Errors and Exceptions
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
