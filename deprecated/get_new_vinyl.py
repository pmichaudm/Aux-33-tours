import random
import csv
import os
import pandas as pd



class GetVinyl:

    pd.set_option('display.max_colwidth', None)  # display full text in console

    def __init__(self):
        self.name = None
        self.price = None
        self.link = None
        self.genre = None
        self.df = None

    def set_random_vinyl(self):
        # random_file = random.choice(os.listdir('csv/records/New-Arrivals'))
        new_arrivals = [filename for filename in os.listdir('../csv/records/New-Arrivals/') if filename.startswith("nouveaux-arrivages")]
        # print(new_arrivals[0])
        with open(f'csv/records/New-Arrivals/{new_arrivals[0]}', 'r') as f:
            reader = csv.DictReader(f)
            self.df = pd.DataFrame(reader, columns=['name', 'price', 'link', 'genre'])
            self.df = self.df.sample()
            self.name = self.df['name'].to_string(index=False, header=False)     # get name of record / removes index num and header
            self.price = self.df['price'].to_string(index=False, header=False)
            self.link = self.df['link'].to_string(index=False, header=False)
            self.genre = self.df['genre'].to_string(index=False, header=False)

    def get_new_arrival_dict(self) -> dict:
        record = {'name': self.name, 'price': self.price, 'link': self.link, 'genre': self.genre}
        return record

    def run(self):
        self.set_random_vinyl()


if __name__ == '__main__':
    GetVinyl().run()
