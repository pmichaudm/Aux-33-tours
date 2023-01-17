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


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class New(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name='new', description='Fetch a random new record from new arrivals', guild_ids=[serverID])
    async def new(self, interaction: Interaction):
        vinyl = GetVinyl()
        vinyl.run()
        vinyl_dict = vinyl.get_new_arrival_dict()
        record_name = vinyl_dict['name']
        record_price = vinyl_dict['price']
        record_link = vinyl_dict['link']
        record_genre = vinyl_dict['genre']
        view = AddToWishlist(vinyl_dict)
        wishlist = SaveToWishlist(view.user_id)
        wishlist.save_item(vinyl_dict)
        image = self.get_image(vinyl_dict['link'])
        thumbnail = 'https://i.imgur.com/NmA0Ads.png'
        embed = nextcord.Embed(title=record_name, description=f"Genre: {record_genre}\n\n{record_price}",
                               url=record_link,
                               color=1079206)
        embed.set_thumbnail(thumbnail)
        embed.set_image(image)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(
                f'[{current_time}] - {interaction.user.id} ({interaction.user}) added: {record_name} to their wishlist! {record_link}')

    def get_image(self, link: str):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "lxml")
        image = soup.find_all('meta', property='og:image', content=True)
        for img in image:
            return img["content"]


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
        new_arrivals = [filename for filename in os.listdir('csv/records/New-Arrivals/') if
                        filename.startswith("nouveaux-arrivages")]
        # print(new_arrivals[0])
        with open(f'csv/records/New-Arrivals/{new_arrivals[0]}', 'r') as f:
            reader = csv.DictReader(f)
            self.df = pd.DataFrame(reader, columns=['name', 'price', 'link', 'genre'])
            self.df = self.df.sample()
            self.name = self.df['name'].to_string(index=False, header=False)  # get name of record / removes index num and header
            self.price = self.df['price'].to_string(index=False, header=False)
            self.link = self.df['link'].to_string(index=False, header=False)
            self.genre = self.df['genre'].to_string(index=False, header=False)
            f.close()

    def get_new_arrival_dict(self) -> dict:
        record = {'name': self.name, 'price': self.price, 'link': self.link, 'genre': self.genre}
        return record

    def run(self):
        self.set_random_vinyl()


def setup(client):
    client.add_cog(New(client))
