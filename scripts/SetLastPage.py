import requests
from bs4 import BeautifulSoup


class SetLastPage:
    def __init__(self, url: str):
        self.url = url
        self.page_numbers = []

    def set_last_page(self):
        p = requests.get(self.url)
        soups = BeautifulSoup(p.content, "lxml")
        pages = soups.find_all('div', class_='pagination__nav')
        if not pages:
            return 1
        if pages:
            for page in pages:
                for page_number in page.find_all('a', href=True):
                    self.page_numbers.append(page_number['data-page'])
                return self.page_numbers[-1]
