import csv
import os
import nextcord
import requests
from bs4 import BeautifulSoup
from nextcord import Interaction
from nextcord.ext import commands
from buttons.save_item_to_wishlist import SaveToWishlist


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


class Wishlist(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client
        self.headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
        }

    @nextcord.slash_command(name="wishlist", description="The bot will send you your wishlist", guild_ids=[serverID])
    async def wishlist(self, interaction: Interaction):
        if not file_exists(f"csv/users/wishlists/{interaction.user.id}.csv"):
            self.create_wishlist(interaction.user.id)
        user_wishlist = self.read_wishlist(interaction.user.id)
        wishlist_pages = self.set_wishlist_pages(user_wishlist)
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

        my_view = nextcord.ui.View(timeout=180)
        if wishlist_pages != []:
            nextButton = nextcord.ui.Button(label=">", style=nextcord.ButtonStyle.blurple)
            nextButton.callback = next_callback
            previousButton = nextcord.ui.Button(label="<", style=nextcord.ButtonStyle.blurple)
            previousButton.callback = previous_callback
            my_view.add_item(previousButton)
            my_view.add_item(nextButton)
        sent_msg = await interaction.response.send_message(embed=embed, ephemeral=True, view=my_view)

    @nextcord.slash_command(name="clearwishlist", description="Clear your wishlist", guild_ids=[serverID])
    async def clearwishlist(self, interaction: Interaction):
        user_file = self.get_user_wishlist(interaction.user.id)
        if file_exists(user_file):
            os.remove(user_file)
            await interaction.response.send_message("Your wishlist has been cleared!", ephemeral=True)
        else:
            await interaction.response.send_message("You don't have a wishlist!", ephemeral=True)


    @nextcord.slash_command(name="remove", description="Remove a record from your wishlist. Make sure to enter the full album name when removing.", guild_ids=[serverID])
    async def remove(self, interaction: Interaction, name: str):
        user_wishlist = self.read_wishlist(interaction.user.id)
        if user_wishlist == []:
            await interaction.response.send_message("Your wishlist is empty!", ephemeral=True)
        else:
            for item in user_wishlist:
                if item["name"] == name:
                    user_wishlist.remove(item)
                    with open (f"csv/users/wishlists/{interaction.user.id}.csv", "w", newline="") as f:
                        fieldnames = (["name", "price", "link", "genre"])
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        for row in user_wishlist:
                            writer.writerow(row)
                        f.close()

                    await interaction.response.send_message("Item removed from wishlist!", ephemeral=True)
                    return
            await interaction.response.send_message("Item not found in wishlist!", ephemeral=True)

    @nextcord.slash_command(name="add", description="Add a record to your wishlist with a link to Aux33tours' website", guild_ids=[serverID])
    async def add(self, interaction: Interaction, link: str):
        if not link.startswith("https://aux33tours.com/"):
            await interaction.response.send_message("Invalid link! Please use a link from Aux 33 Tours", ephemeral=True)
            return
        else:
            await interaction.response.send_message(f"{self.add_user_record(link,interaction.user.id)}", ephemeral=True)


    def add_user_record(self, link: str, user_id) -> str:
        r = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(r.content, "lxml")
        name = soup.find('h1', class_='product-meta__title heading h1').text.strip()
        record_genre = soup.find('div', class_='rte text--pull').text.strip()
        price = soup.find('span', class_='price').text.strip()
        if name.__contains__("Vinyle Usagé"):
            name = name.replace(' (Vinyle Usagé)', '')
            record_genre = record_genre.split('Genre :')[1]
            record_genre = record_genre.split('Maison de disque :')[0]
            record_genre = record_genre.strip()
            link = link.split('?')[0]
            print(name)
            print(price)
            print(record_genre)
            print(link)
            print("Vinyle Usagé detected")
            self.write_record_to_wishlist(name, price, link, record_genre, user_id)
            return "Used record added to your wishlist!"
        elif name.__contains__("Vinyle Neuf"):
            name = name.replace(' (Vinyle Neuf)', '')
            record_genre = record_genre.split('Genre :')[1]
            record_genre = record_genre.split('Relié', 1)[0]
            record_genre = record_genre.split('Veuillez', 1)[0]
            self.write_record_to_wishlist(name, price, link, record_genre, user_id)
            return "New record added to your wishlist!"
        else:
            return "Invalid record link, please provide a link to a used or new record from Aux 33 Tours."


    def write_record_to_wishlist(self, name: str, price: str, link: str, genre: str, user_id) -> None:
        with open(f"csv/users/wishlists/{user_id}.csv", "a", newline="") as f:
            fieldnames = (["name", "price", "link", "genre"])
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({"name": name, "price": price, "link": link, "genre": genre})
            f.close()

    def read_wishlist(self, user_id: int) -> list:
        user_wishlist = []
        is_empty = True
        FILE_NAME = f"csv/users/wishlists/{user_id}.csv"
        if not file_exists(FILE_NAME):
            save_to_wishlist = SaveToWishlist(user_id)
            save_to_wishlist.create_file()
        if file_exists(FILE_NAME):
            with open(f"csv/users/wishlists/{user_id}.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row != 0:
                        is_empty = False
                        user_wishlist.append(row)
                if is_empty is True:
                    # print("User wishlist is empty") #for debugging
                    return []
                f.close()
        return user_wishlist

    def get_user_wishlist(self, user_id: int):
        user_file = f"csv/users/wishlists/{user_id}.csv"
        return user_file

    def set_wishlist_pages(self, user_wishlist: list) -> list:
        if (len(user_wishlist)-1) != 0:
            wishlist_number_pages = (len(user_wishlist) - 1) / 10
            rows, cols = (wishlist_number_pages.__ceil__(), 10)
        else:
            rows, cols = (1, 10)
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

        if wishlist_pages != []:
            return wishlist_pages[page_number]
        else:
            return []

    def get_wishlist_page(self, user_name: str, user_wishlist: list, wishlist_page: list, wishlist_pages: list):
        thumbnail = 'https://i.imgur.com/NmA0Ads.png'
        if len(user_wishlist) != 0:
            embed = nextcord.Embed(title=f'''__**{user_name}'s wishlist - {len(user_wishlist)} items**__''', color=0x00ff00)
            for item in wishlist_page:
                if item != " ":
                    embed.add_field(name=f'''{item['name']}''', value=f'''[{item['price']} 🔗]({item['link']})''',
                                    inline=False)
            embed.set_footer(text=f'''Page {wishlist_pages.index(wishlist_page) + 1}/{len(wishlist_pages)}''', icon_url=thumbnail)


        else:
            embed = nextcord.Embed(title="Your wishlist is empty!",
                                   description="Add some records to your wishlist by clicking the button on the record embed!",
                                   color=0x00ff00)
        return embed


def setup(client):
    client.add_cog(Wishlist(client))
