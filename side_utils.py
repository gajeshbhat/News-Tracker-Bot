import traceback
from news_modules import News_Modules
from gtts import gTTS

NEWS_MODULE_LOGS = "logs/news_module_err_logs.txt"
BOT_MODULE_LOGS = "logs/bot_module_err_logs.txt"
DB_MONGO_LOGS = "logs/db_pymongo_err_logs.txt"
SOURCE_FETCH_URL = "https://newsapi.org/v1/sources"
CONTENT_SAPERATOR = "\n\n"


def preapre_news_audio(id,lang_value,summary_desc):
    news_string = summary_desc
    news_audio = gTTS(text=news_string,lang=lang_value)
    news_audio.save("data/audio_summary/" + str(id) + "-summary.mp3")

def log_error_to_file(e,LOG_FILE_TYPE):
    with open(LOG_FILE_TYPE, 'a') as filePointer:
        filePointer.write(CONTENT_SAPERATOR + str(traceback.format_exc()))
def hard_refresh_news_db():
    try:
        news_module_obj = News_Modules()
    except Exception as e:
        log_error_to_file(e,NEWS_MODULE_LOGS)

    try:
        sources_db = news_module_obj.news_db
        news_sources = sources_db.news_sources
        news_sources.delete_many({})
    except Exception as e:
        log_error_to_file(e,DB_MONGO_LOGS)

    try:
        news_sources = news_module_obj.get_news_details(SOURCE_FETCH_URL)['sources']
        news_module_obj.create_news_sources(news_sources)
    except Exception as e:
        log_error_to_file(e,NEWS_MODULE_LOGS)
    try:
        articles_collection = news_module_obj.news_db.news_articles
        news_module_obj.news_db.news_articles.delete_many({})
    except Exception as e:
        log_error_to_file(e,DB_MONGO_LOGS)
    try:
        news_source_list = news_module_obj.news_db.news_sources.find({})
        news_module_obj.get_news_summary(news_source_list)
    except Exception as e:
        log_error_to_file(e,NEWS_MODULE_LOGS)
    news_module_obj.prepare_news_summary()

def constant_refresh_db():
    try:
        news_module_obj = News_Modules()
    except Exception as e:
        log_error_to_file(e,NEWS_MODULE_LOGS)
    try:
        articles_collection = news_module_obj.news_db.news_articles
        news_module_obj.news_db.news_articles.delete_many({})
        news_source_list = news_module_obj.news_db.news_sources.find({})
    except Exception as e:
        log_error_to_file(e,DB_MONGO_LOGS)

    news_module_obj.get_news_summary(news_source_list)
    news_module_obj.prepare_news_summary()
