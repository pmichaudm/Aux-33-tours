import json
import os
import nextcord
from random import randint
from nextcord.ext import commands
from nextcord import Interaction
from datetime import datetime
from buttons.add_to_wishlist import AddToWishlist
from buttons.save_item_to_wishlist import SaveToWishlist
from scripts.get_image import GetImage


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class UsedRandom(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="random_used", description="Fetch a random used vinyl from the new arrivals page", guild_ids=[serverID])
    async def random_used(self, interaction: Interaction):
        vinyl_dict = self.set_random_vinyl()
        record_info = ''
        if vinyl_dict['record_info'] is None:
            record_info = ""
        elif vinyl_dict['record_info'] is not None:
            record_info = f'''Info: {vinyl_dict['record_info']}'''
        view = AddToWishlist(vinyl_dict)
        wishlist = SaveToWishlist(view.user_id)
        wishlist.save_item(vinyl_dict)
        thumbnail = 'https://i.imgur.com/NmA0Ads.png'
        embed = nextcord.Embed(title=vinyl_dict['name'],
                               description=f"Genre: {vinyl_dict['genre']}\nLabel: {vinyl_dict['record_label']}\nCountry: {vinyl_dict['record_country']}\nCatalog #: {vinyl_dict['record_cat']}\nRecord condition: {vinyl_dict['record_grade']}\nSleeve condition: {vinyl_dict['sleeve_grade']}\n{record_info}\n\n{vinyl_dict['price']}",
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

    @staticmethod
    def get_image(link: str):
        get_image = GetImage(link)
        return get_image.get_image()

    @staticmethod
    def set_random_vinyl() -> dict:
        new_arrivals = [filename for filename in os.listdir('json/records/New-Arrivals-Used/') if filename.startswith("nouveaux-arrivages")]
        with open(f'json/records/New-Arrivals-Used/{new_arrivals[0]}', 'r') as f:
            data = json.load(f)
            record = data[randint(0, len(data) - 1)]
        return record


def setup(client):
    client.add_cog(UsedRandom(client))
