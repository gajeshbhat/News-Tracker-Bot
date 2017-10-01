import requests
from BeautifulSoup import BeautifulSoup
from pymongo import MongoClient

def get_reuters_global_summary():
    summary_page = requests.get("http://www.reuters.com/news/archive/worldNews?date=today")
    content_soup = BeautifulSoup(summary_page.content)
    div_soup = content_soup.findAll('div',{'class':'story-content'})

    if(summary_page.status_code != 200):
        print "Error downloading page."

    client = MongoClient('localhost',27017)
    news_db =  client.news_db
    current_summary = news_db.current_summary
    clear_db = news_db.current_summary.delete_many({})

    for div in div_soup:
        article_link = div.findNext('a',href=True)
        article_heading = div.findNext('h3')
        article_content_summary = div.findNext('p')
        news_article={
        "Headline":article_heading.text,
        "Link":"http://www.reuters.com/" + article_link['href'],
        "Summary" : article_content_summary.text
        }
        current_summary.insert_one(news_article)
    return True

def preapre_audio():
    return True

def update_news():
    return True
