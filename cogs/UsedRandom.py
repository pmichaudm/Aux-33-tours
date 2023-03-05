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
from scripts.WishlistLog import WishlistLog


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class UsedRandom(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="random_used", description="Fetch a random used vinyl from the new arrivals page", guild_ids=[serverID])
    async def random_used(self, interaction: Interaction):
        record_dict = self.set_random_vinyl()
        record_info = ''
        if record_dict['record_info'] is None:
            record_info = ""
        elif record_dict['record_info'] is not None:
            record_info = f'''Info: {record_dict['record_info']}'''
        view = AddToWishlist(record_dict)
        wishlist = SaveToWishlist(view.user_id)
        wishlist.save_item(record_dict)
        thumbnail = 'https://i.imgur.com/NmA0Ads.png'
        embed = nextcord.Embed(title=record_dict['name'],
                               description=f"Genre: {record_dict['genre']}\nLabel: {record_dict['record_label']}\nCountry: {record_dict['record_country']}\nCatalog #: {record_dict['record_cat']}\nRecord condition: {record_dict['record_grade']}\nSleeve condition: {record_dict['sleeve_grade']}\n{record_info}\n\n{record_dict['price']}",
                               url=record_dict['link'], color=1079206)
        embed.set_thumbnail(thumbnail)
        embed.set_image(self.get_image(record_dict['link']))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        await view.wait()
        if view.value is None:
            return
        elif view.value:
            log = WishlistLog()
            log.add(interaction.user.id, interaction.user, record_dict['name'], record_dict['link'])

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
