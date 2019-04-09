from bot_modules import *
from side_utils import constant_refresh_db

#Recrawl
constant_refresh_db()

#Start the bot
message_handle_updater.start_polling()
