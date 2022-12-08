import csv
import random
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class Write_vinyl:
    pass

    def __init__(self) -> None:
        self.filtered_genres: list = []
        self.price: float = 0.00
        self.name: str = ""
        self.last_page: str = ""
        self.headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }
        self.product_link: str = ""
        self.product_links: list = []
        self.product_list: list = []
        self.page_numbers: list = []
        self.genres: list = []
        self.records: list = []
        self.base_url: str = 'https://aux33tours.com'
        self.genre: str = ""
        self.category: str = ''
        # self.set_last_page()
        # self.get_genres()
        self.write_new_arrivals()

    def get_genres(self) -> list:
        p = requests.get(f'{self.base_url}{self.category}')
        soups = BeautifulSoup(p.content, "lxml")
        genres = soups.find_all('div', class_='checkbox-wrapper')
        for genre in genres:
            for genre_tag in genre.find_all('input'):
                if genre_tag['data-tag'] not in self.genres:
                    self.genres.append(genre_tag['data-tag'])
        # pprint(self.genres)
        return self.genres

    def set_last_page(self) -> None:
        p = requests.get(f'{self.base_url}{self.category}{self.genre}?sort_by=title-ascending&page=1')
        soups = BeautifulSoup(p.content, "lxml")
        pages = soups.find_all('div', class_='pagination__nav')
        if not pages:
            self.last_page = 1
        if pages:
            for page in pages:
                for page_number in page.find_all('a', href=True):
                    self.page_numbers.append(page_number['data-page'])
                self.last_page = self.page_numbers[-1]

    def get_last_page(self) -> int:
        # print(self.last_page)
        return int(self.last_page)

    def vinyl_link(self) -> list:
        self.set_last_page()
        self.product_links = []
        self.product_list = []
        self.records = []
        for page in range(1, self.get_last_page() + 1):
            print(f'{self.base_url}{self.category}{self.genre}?sort_by=title-ascending&page={page}')
            r = requests.get(f'{self.base_url}{self.category}{self.genre}?sort_by=title-ascending&page={page}')
            soup = BeautifulSoup(r.content, "lxml")
            self.product_list = soup.find_all('div', class_='product-item__info')
            for item in self.product_list:
                for link in item.find_all('a', href=True):
                    self.product_links.append(self.base_url + link['href'])
        for product in self.product_links:
            self.product_link = product
            r2 = requests.get(self.product_link, headers=self.headers)
            soup = BeautifulSoup(r2.content, "lxml")
            self.name = soup.find('h1', class_='product-meta__title heading h1').text.strip()
            self.price = soup.find('span', class_='price').text.strip()
            self.records.append({
                "name": self.name,
                "price": self.price,
                "link": self.product_link
            })
        return self.records

    def write_new_arrivals(self):
        self.category = '/collections/nouveautes/'
        for genre in self.get_genres():
            self.genre = genre
            self.write_to_file(self.genre, 'New-Arrivals')
        print("Done! New arrivals have been saved.")

    def write_to_file(self, FILE_NAME, FOLDER):
        with open(f'csv/records/{FOLDER}/{FILE_NAME}.csv', mode="w", newline="") as csvfile:
            print(f'Writing {FILE_NAME} to file...')
            records = self.vinyl_link()
            fieldnames = (['name', 'price', 'link'])
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
            csvfile.close()
        print(f"File written: {FILE_NAME}")


if __name__ == '__main__':
    vinyls = Write_vinyl()
