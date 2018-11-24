from random import randint
from time import sleep
from urllib.request import urlopen
import json

from bs4 import BeautifulSoup
from unidecode import unidecode

sample_url = 'https://www.youtube.com/results?search_query=mario+budowlaniec&pbj=1'

data_filename = 'database.json'


class VideoFetcher(object):
    def __init__(self):
        with open(data_filename) as f:
            people = json.load(f)
        for person in people:
            if person.get("youtube_video_id"):
                continue
            first_accurate_video = self.get_first_accurate_video(person.get("name").replace(" ", "%20"))
            if not first_accurate_video:
                continue
            print(person["name"], ' fetched')
            person["youtube_video_id"] = first_accurate_video
            sleep(randint(2, 4))
            self.save(people)

    @staticmethod
    def get_first_accurate_video(search):
        response = urlopen('https://www.youtube.com/results?search_query=' + unidecode(search))
        soup = BeautifulSoup(response)
        divs = soup.find_all("div", {"class": "yt-lockup-content"})
        videos_found = []
        for i in divs:
            href = i.find('a', href=True)
            if not href:
                return None
            videos_found.append(href['href'])
        if not videos_found:
            return None
        return videos_found[0]

    def save(self, data):
        with open(data_filename, 'w') as outfile:
            json.dump(data, outfile, ensure_ascii=False)

VideoFetcher()
