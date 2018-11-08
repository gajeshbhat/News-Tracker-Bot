from subprocess import call
from os import getenv
from gtts import gTTS

SOURCE = "data/audio_summary_temp/"
DESTINATION = "data/audio_summary/"

def copy_all_dir_contents(source, target):
    call(['cp', '-r', source, target])

def preapre_news_audio(id,lang_value,summary_desc):
    news_string = summary_desc
    news_audio = gTTS(text=news_string,lang=lang_value)
    news_audio.save("data/audio_summary_temp/" + str(id) + "-summary.mp3")
