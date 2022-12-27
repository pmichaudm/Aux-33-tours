import csv
import requests
from bs4 import BeautifulSoup


class Write_used_vinyl:

    def __init__(self) -> None:
        self.filtered_genres: list = []
        self.record_price: float = 0.00
        self.record_name: str = ""
        self.record_genre: str = ""
        self.record_label: str = ""
        self.record_country: str = ""
        self.record_cat: str = ""
        self.record_grade: str = ""
        self.sleeve_grade: str = ""
        self.record_info: str = ""
        self.record_attributes: str = ""
        self.product_list: list = []
        self.last_page: str = ""
        self.headers: dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        self.product_link: str = ""
        self.product_links: list = []
        self.page_numbers: list = []
        self.genre: str = ""
        self.genres: list = []
        self.records: list = []
        self.base_url: str = 'https://aux33tours.com'
        self.category: str = '/collections/nouveaux-arrivages-usage/'
        self.get_genres()
        self.fetch_links()
        self.fetch_record()
        self.write_new_arrivals()


    def fetch_links(self) -> None:
        for page in range(1, 1 + 1): # testing with 1 page
        # for page in range(1, self.get_last_page() + 1):
            print(f'{self.base_url}{self.category}{self.genre}?sort_by=title-ascending&page={page}')
            r = requests.get(f'{self.base_url}{self.category}{self.genre}?sort_by=title-ascending&page={page}')
            soup = BeautifulSoup(r.content, "lxml")
            self.product_list = soup.find_all('div', class_='product-item__info')
            for item in self.product_list:
                for link in item.find_all('a', href=True):
                    self.product_links.append(self.base_url + link['href'])

    def fetch_record(self) -> None:
        for product in self.product_links:
            self.product_link = product
            r2 = requests.get(self.product_link, headers=self.headers)
            soup = BeautifulSoup(r2.content, "lxml")
            self.record_name = soup.find('h1', class_='product-meta__title heading h1').text.strip()
            self.record_name = self.record_name.replace('(Vinyle Usagé)', '')
            self.record_price = soup.find('span', class_='price').text.strip()
            self.record_attributes = soup.find('div', class_='rte text--pull').text.strip()
            self.set_attributes()
            self.set_record_genre()
            self.set_label()
            self.set_country()
            self.set_cat()
            self.set_grade()
            self.set_sleeve_grade()
            self.set_info()
            self.records.append({
                "name": self.record_name,
                "price": self.record_price,
                "link": self.product_link,
                "genre": self.record_genre,
                "label": self.record_label,
                "country": self.record_country,
                "catalog": self.record_cat,
                "grade": self.record_grade,
                "sleeve": self.sleeve_grade,
                "info": self.record_info
            })

    def write_new_arrivals(self):
        self.category = '/collections/nouveaux-arrivages-usage/'
        for genre in self.get_genres():
            if genre.startswith("nouveaux-arrivages"):
                self.genre = genre
                self.write_to_file(self.genre, 'New-Arrivals-Used')
        print("Done! New used arrivals have been saved.")

    def write_to_file(self, FILE_NAME, FOLDER):
        with open(f'csv/records/{FOLDER}/{FILE_NAME}.csv', mode="w", newline="") as csvfile:
            print(f'Writing {FILE_NAME} to file...')
            fieldnames = (['name', 'price', 'link', 'genre', 'label', 'country', 'catalog', 'grade', 'sleeve', 'info'])
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.records)
            csvfile.close()
        print(f"File written: {FILE_NAME}")

    def set_attributes(self):
        self.record_genre = self.record_attributes
        self.record_label = self.record_attributes
        self.record_country = self.record_attributes
        self.record_cat = self.record_attributes
        self.record_grade = self.record_attributes
        self.sleeve_grade = self.record_attributes
        self.record_info = self.record_attributes

    def set_label(self) -> None:
        try:
            self.record_label = self.record_attributes.split('Maison de disque :')[1]
            self.record_label = self.record_label.split('''Pays d'origine :''')[0]
            self.record_label = self.record_label.strip()
            # print(self.record_label)
        except IndexError:
            print("No label found")
            self.record_label = None

    def set_country(self) -> None:
        try:
            self.record_country = self.record_attributes.split('''Pays d'origine :''')[1]
            self.record_country = self.record_country.split('# de catalogue :')[0]
            self.record_country = self.record_country.strip()
            # print(self.record_country)
        except IndexError:
            print("No country found")
            self.record_country = None

    def set_cat(self) -> None:
        try:
            self.record_cat = self.record_attributes.split('# de catalogue :')[1]
            self.record_cat = self.record_cat.split('État du disque :')[0]
            self.record_cat = self.record_cat.strip()
            # print(self.record_cat)
        except IndexError:
            print("No catalog number found")
            self.record_cat = None

    def set_grade(self) -> None:
        try:
            self.record_grade = self.record_attributes.split('État du disque :')[1]
            self.record_grade = self.record_grade.split('(')[0]
            self.record_grade = self.record_grade.split('État de la pochette :')[0]
            self.record_grade = self.record_grade.strip()
            # print(self.record_grade)
        except IndexError:
            print("No record grade found")
            self.record_grade = None

    def set_sleeve_grade(self) -> None:
        self.sleeve_grade = self.record_attributes.split('État de la pochette :')[1]
        try:
            self.sleeve_grade = self.sleeve_grade.split('(')[0]
            self.sleeve_grade = self.sleeve_grade.split('Informations sur le pressage :')[0]
            self.sleeve_grade = self.sleeve_grade.split('Relié à :')[0]
            self.sleeve_grade = self.sleeve_grade.replace('''   Veuillez noter qu'il s'agit d'un produit USAGÉ. La photo affichée est à des fins d'illustrations et ne concorde pas nécessairement à l'état du produit. Veuillez nous contacter si vous souhaitez avoir une photo de l'item en question. Aucun retour n'est possible sur les items usagés.''', '')
        except IndexError:
            self.sleeve_grade = self.sleeve_grade.strip()
        # print(self.sleeve_grade)
        self.sleeve_grade = self.sleeve_grade.strip()

    def set_info(self) -> None:
        try:
            self.record_info = self.record_attributes.split('Informations sur le pressage :')[1]
            self.record_info = self.record_info.split('Veuillez', 1)[0]
            self.sleeve_grade = self.sleeve_grade.split('Relié à :')[0]
            self.record_info = self.record_info.strip()
        except IndexError:
            self.record_info = None
            return

    def set_record_genre(self) -> None:
        try:
            self.record_genre = self.record_genre.split('Genre :')[1]
            self.record_genre = self.record_genre.split('Maison de disque :')[0]
            self.record_genre = self.record_genre.strip()
            # print(self.record_genre)
        except IndexError:
            self.record_genre = None
            print("Genre not found")

    def get_record_genre(self) -> str:
        return self.record_genre

    def get_genres(self) -> list:
        p = requests.get(f'{self.base_url}{self.category}')
        soups = BeautifulSoup(p.content, "lxml")
        genres = soups.find_all('div', class_='checkbox-wrapper')
        for genre in genres:
            for genre_tag in genre.find_all('input'):
                if genre_tag['data-tag'] not in self.genres:
                    self.genres.append(genre_tag['data-tag'])
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
        return int(self.last_page)


if __name__ == '__main__':
    vinyls = Write_used_vinyl()
