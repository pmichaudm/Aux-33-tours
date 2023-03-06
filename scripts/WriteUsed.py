import json
from scripts.GetGenres import GetGenres
from scripts.GetRecord import GetRecord
from scripts.SetLastPage import SetLastPage
from scripts.FetchLinks import FetchRecordLinks


class WriteUsedVinyl:

    def __init__(self) -> None:
        self.last_page: str = ""
        self.headers: dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        self.product_links: list = []
        self.genre: str = ""
        self.genres: list = []
        self.records: list = []
        self.base_url: str = 'https://aux33tours.com'
        self.category: str = '/collections/nouveaux-arrivages-usage/'
        self.get_genres()
        self.set_last_page()
        self.fetch_links()
        self.fetch_record()
        self.write_new_arrivals()


    def fetch_links(self) -> None:
        fetch_links = FetchRecordLinks(f'{self.base_url}{self.category}?sort_by=title-ascending&page=', self.get_last_page())
        self.product_links = fetch_links.fetch_record_links()
        print(self.product_links)

    def fetch_record(self) -> None:
        for product in self.product_links:
            get_record = GetRecord(product)
            record = get_record.get_record()
            self.records.append(record)

    def write_new_arrivals(self):
        for genre in self.get_genres():
            if genre.startswith("nouveaux-arrivages"):
                self.genre = genre
                self.write_to_file(self.genre, 'New-Arrivals-Used')
                print('test')
        print("Done! New used arrivals have been saved.")

    def write_to_file(self, FILE_NAME, FOLDER):
        with open(f'json/records/{FOLDER}/{FILE_NAME}.json', mode="w", newline="") as jsonFile:
            print(f'Writing {FILE_NAME} to file...')
            json.dump(self.records, jsonFile)
        print(f"File written: {FILE_NAME}")

    def get_genres(self) -> list:
        get_genres = GetGenres(f'{self.base_url}{self.category}')
        return get_genres.get_genres()

    def set_last_page(self) -> None:
        set_last_page = SetLastPage(f'{self.base_url}{self.category}{self.genre}?sort_by=title-ascending&page=1')
        self.last_page = set_last_page.set_last_page()

    def get_last_page(self) -> int:
        return int(self.last_page)


if __name__ == '__main__':
    vinyls = WriteUsedVinyl()
