import requests
import os
import json
from pymongo import MongoClient
from gtts import gTTS



class News_Modules:
    client = MongoClient('localhost',27017)
    news_db =  client.news_db

    def preapre_news_audio(self,id,lang_value,summary_desc):
        news_string = summary_desc
        news_audio = gTTS(text=news_string,lang=lang_value)
        news_audio.save("audio_summary/" + str(id) + "-summary.mp3")

    def curate_news_summary(self):
        news_articles = self.news_db.news_articles.find({})
        for article in news_articles:
            summary_desc = '\n Recent headlines in '+ str(article['name']) +'  today are\n'
            for desc in article['articles']:
                if(desc['description'] ==  None):
                    summary_desc+=desc['title']+"\n"+ "Read the story on" + article['name']+ "\n In other news \n"
                else:
                    summary_desc+=desc['title']+"\n"+desc['description'] + "\n In other news \n"
            summary_desc+= "\n For more recent updates refresh every hour."
            self.preapre_news_audio(article['search_id'],article['lang'],summary_desc)

    def get_raw_json(self,url):
        response = requests.get(url,params={'apiKey':str(os.getenv('NEWSAPI'))})
        if response.json()['status'] == "error":
            print("Error")
        else:
            return response.json()['articles']

    def refresh_news_sources(self):
        source_fetch_url = 'https://newsapi.org/v1/sources'
        sources_db = self.client.news_db
        news_sources = sources_db.news_sources
        news_sources.delete_many({})
        for source in self.get_raw_json(url=source_fetch_url)['sources']:
            source_info={
            "search_id":source['id'],
            "name":source['name'],
            "description":source['description'],
            "lang":source['language'],
            "site_url":source['url'],
            "api_url":"https://newsapi.org/v1/articles?source="+str(source['id'])
            }
            news_sources.insert_one(source_info)

    def fetch_news_summary(self):
        self.refresh_news_sources() # Refresh API List
        articles_collection = self.news_db.news_articles
        self.news_db.news_articles.delete_many({})
        for article in self.news_db.news_sources.find({}):
            article_json = self.get_raw_json(article['api_url'])
            news_articles={
            'name':article['name'],
            'search_id':article['search_id'],
            'lang':article['lang'],
            'articles':article_json,
            }
            self.news_db.news_articles.insert(news_articles,check_keys=False)

    def get_text_summary(self,agency_name):
        news_article_list = self.news_db.news_articles.find({'search_id':str(agency_name)})
        summary_report = '\t*Breaking Headlines :*\n\n'
        for articles in news_article_list:
            for article in articles['articles']:
                summary_report+='['+ article['title'] +']('+ (article['url']) + ')\n\n'
        return summary_report


def main():
    nw = News_Modules()
    nw.fetch_news_summary()
    #nw.curate_news_summary()

if __name__ == '__main__':
    main()
