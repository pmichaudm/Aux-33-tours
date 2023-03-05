import json
import os

from scripts.get_genres import GetGenres
from scripts.get_record_dict import GetRecord
from scripts.set_last_page import SetLastPage
from scripts.fetch_record_links import FetchRecordLinks


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)

class WriteNewVinyl:

    def __init__(self) -> None:
        self.price: float = 0.00
        self.name: str = ""
        self.last_page: str = ""
        self.headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }
        self.product_links: list = []
        self.product_list: list = []
        self.page_numbers: list = []
        self.genre: str = ""
        self.records: list = []
        self.base_url: str = 'https://aux33tours.com'
        self.category = '/collections/nouveautes/'
        self.get_genres()
        self.set_last_page()
        self.fetch_links()
        self.fetch_record()
        self.write_new_arrivals()

    def fetch_links(self) -> None:
        fetch_links = FetchRecordLinks(f'{self.base_url}{self.category}?sort_by=title-ascending&page=', self.get_last_page())
        self.product_links = fetch_links.fetch_record_links()

    def fetch_record(self) -> None:
        for product in self.product_links:
            get_record = GetRecord(product)
            record = get_record.get_record()
            self.records.append(record)

    def write_new_arrivals(self):
        for genre in self.get_genres():
            if genre.startswith("nouveaux-arrivages"):
                self.genre = genre
                self.write_to_file(self.genre, 'New-Arrivals')
        print("Done! New arrivals have been saved.")

    # **** THIS IS THE CSV WRITER ****
    # def write_to_file(self, FILE_NAME, FOLDER):
    #     with open(f'../csv/records/{FOLDER}/{FILE_NAME}.csv', mode="w", newline="") as csvfile:
    #         print(f'Writing {FILE_NAME} to file...')
    #         fieldnames = ['name', 'price', 'link', 'genre']
    #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         writer.writeheader()
    #         writer.writerows(self.records)
    #         csvfile.close()
    #     print(f"File written: {FILE_NAME}")

    def write_to_file(self, FILE_NAME, FOLDER):
        with open(f'../json/records/{FOLDER}/{FILE_NAME}.json', mode="w", newline="") as jsonFile:
            print(f'Writing {FILE_NAME} to file...')
            json.dump(self.records, jsonFile)
        print(f"File written: {FILE_NAME}")

    def get_genres(self) -> list:
        get_genres = GetGenres(f'{self.base_url}{self.category}')
        return get_genres.get_genres()

    def set_last_page(self) -> None:
        set_last_page = SetLastPage(f'{self.base_url}{self.category}?sort_by=title-ascending&page=1')
        self.last_page = set_last_page.set_last_page()

    def get_last_page(self) -> int:
        return int(self.last_page)


if __name__ == '__main__':
    vinyls = WriteNewVinyl()
