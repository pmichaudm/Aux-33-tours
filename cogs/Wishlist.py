import csv
import os

import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from nextcord.ui import Button, View


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class Wishlist(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="wishlist", description="The bot will send you your wishlist", guild_ids=[serverID])
    async def wishlist(self, interaction: Interaction):
        # TODO: Create a function that sends the user their wishlist
        user_wishlist = self.read_wishlist(interaction.user.id)
        user_file = self.get_user_wishlist(interaction.user.id)
        wishlist_pages = self.set_wishlist_pages(user_wishlist)
        embed = None
        wishlist_page = self.set_wishlist_page(0, wishlist_pages)
        embed = self.get_wishlist_page(interaction.user.name, user_wishlist, wishlist_page, wishlist_pages)
        current_page = 0

        async def previous_callback(interaction: Interaction):
            nonlocal current_page, sent_msg
            if current_page == 0:
                current_page = len(wishlist_pages)
            current_page -= 1
            wishlist_page = self.set_wishlist_page(current_page, wishlist_pages)
            embed = self.get_wishlist_page(interaction.user.name, user_wishlist, wishlist_page, wishlist_pages)
            await interaction.response.edit_message(embed=embed)

        async def next_callback(interaction: Interaction):
            nonlocal current_page, sent_msg
            current_page += 1
            if current_page == len(wishlist_pages):
                current_page = 0
            wishlist_page = self.set_wishlist_page(current_page, wishlist_pages)
            embed = self.get_wishlist_page(interaction.user.name, user_wishlist, wishlist_page, wishlist_pages)
            await interaction.response.edit_message(embed=embed)


        nextButton = nextcord.ui.Button(label=">", style=nextcord.ButtonStyle.blurple)
        nextButton.callback = next_callback
        previousButton = nextcord.ui.Button(label="<", style=nextcord.ButtonStyle.blurple)
        previousButton.callback = previous_callback
        my_view = nextcord.ui.View(timeout=180)
        my_view.add_item(previousButton)
        my_view.add_item(nextButton)
        sent_msg = await interaction.response.send_message(embed=embed, ephemeral=True, view=my_view)

    def read_wishlist(self, user_id: int) -> list:
        user_wishlist = []
        is_empty = True
        FILE_NAME = f"csv/users/wishlists/{user_id}.csv"
        if not file_exists(FILE_NAME):
            with open(FILE_NAME, "w") as f:
                print(f'Creating {FILE_NAME} and writing to file...')
                fieldnames = (["name", "price", "link", "genre"])
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                f.close()
        if file_exists(FILE_NAME):
            with open(f"csv/users/wishlists/{user_id}.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row != 0:
                        is_empty = False
                        user_wishlist.append(row)
                if is_empty is True:
                    print("User wishlist is empty")
                    return []
                f.close()
        return user_wishlist

    def get_user_wishlist(self, user_id: int):
        user_file = nextcord.File(f"csv/users/wishlists/{user_id}.csv",
                                  filename=f'''{user_id}'s wishlist.csv''')
        return user_file

    def set_wishlist_pages(self, user_wishlist: list) -> list:
        wishlist_number_pages = (len(user_wishlist) - 1) / 10
        rows, cols = (wishlist_number_pages.__ceil__(), 10)
        wishlist_pages = []
        item_count = 0

        for i in range(rows):
            col = []
            for j in range(cols):
                try:
                    col.append(user_wishlist[j + item_count])
                except IndexError:
                    col.append(" ")
            item_count += 10
            wishlist_pages.append(col)
        return wishlist_pages

    def set_wishlist_page(self, page_number: int, wishlist_pages: list) -> list:
        wishlist_page = wishlist_pages[page_number]
        return wishlist_page

    def get_wishlist_page(self, user_name: str, user_wishlist: list, wishlist_page: list, wishlist_pages: list):
        if len(user_wishlist) != 0:
            embed = nextcord.Embed(title=f'''{user_name}'s wishlist''', color=0x00ff00)
            for item in wishlist_page:
                if item != " ":
                    embed.add_field(name=f'''{item['name']}''', value=f'''[{item['price']} 🔗]({item['link']})''',
                                    inline=False)
            embed.set_footer(text=f'''Page {wishlist_pages.index(wishlist_page) + 1}/{len(wishlist_pages)}''')

        else:
            embed = nextcord.Embed(title="Your wishlist is empty!",
                                   description="Add some records to your wishlist by clicking the button on the record embed!",
                                   color=0x00ff00)
        return embed


def setup(client):
    client.add_cog(Wishlist(client))
