import traceback
from news_modules import News_Modules

LOGFILE = "logs.txt"
SOURCE_FETCH_URL = "https://newsapi.org/v1/sources"
CONTENT_SAPERATOR = "\n\n"

def hard_refresh_news_db():
    try:
        news_module_obj = News_Modules()
        news_sources = news_module_obj.news_db.news_sources
        news_sources.delete_many({})

        news_sources = news_module_obj.get_news_details(SOURCE_FETCH_URL)['sources']
        news_module_obj.create_news_sources(news_sources)
        articles_collection = news_module_obj.news_db.news_articles

        news_module_obj.news_db.news_articles.delete_many({})
        news_source_list = news_module_obj.news_db.news_sources.find({})
        news_module_obj.get_news_summary(news_source_list)
        news_module_obj.prepare_news_summary()
    except Exception as e:
        log_error_to_file(e,LOGFILE)


def constant_refresh_db():
    try:
        news_module_obj = News_Modules()
        news_module_obj.news_db.news_articles.delete_many({})
        news_source_list = news_module_obj.news_db.news_sources.find({}
        news_module_obj.get_news_summary(news_source_list)
        news_module_obj.prepare_news_summary()
    except Exception as e:
        log_error_to_file(e,LOGFILE)

def get_article_text_summary(agency_name):
    news_module_obj = News_Modules()
    agency_id = news_module_obj.get_agency_id(agency_name)
    return news_module_obj.get_text_summary(agency_id)

def log_error_to_file(e,LOG_FILE_TYPE):
    with open(LOG_FILE_TYPE, 'a') as filePointer:
        filePointer.write(CONTENT_SAPERATOR + str(traceback.format_exc()))
