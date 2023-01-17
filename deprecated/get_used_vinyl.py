import random
import csv
import os
import pandas as pd


class GetUsedVinyl:

    pd.set_option('display.max_colwidth', None)  # display full text in console

    def __init__(self):
        self.record_name: str = ""
        self.record_price: str = ""
        self.record_link: str = ""
        self.record_genre: str = ""
        self.record_label: str = ""
        self.record_country: str = ""
        self.record_cat: str = ""
        self.record_grade: str = ""
        self.sleeve_grade: str = ""
        self.record_info: str = ""
        self.df = None

    def set_random_vinyl(self):
        # random_file = random.choice(os.listdir('csv/records/New-Arrivals'))
        new_arrivals = [filename for filename in os.listdir('../csv/records/New-Arrivals-Used/') if filename.startswith("nouveaux-arrivages")]
        # print(new_arrivals[0])
        with open(f'csv/records/New-Arrivals-Used/{new_arrivals[0]}', 'r') as f:
            reader = csv.DictReader(f)
            self.df = pd.DataFrame(reader, columns=['name', 'price', 'link', 'genre', 'label', 'country', 'catalog', 'grade', 'sleeve', 'info']).sample()
            self.record_name = self.df['name'].to_string(index=False, header=False)     # get name of record / removes index num and header
            self.record_price = self.df['price'].to_string(index=False, header=False)
            self.record_link = self.df['link'].to_string(index=False, header=False)
            self.record_genre = self.df['genre'].to_string(index=False, header=False)
            self.record_label = self.df['label'].to_string(index=False, header=False)
            self.record_country = self.df['country'].to_string(index=False, header=False)
            self.record_cat = self.df['catalog'].to_string(index=False, header=False)
            self.record_grade = self.df['grade'].to_string(index=False, header=False)
            self.sleeve_grade = self.df['sleeve'].to_string(index=False, header=False)
            self.record_info = self.df['info'].to_string(index=False, header=False)

    def get_used_arrival_dict(self) -> dict:
        record = {'name': self.record_name, 'price': self.record_price, 'link': self.record_link, 'genre': self.record_genre, 'label': self.record_label, 'country': self.record_country, 'catalog': self.record_cat, 'grade': self.record_grade, 'sleeve': self.sleeve_grade, 'info': self.record_info}
        return record

    def run(self):
        self.set_random_vinyl()


if __name__ == '__main__':
    GetUsedVinyl().run()
