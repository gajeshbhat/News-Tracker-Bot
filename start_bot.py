from bot_modules import *
from side_utils import hard_refresh_news_db

# First time Hard Refresh DB
hard_refresh_news_db()

#Start the bot
message_handle_updater.start_polling()
