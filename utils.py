from subprocess import call
from os import getenv
from gtts import gTTS
from pymongo import MongoClient

SOURCE = "data/audio_summary_temp/"
DESTINATION = "data/audio_summary/"

def copy_all_dir_contents(source, target):
    call(['cp', '-r', source, target])

def preapre_news_audio(self,id,lang_value,summary_desc):
    news_string = summary_desc
    news_audio = gTTS(text=news_string,lang=lang_value)
    news_audio.save("/data/audio_summary_temp/" + str(id) + "-summary.mp3")

def get_text_summary(self,agency_name):
    news_article_list = self.news_db.news_articles.find({'search_id':str(agency_name)})
    summary_report = '\t*Breaking Headlines :*\n\n'
    for articles in news_article_list:
        for article in articles['articles']:
            summary_report+='['+ article['title'] +']('+ (article['url']) + ')\n\n'
        return summary_report
