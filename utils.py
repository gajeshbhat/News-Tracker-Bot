from subprocess import call
from os import getenv

SOURCE = "data/audio_summary_temp/"
DESTINATION = "data/audio_summary/"

def cp_dir(source, target):
    call(['cp', '-r', source, target])
