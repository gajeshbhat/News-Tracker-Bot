import os
from news_modules import News_Modules
from Telegram_bot_modules import msgCmdupdater
from apscheduler.schedulers.blocking import BlockingScheduler
from pprint import pprint

news_obj=News_Modules()

msgCmdupdater.start_polling() #Start bot thread.

#First Crawl and Store. Exception for Google Text to speech failure.
try:
    news_obj.fetch_news_summary()
    news_obj.curate_news_summary()
except:
    news_obj.fetch_news_summary()
    news_obj.curate_news_summary()

scheduler = BlockingScheduler()
scheduler.add_job(news_obj.fetch_news_summary, 'interval', hours=1)
scheduler.add_job(news_obj.curate_news_summary,'interval', hours=1)
scheduler.start() # Start the refresh thread
