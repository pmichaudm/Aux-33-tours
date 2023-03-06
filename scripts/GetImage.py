import requests
from bs4 import BeautifulSoup


class GetImage:
    def __init__(self, url: str):
        self.url = url
        self.genres = []


    def get_image(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "lxml")
        image = soup.find_all('meta', property='og:image', content=True)
        for img in image:
            return img["content"]