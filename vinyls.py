import random
import csv
import os
import pandas as pd


class Vinyls:

    pd.set_option('display.max_colwidth', None)  # display full text in console

    def __init__(self):
        self.link = None
        self.price = None
        self.name = None
        self.df = None

    def set_random_vinyl(self):
        random_file = random.choice(os.listdir('csv/records/New-Arrivals'))
        with open(f'csv/records/New-Arrivals/{random_file}', 'r', encoding="utf8") as f:
            reader = csv.DictReader(f)
            self.df = pd.DataFrame(reader, columns=['name', 'price', 'link'])
            self.df = self.df.sample()
            self.name = self.df['name'].to_string(index=False, header=False)     # get name of record / removes index num and header
            self.price = self.df['price'].to_string(index=False, header=False)
            self.link = self.df['link'].to_string(index=False, header=False)

    def get_new_arrival_dict(self) -> dict:
        return self.df.to_dict()

    def get_new_arrival(self) -> str:
        return f"{self.name}\n" \
               f"{self.price}\n" \
               f"{self.link}\n"

    def run(self):
        self.set_random_vinyl()


if __name__ == '__main__':
    Vinyls().run()
