import urllib.request
from bs4 import BeautifulSoup
from pprint import pprint

def test_url():
	return "https://www.aninews.in/rss/feed/category/national/general-news.xml"

def preapre_news_audio(self,id,lang_value,summary_desc):
	news_string = summary_desc
    news_audio = gTTS(text=news_string,lang=lang_value)
    news_audio.save("audio_summary/" + str(id) + "-summary.mp3")


def get_xml_soup(url):
	with urllib.request.urlopen(url) as response:
		xml = response.read()
		news_xml_soup = BeautifulSoup(xml, 'lxml-xml')
		return news_xml_soup

def parse_ani_news(xml):
	news_item_list = list()

	for item in xml.find_all('item'):
		each_item = {
		"name":item.find('title').text,
		"url":item.find('guid').text,
		"description": str(item.find('description').text),
		"cover_image":item.find('image').find('url').text,
		}
		news_item_list.append(each_item)
	
	#Other inforamtion
	news_paper_info = {
	"name": "ANI",
	"language": xml.find('channel').find('language').text,
	"last_updated_at": xml.find('lastBuildDate').text,
	"xml-feed-url": xml.find('atom:link')['href'],
	"articles": news_item_list,
	}
	return news_paper_info