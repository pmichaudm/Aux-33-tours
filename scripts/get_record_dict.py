import requests
from bs4 import BeautifulSoup


class GetRecord:
    def __init__(self, url: str):
        self.r = requests.get(url)
        self.soup = BeautifulSoup(self.r.content, "lxml")
        self.link = url
        self.record = {}
        self.name = ''
        self.price = ''
        self.record_genre = ''
        self.record_label = ''
        self.record_country = ''
        self.record_cat = ''
        self.record_grade = ''
        self.sleeve_grade = ''
        self.record_info = ''

    def get_record(self) -> dict:
        self.name = self.soup.find('h1', class_='product-meta__title heading h1').text.strip()
        self.price = self.soup.find('span', class_='price').text.strip()
        self.record_genre = self.soup.find('div', class_='rte text--pull').text.strip()
        if self.name.__contains__('Vinyle Neuf'):
            try:
                self.record_genre = self.record_genre.split('Genre :', 1)[1]
            except:
                self.record_genre = "N/A"
            try:
                self.record_genre = self.record_genre.split('Veuillez', 1)[0]
                self.record_genre = self.record_genre.strip()
            except:
                self.record_genre = self.record_genre.strip()
            self.record = ({
                "name": self.name,
                "price": self.price,
                "link": self.link,
                "genre": self.record_genre
            })

        if self.name.__contains__('Vinyle Usagé') or self.name.__contains__('45-Tours Usagé'):
            record_attributes = self.soup.find('div', class_='rte text--pull').text.strip()
            try:
                record_attributes = record_attributes.split('Veuillez', 1)[0]
                record_attributes = record_attributes.split('Relié à :', 1)[0]
            except:
                pass
            try:
                self.record_genre = record_attributes.split('Genre :', 1)[1]
                self.record_genre = self.record_genre.split('Maison', 1)[0]
                self.record_genre.strip()
            except IndexError:
                self.record_genre = 'N/A'
            try:
                self.record_label = record_attributes.split('Maison de disque :')[1]
                self.record_label = self.record_label.split('''Pays d'origine :''')[0]
                self.record_label.strip()
            except IndexError:
                self.record_label = 'N/A'
            try:
                self.record_country = record_attributes.split('''Pays d'origine :''')[1]
                self.record_country = self.record_country.split('# de catalogue :')[0]
                self.record_country.strip()
            except IndexError:
                self.record_country = 'N/A'
            try:
                self.record_cat = record_attributes.split('# de catalogue :')[1]
                self.record_cat = self.record_cat.split('État du disque :')[0]
                self.record_cat.strip()
            except IndexError:
                self.record_cat = 'N/A'
            try:
                self.record_grade = record_attributes.split('État du disque :')[1]
                self.record_grade = self.record_grade.split('(')[0]
                self.record_grade = self.record_grade.split('État de la pochette :')[0]
                self.record_grade.strip()
            except IndexError:
                self.record_grade = 'N/A'
            try:
                self.sleeve_grade = record_attributes.split('État de la pochette :')[1]
                self.sleeve_grade = self.sleeve_grade.split('(')[0]
                self.sleeve_grade.strip()
            except IndexError:
                self.sleeve_grade = 'N/A'
            try:
                self.sleeve_grade = self.sleeve_grade.split('Informations sur le pressage :')[0]
                self.sleeve_grade.strip()
            except IndexError:
                pass
            try:
                self.record_info = record_attributes.split('Informations sur le pressage :')[1]
            except IndexError:
                self.record_info = ''
            self.record = ({
                "name": self.name,
                "price": self.price,
                "link": self.link,
                "genre": self.record_genre,
                "record_label": self.record_label,
                "record_country": self.record_country,
                "record_cat": self.record_cat,
                "record_grade": self.record_grade,
                "sleeve_grade": self.sleeve_grade,
                "record_info": self.record_info
            })
        return self.record
