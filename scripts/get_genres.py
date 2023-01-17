import requests
from bs4 import BeautifulSoup


class GetGenres:
    def __init__(self, url: str):
        self.url = url
        self.genres = []


    def get_genres(self):
        p = requests.get(self.url)
        soups = BeautifulSoup(p.content, "lxml")
        genres = soups.find_all('div', class_='checkbox-wrapper')
        for genre in genres:
            for genre_tag in genre.find_all('input'):
                if genre_tag['data-tag'] not in self.genres:
                    self.genres.append(genre_tag['data-tag'])
        return self.genres
