import csv
import os

import nextcord
import requests
from bs4 import BeautifulSoup
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import Button, View


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class Search(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="search", description="Search for something and get the number of results and the link.",
                          guild_ids=[serverID])
    async def search(self, interaction: Interaction, search: str):
        new_string = search.replace(" ", "+")
        url = f"https://aux33tours.com/search?type=product&q={new_string}*"
        thumbnail = 'https://i.imgur.com/NmA0Ads.png'
        view = View()
        view.add_item(Button(label="URL", style=nextcord.ButtonStyle.link, url=url))
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")
        results = soup.find_all('span', class_='collection__showing-count hidden-pocket hidden-lap')
        result_number: str = ''
        for x in results:
            result_number = x.text.strip()
            result_number = result_number.split('''de''')[1]
            result_number = result_number.split('''résultats''')[0]
            result_number = result_number.strip()
        embed = nextcord.Embed(title=f"Search results for {search}",
                               description=f'{result_number} results found', color=0x00ff00)
        await interaction.response.send_message(embed=embed, view=view)


def setup(client):
    client.add_cog(Search(client))
