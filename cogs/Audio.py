import json
import os
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from buttons.save_item_to_wishlist import SaveToWishlist
from scripts.WishlistLog import WishlistLog
from scripts.GetImage import GetImage


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class Audio(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client
        self.page_number = 0
        self.audio = {}


    @nextcord.slash_command(name="audio", description="Browse through all the audio equipment", guild_ids=[serverID])
    async def audio(self, interaction: Interaction):

        embed = self.getAudioPage(self.page_number)
        save = SaveToWishlist(interaction.user.id)
        async def previous_callback(interaction: Interaction):
            nonlocal sent_msg
            self.page_number -= 1
            if self.page_number < 0:
                self.page_number = self.total_pages() - 1
            embed = self.getAudioPage(self.page_number)
            wishlistButton.label = "Add to wishlist"
            wishlistButton.disabled = False
            await interaction.response.edit_message(embed=embed, view=my_view)

        async def next_callback(interaction: Interaction):
            nonlocal sent_msg
            self.page_number += 1
            if self.page_number > self.total_pages() - 1:
                self.page_number = 0
            embed = self.getAudioPage(self.page_number)
            wishlistButton.label = "Add to wishlist"
            wishlistButton.disabled = False
            await interaction.response.edit_message(embed=embed, view=my_view)

        async def save_callback(interaction: Interaction):
            nonlocal sent_msg
            embed = self.getAudioPage(self.page_number)
            if not save.file_exists():
                save.create_file()
            if save.is_in_wishlist(self.audio):
                wishlistButton.label = "Already in wishlist"
            else:
                save.save_item(self.audio)
                save.save()
                wishlistButton.label = "Saved to wishlist"
                log = WishlistLog()
                log.add(interaction.user.id, interaction.user, self.audio['name'], self.audio['link'])
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


    def get_record(self) -> None:
        audio = {}
        with open(f'json/equipment/AudioEquipment.json', 'r') as f:
            data = json.load(f)
            audio = data[self.page_number]
        self.audio = audio

    def total_pages(self):
        with open(f'json/equipment/AudioEquipment.json', 'r') as f:
            data = json.load(f)
            return len(data)

    def getAudioPage(self, page_number: int):
        if(self.total_pages()==0):
            return nextcord.Embed(title="No audio equipment found", description="There is no audio equipment in the database", color=0x000000)
        self.get_record()
        name = self.audio['name']
        description = self.audio['description'].replace('\n', '\n\n')
        embed = nextcord.Embed(title=name, description=f"{self.audio['price']}\n\n{description}", url=self.audio['link'], color=0x000000)
        thumbnail = 'https://i.imgur.com/NmA0Ads.png'
        embed.set_footer(text=f'''Result {self.page_number + 1} out of {self.total_pages()}''', icon_url=thumbnail)
        get_image = GetImage(self.audio['link'])
        embed.set_image(get_image.get_image())
        embed.set_thumbnail(thumbnail)
        return embed


def setup(client):
    client.add_cog(Audio(client))
