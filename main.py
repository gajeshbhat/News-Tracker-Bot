from news_modules import News_Modules
from Telegram_bot_modules import msgCmdupdater
from apscheduler.schedulers.blocking import BlockingScheduler

msgCmdupdater.start_polling() #Start bot thread.

def refresh_news():
    news_obj=News_Modules()
    news_obj.update_news()

scheduler = BlockingScheduler()
scheduler.add_job(refresh_news, 'interval', hours=1)
scheduler.start() # Start the refresh thread
