import json
import os
import requests
from bs4 import BeautifulSoup
from scripts.SetLastPage import SetLastPage
from scripts.FetchLinks import FetchRecordLinks


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class WriteAudioEquipment:

    def __init__(self) -> None:
        self.last_page: str = ""
        self.headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }
        self.product_links: list = []
        self.audioEquipment: list = []
        self.base_url: str = 'https://aux33tours.com'
        self.category = '/collections/equipement'
        self.r = requests.get('https://aux33tours.com/collections/equipement')
        self.soup = BeautifulSoup(self.r.content, "lxml")
        self.set_last_page()
        self.fetch_links()
        self.fetchEquipment()
        self.write_new_arrivals()

    def fetch_links(self) -> None:
        fetch_links = FetchRecordLinks(f'{self.base_url}{self.category}?sort_by=title-ascending&page=', self.get_last_page())
        self.product_links = fetch_links.fetch_record_links()

    def fetchEquipment(self) -> None:

        for product in self.product_links:
            self.r = requests.get(product)
            self.soup = BeautifulSoup(self.r.content, "lxml")
            name = self.soup.find('h1', class_='product-meta__title heading h1').text.strip()
            price = self.soup.find('span', class_='price').text.strip()
            description = self.soup.find('div', class_='rte text--pull').text.strip()
            equipment = {
                'name': name,
                'price': price,
                'description': description,
                'link': product
            }
            self.audioEquipment.append(equipment)

    def write_new_arrivals(self):
        self.write_to_file('AudioEquipment')
        print("Done! New arrivals have been saved.")

    def write_to_file(self, FILE_NAME):
        with open(f'../json/equipment/{FILE_NAME}.json', mode="w", newline="") as jsonFile:
            print(f'Writing {FILE_NAME} to file...')
            json.dump(self.audioEquipment, jsonFile)
        print(f"File written: {FILE_NAME}")

    def set_last_page(self) -> None:
        set_last_page = SetLastPage(f'{self.base_url}{self.category}?sort_by=title-ascending&page=1')
        self.last_page = set_last_page.set_last_page()

    def get_last_page(self) -> int:
        return int(self.last_page)


if __name__ == '__main__':
    vinyls = WriteAudioEquipment()
