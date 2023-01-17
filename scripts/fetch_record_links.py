import requests
from bs4 import BeautifulSoup


class FetchRecordLinks:
    def __init__(self, url: str, last_page: int):
        self.url = url
        self.last_page = last_page
        self.product_list: list = []
        self.product_links: list = []
        self.base_url: str = 'https://aux33tours.com'

    def fetch_record_links(self) -> list:
        # for page in range(1, 1 + 1):  # testing with 1 page
        for page in range(1, self.last_page + 1):
            print(f'{self.url}{page}')
            r = requests.get(f'{self.url}{page}')
            soup = BeautifulSoup(r.content, "lxml")
            self.product_list = soup.find_all('div', class_='product-item__info')
            for item in self.product_list:
                for link in item.find_all('a', href=True):
                    self.product_links.append(self.base_url + link['href'])
        return self.product_links
