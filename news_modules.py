import requests
import os
from BeautifulSoup import BeautifulSoup
from pymongo import MongoClient
from gtts import gTTS

class News_Modules:
    client = MongoClient('localhost',27017)
    news_db =  client.news_db
    current_summary = news_db.current_summary

    def get_reuters_global_summary(self):

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
        return True

    def curate_summary(self):
        news_text = '\n Recent headlines in the world news today are\n'
        for article in self.current_summary.find():
            news_text+= '\n' + article['Headline'] + '\n' + article['Summary'] + "\n In other news"
        news_text+= "\n For more recent updates refresh your bot now."
        return news_text

    def preapre_audio(self):
        news_string = self.curate_summary()
        news_audio = gTTS(text=news_string,lang='en')
        news_audio.save("CurrentSummary.mp3")
        return True

    def update_news(self):
        return True
