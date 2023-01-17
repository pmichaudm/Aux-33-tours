import csv
import os
import nextcord
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nextcord.ext import commands
from nextcord import Interaction
from datetime import datetime

from buttons.add_to_wishlist import AddToWishlist
from buttons.save_item_to_wishlist import SaveToWishlist
from scripts.get_image import GetImage


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class Used(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="used", description="Fetch a random used vinyl from the new arrivals page", guild_ids=[serverID])
    async def used(self, interaction: Interaction):
        vinyl = GetUsedVinyl()
        vinyl.run()
        vinyl_dict = vinyl.get_used_arrival_dict()
        record_info = ''
        if vinyl_dict['info'] is None:
            record_info = ""
        elif vinyl_dict['info'] is not None:
            record_info = f'''Info: {vinyl_dict['info']}'''
        simple_record = {'name': vinyl_dict['name'], 'price': vinyl_dict['price'], 'link': vinyl_dict['link'],
                         'genre': vinyl_dict['genre']}
        view = AddToWishlist(simple_record)
        wishlist = SaveToWishlist(view.user_id)
        wishlist.save_item(simple_record)
        thumbnail = 'https://i.imgur.com/NmA0Ads.png'
        embed = nextcord.Embed(title=vinyl_dict['name'],
                               description=f"Genre: {vinyl_dict['genre']}\nLabel: {vinyl_dict['label']}\nCountry: {vinyl_dict['country']}\nCatalog #: {vinyl_dict['catalog']}\nRecord condition: {vinyl_dict['grade']}\nSleeve condition: {vinyl_dict['sleeve']}\n{record_info}\n\n{vinyl_dict['price']}",
                               url=vinyl_dict['link'], color=1079206)
        embed.set_thumbnail(thumbnail)
        embed.set_image(self.get_image(vinyl_dict['link']))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
        if view.value is None:
            print("View timed out")
            return
        elif view.value:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(
                f'''[{current_time}] - {interaction.user.id} ({interaction.user}) added: {vinyl_dict['name']} to their wishlist! {vinyl_dict['link']}''')

    def get_image(self, link: str):
        get_image = GetImage(link)
        return get_image.get_image()


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
        new_arrivals = [filename for filename in os.listdir('csv/records/New-Arrivals-Used/') if filename.startswith("nouveaux-arrivages")]
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
            f.close()

    def get_used_arrival_dict(self) -> dict:
        record = {'name': self.record_name,
                  'price': self.record_price,
                  'link': self.record_link,
                  'genre': self.record_genre,
                  'label': self.record_label,
                  'country': self.record_country,
                  'catalog': self.record_cat,
                  'grade': self.record_grade,
                  'sleeve': self.sleeve_grade,
                  'info': self.record_info}
        return record

    def run(self):
        self.set_random_vinyl()


def setup(client):
    client.add_cog(Used(client))
