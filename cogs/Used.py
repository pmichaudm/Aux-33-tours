import csv
import os
import nextcord
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nextcord.ext import commands
from nextcord import Interaction
from datetime import datetime

from buttons import add_to_wishlist
from buttons.add_to_wishlist import AddToWishlist
from buttons.save_item_to_wishlist import SaveToWishlist
from scripts.get_image import GetImage


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class Used(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client
        self.page_number = 0
        self.record = {}

    @nextcord.slash_command(name="used", description="Fetch a random used vinyl from the new arrivals page", guild_ids=[serverID])
    async def used(self, interaction: Interaction):

        embed = self.get_record_page(self.page_number)

        async def previous_callback(interaction: Interaction):
            nonlocal sent_msg
            self.page_number -= 1
            if self.page_number < 0:
                self.page_number = self.total_pages() - 1
            embed = self.get_record_page(self.page_number)
            wishlistButton.label = "Add to wishlist"
            wishlistButton.disabled = False
            await interaction.response.edit_message(embed=embed, view=my_view)

        async def next_callback(interaction: Interaction):
            nonlocal sent_msg
            self.page_number += 1
            if self.page_number > self.total_pages() - 1:
                self.page_number = 0
            embed = self.get_record_page(self.page_number)
            wishlistButton.label = "Add to wishlist"
            wishlistButton.disabled = False
            await interaction.response.edit_message(embed=embed, view=my_view)

        async def save_callback(interaction: Interaction):
            nonlocal sent_msg
            embed = self.get_record_page(self.page_number)
            if not add_to_wishlist.file_exists():
                add_to_wishlist.create_file()
            if add_to_wishlist.is_in_wishlist(self.get_purged_record()):
                wishlistButton.label = "Already in wishlist"
            else:
                add_to_wishlist.save_item(self.get_purged_record())
                add_to_wishlist.save()
                wishlistButton.label = "Saved to wishlist"
            wishlistButton.disabled = True
            await interaction.response.edit_message(embed=embed, view=my_view)

        my_view = nextcord.ui.View()
        nextButton = nextcord.ui.Button(label=">", style=nextcord.ButtonStyle.blurple, row=1)
        previousButton = nextcord.ui.Button(label="<", style=nextcord.ButtonStyle.blurple, row=1)
        wishlistButton = nextcord.ui.Button(label="Add to wishlist", style=nextcord.ButtonStyle.green, row=0)
        my_view.add_item(wishlistButton)
        my_view.add_item(previousButton)
        my_view.add_item(nextButton)
        nextButton.callback = next_callback
        previousButton.callback = previous_callback
        wishlistButton.callback = save_callback
        sent_msg = await interaction.response.send_message(embed=embed, ephemeral=True, view=my_view)

    def get_last_arrivals(self):
        new_arrivals = [filename for filename in os.listdir('csv/records/New-Arrivals-Used/') if
                        filename.startswith("nouveaux-arrivages")]
        return new_arrivals[0]

    def get_record(self) -> None:
        record = {}
        with open(f'csv/records/New-Arrivals-Used/{self.get_last_arrivals()}', 'r') as f:
            csv_reader = csv.DictReader(f)
            rows = list(csv_reader)
            record = rows[self.page_number]
        self.record = record

    def total_pages(self):
        with open(f'csv/records/New-Arrivals-Used/{self.get_last_arrivals()}', 'r') as f:
            csv_reader = csv.DictReader(f)
            rows = list(csv_reader)
            return len(rows)

    def get_record_page(self, page_number: int):
        self.get_record()
        name = self.record['name']
        if name.__contains__('Vinyle Usagé') or name.__contains__('45-Tours Usagé'):
            if self.record['record_info'] == '':
                self.record_info = ''
            else:
                self.record_info = f"**Info:** {self.record['record_info']}\n"
        embed = None
        if name.__contains__('Vinyle Usagé') or name.__contains__('45-Tours Usagé'):
            embed = nextcord.Embed(title=name, description=f"**Genre:** {self.record['genre']}\n"
                                                           f"**Label:** {self.record['record_label']}\n"
                                                           f"**Country:** {self.record['record_country']}\n"
                                                           f"**Catalog #:** {self.record['record_cat']}\n"
                                                           f"**Record condition:** {self.record['record_grade']}\n"
                                                           f"**Sleeve condition:** {self.record['sleeve_grade']}\n"
                                                           f"{self.record_info}\n"
                                                           f"{self.record['price']}", url=self.record['link'],
                                   color=0x000000)
            thumbnail = 'https://i.imgur.com/NmA0Ads.png'
            embed.set_footer(text=f'''Result {self.page_number + 1} out of {self.total_pages()}''', icon_url=thumbnail)
            get_image = GetImage(self.record['link'])
            embed.set_image(get_image.get_image())
            embed.set_thumbnail(thumbnail)
        else:
            embed = nextcord.Embed(title="There are no new used arrivals!",
                                   description="Try again at a later time!",
                                   color=0x00ff00)
        return embed


def setup(client):
    client.add_cog(Used(client))
