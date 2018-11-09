import requests
from side_utils import *
from pymongo import MongoClient
from os import getenv

class News_Modules:
    client = MongoClient('localhost',27017)
    news_db =  client.news_db

    def get_news_details(self,url):
        response = requests.get(url,params={'apiKey':getenv('NEWSAPI')})
        return response.json()

    def create_news_sources(self,source_list):
        for source in source_list:
            source_info={
            "search_id":source['id'],
            "name":source['name'],
            "description":source['description'],
            "lang":source['language'],
            "site_url":source['url'],
            "api_url":"https://newsapi.org/v1/articles?source="+str(source['id'])
            }
            self.news_db.news_sources.insert_one(source_info)

    def get_news_summary(self,news_source_list):
        for source in news_source_list:
            article_list = self.get_news_details(source['api_url'])['articles']
            news_articles={
            'name':source['name'],
            'search_id':source['search_id'],
            'lang':source['lang'],
            'articles':article_list,
            }
            self.news_db.news_articles.insert(news_articles,check_keys=False)

    def get_text_summary(self,agency_name):
        news_article_list = self.news_db.news_articles.find({'search_id':str(agency_name)})
        summary_report = '\t*Breaking Headlines :*\n\n'
        for articles in news_article_list:
            for article in articles['articles']:
                summary_report+='['+ article['title'] +']('+ (article['url']) + ')\n\n'
            return summary_report

    def prepare_news_summary(self):
        news_articles = self.news_db.news_articles.find({})
        for article in news_articles:
            summary_desc = '\n Recent headlines in '+ str(article['name']) +'  today are\n'
            for desc in article['articles']:
                if(desc['description'] ==  None):
                    summary_desc+=desc['title'] + "\n In other news \n"
                else:
                    summary_desc+=desc['title']+"\n"+desc['description'] + "\n In other news \n"
            summary_desc+= "\n Check back later for updates."
            try:
                preapre_news_audio(article['search_id'],article['lang'],summary_desc)
            except Exception as e:
                log_error_to_file(e,NEWS_MODULE_LOGS)
