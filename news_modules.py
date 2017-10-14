import requests
import os
import json
from pprint import pprint
from BeautifulSoup import BeautifulSoup
from pymongo import MongoClient
from gtts import gTTS
from urllib2 import urlopen, Request


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

    def get_raw_json(self,url=None):
        headers = {'X-Api-Key': '%s' % str(os.getenv('NEWSAPI'))}
        request = Request(url, headers=headers)
        response = urlopen(request)
        raw_json = json.loads(response.read())
        return raw_json

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
            article_json=self.get_raw_json(article['api_url'])
            for edit_article in article_json['articles']:
                del edit_article['urlToImage']
                del edit_article['author']

            news_articles={
            'name':article['name'],
            'search_id':article['search_id'],
            'lang':article['lang'],
            'articles':article_json['articles']
            }
            self.news_db.news_articles.insert(news_articles,check_keys=False)

    # Not integrated yet..But works independently.
    def get_reuters_global_feed(self):
        summary_page = requests.get("http://www.reuters.com/news/archive/worldNews?date=today")
        content_soup = BeautifulSoup(summary_page.content)
        div_soup = content_soup.findAll('div',{'class':'story-content'})
        clear_db = self.current_summary.delete_many({})

        if(summary_page.status_code != 200):
            print "Error downloading page."

        for div in div_soup:
            article_link = div.findNext('a',href=True)
            article_heading = div.findNext('h3')
            article_content_summary = div.findNext('p')
            news_article={
            "Headline":article_heading.text,
            "Link":"http://www.reuters.com/" + article_link['href'],
            "Summary" : article_content_summary.text
            }
            self.current_summary.insert_one(news_article)

    def get_text_summary(self,agency_name):
        news_article_list = self.news_db.news_articles.find({'search_id':str(agency_name)})
        summary_report = '\t*Breaking Headlines :*\n'
        for articles in news_article_list:
            for article in articles['articles']:
                summary_report+='['+ article['title'] +']('+ (article['url']) + ')\n'
        return summary_report
