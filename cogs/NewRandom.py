import json
import os
import nextcord
import requests
from random import randint
from bs4 import BeautifulSoup
from nextcord.ext import commands
from nextcord import Interaction
from datetime import datetime
from buttons.add_to_wishlist import AddToWishlist
from buttons.save_item_to_wishlist import SaveToWishlist


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class NewRandom(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name='random_new', description='Fetch a random new record from new arrivals', guild_ids=[serverID])
    async def random_new(self, interaction: Interaction):
        record_dict = self.set_random_vinyl()
        record_name = record_dict['name']
        record_price = record_dict['price']
        record_link = record_dict['link']
        record_genre = record_dict['genre']
        view = AddToWishlist(record_dict)
        wishlist = SaveToWishlist(view.user_id)
        wishlist.save_item(record_dict)
        image = self.get_image(record_dict['link'])
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

    @staticmethod
    def get_image(link: str):
        r = requests.get(link)
        soup = BeautifulSoup(r.content, "lxml")
        image = soup.find_all('meta', property='og:image', content=True)
        for img in image:
            return img["content"]

    @staticmethod
    def set_random_vinyl() -> dict:
        new_arrivals = [filename for filename in os.listdir('json/records/New-Arrivals/') if
                        filename.startswith("nouveaux-arrivages")]
        with open(f'json/records/New-Arrivals/{new_arrivals[0]}', 'r') as f:
            data = json.load(f)
            record = data[randint(0, len(data) - 1)]
        return record


def setup(client):
    client.add_cog(NewRandom(client))
