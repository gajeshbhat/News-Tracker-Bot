import traceback
import json
from news_modules import News_Modules

LOGFILE = "logs.txt"
SOURCE_FETCH_URL = "https://newsapi.org/v2/sources"
CONTENT_SAPERATOR = "\n"

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
        news_summary_result = news_module_obj.get_news_summary(news_source_list)
        if news_summary_result['status'] == 'ok':
            news_module_obj.prepare_news_summary()
        else:
            log_api_error(news_summary_result,LOGFILE)
    except Exception as e:
        log_error_to_file(e,LOGFILE)


def constant_refresh_db():
    try:
        news_module_obj = News_Modules()
        news_module_obj.news_db.news_articles.delete_many({})
        news_source_list = news_module_obj.news_db.news_sources.find({})
        news_summary_result = news_module_obj.get_news_summary(news_source_list)
        if news_summary_result['status'] == 'error':
            log_api_error(news_summary_result,LOGFILE)
        else:
            news_module_obj.prepare_news_summary()
    except Exception as e:
        log_error_to_file(e,LOGFILE)

def get_article_text_summary(agency_name):
    news_module_obj = News_Modules()
    agency_id = news_module_obj.get_agency_id(agency_name)
    return news_module_obj.get_text_summary(agency_id)

def log_api_error(api_response,LOG_FILE_TYPE):
    with open(LOG_FILE_TYPE, 'a') as filePointer:
        filePointer.write(str(json.dumps(api_response,indent=4,sort_keys=True)) + CONTENT_SAPERATOR)

def log_error_to_file(e,LOG_FILE_TYPE):
    with open(LOG_FILE_TYPE, 'a') as filePointer:
        filePointer.write(str(traceback.format_exc()) + CONTENT_SAPERATOR)
