import os
import nextcord
import requests
from bs4 import BeautifulSoup
from nextcord.ext import commands
from nextcord import Interaction
from buttons.save_item_to_wishlist import SaveToWishlist
from scripts.fetch_record_links import FetchRecordLinks
from scripts.get_record_dict import GetRecord
from scripts.set_last_page import SetLastPage

#TODO - Create a class to fetch record links instead of repeating code
#TODO - Modify New and Used to use the get_record_dict.py script

def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


def get_image(link: str):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "lxml")
    image = soup.find_all('meta', property='og:image', content=True)
    for img in image:
        return img["content"]


class Search(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client
        self.headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}
        self.url = ''
        self.base_url = 'https://aux33tours.com'
        self.page_numbers = []
        self.last_page = 1
        self.product_link = ''
        self.product_links = []
        self.records = []
        self.product_list = []
        self.record = []
        self.urlButton = None

    @nextcord.slash_command(name="search",
                            description="Search for something and get the number of results and the link.",
                            guild_ids=[serverID])
    async def search(self, interaction: Interaction, search: str):
        add_to_wishlist = SaveToWishlist(interaction.user.id)
        new_string = search.replace(" ", "+")
        self.url = f"https://aux33tours.com/search?type=product&q={new_string}*&page=1"
        records = self.get_results()
        current_page = 0
        embed = self.get_record_page(records, current_page)

        async def previous_callback(interaction: Interaction):
            nonlocal current_page, sent_msg
            if current_page == 0:
                current_page = len(records)
            current_page -= 1
            embed = self.get_record_page(records, current_page)
            wishlistButton.label = "Add to wishlist"
            wishlistButton.disabled = False
            self.urlButton.url = self.record['link']
            await interaction.response.edit_message(embed=embed, view=my_view)

        async def next_callback(interaction: Interaction):
            nonlocal current_page, sent_msg
            current_page += 1
            if current_page == len(records):
                current_page = 0
            embed = self.get_record_page(records, current_page)
            wishlistButton.label = "Add to wishlist"
            wishlistButton.disabled = False
            self.urlButton.url = self.record['link']
            await interaction.response.edit_message(embed=embed, view=my_view)

        async def save_callback(interaction: Interaction):
            nonlocal current_page, sent_msg
            current_page = current_page
            embed = self.get_record_page(records, current_page)
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


        my_view = nextcord.ui.View(timeout=180)
        nextButton = nextcord.ui.Button(label=">", style=nextcord.ButtonStyle.blurple, row=1)
        previousButton = nextcord.ui.Button(label="<", style=nextcord.ButtonStyle.blurple, row=1)
        wishlistButton = nextcord.ui.Button(label="Add to wishlist", style=nextcord.ButtonStyle.green, row=0)
        browseButton = nextcord.ui.Button(label="Browse", style=nextcord.ButtonStyle.gray, url=self.url, row=0)
        self.urlButton = nextcord.ui.Button(label="URL", style=nextcord.ButtonStyle.red, url=self.record['link'], row=0)
        my_view.add_item(wishlistButton)
        my_view.add_item(self.urlButton)
        my_view.add_item(browseButton)
        nextButton.callback = next_callback
        previousButton.callback = previous_callback
        wishlistButton.callback = save_callback

        if len(records) > 1:
            my_view.add_item(previousButton)
            my_view.add_item(nextButton)
        sent_msg = await interaction.response.send_message(embed=embed, ephemeral=True, view=my_view)

    def get_record(self, link: str) -> dict:
        get_record = GetRecord(link)
        self.record = get_record.get_record()
        return self.record

    def get_purged_record(self):
        purged_record = {
                "name": self.record['name'],
                "price": self.record['price'],
                "link": self.record['link'],
                "genre": self.record['genre']
            }
        return purged_record

    def get_results(self):
        self.set_last_page()
        get_links = FetchRecordLinks(self.url, self.last_page)
        return get_links.fetch_record_links()

    def set_last_page(self) -> None:
        set_last_page = SetLastPage(self.url)
        self.last_page = set_last_page.set_last_page()

    def get_last_page(self) -> int:
        return int(self.last_page)

    def get_record_page(self, records: list, page_number: int):
        self.get_record(records[page_number])
        name = self.record['name']
        if name.__contains__('Vinyle Usagé') or name.__contains__('45-Tours Usagé'):
            if self.record['record_info'] == '':
                self.record_info = ''
            else:
                self.record_info = f"**Info:** {self.record['record_info']}\n"
        embed = None
        if len(records) != 0:
            if name.__contains__('Vinyle Neuf'):
                embed = nextcord.Embed(title=name, description=f"**Genre:** {self.record['genre']}\n\n{self.record['price']}", url=self.record['link'], color=0x000000)
            if name.__contains__('Vinyle Usagé') or name.__contains__('45-Tours Usagé'):
                embed = nextcord.Embed(title=name, description=f"**Genre:** {self.record['genre']}\n"
                                                               f"**Label:** {self.record['record_label']}\n"
                                                               f"**Country:** {self.record['record_country']}\n"
                                                               f"**Catalog #:** {self.record['record_cat']}\n"
                                                               f"**Record condition:** {self.record['record_grade']}\n"
                                                               f"**Sleeve condition:** {self.record['sleeve_grade']}\n"
                                                               f"{self.record['record_info']}\n"
                                                               f"{self.record['price']}", url=self.record['link'], color=0x000000)
            thumbnail = 'https://i.imgur.com/NmA0Ads.png'
            embed.set_footer(text=f'''Result {page_number + 1} out of {len(records)}''', icon_url=thumbnail)
            embed.set_image(get_image(self.record['link']))
            embed.set_thumbnail(thumbnail)

        else:
            embed = nextcord.Embed(title="There are no results for your search",
                                   description="Try to search for something else or try again at a later time!",
                                   color=0x00ff00)
        return embed


def setup(client):
    client.add_cog(Search(client))
