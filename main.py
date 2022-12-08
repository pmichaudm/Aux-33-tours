import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from vinyls import Vinyls
import os
from Wishlist import Wishlist
from saveitemtowishlist import SaveItemToWishList

serverID = 603653205477425152
FILE_NAME = 'token.txt'
command_prefix = '/'
intents = nextcord.Intents.all()
# intents.members = True
client = commands.Bot(intents=intents, command_prefix=command_prefix)


def token():
    with open(FILE_NAME, "r") as f:
        return f.read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.slash_command(name='new', description='Fetch a new random record from new arrivals', guild_ids=[serverID])
async def new(interaction: Interaction):
    vinyls = Vinyls()
    await interaction.response.send_message(vinyls)
    print(vinyls)


@client.slash_command(name='test2', description='test command', guild_ids=[serverID])
async def test2(interaction: Interaction):
    vinyl = Vinyls()
    vinyl.run()
    vinyl = vinyl.get_new_arrival()
    # record = Vinyls().get_new_arrival()
    view = Wishlist()
    print(interaction.user.id)
    await interaction.response.send_message(vinyl, view=view)
    await view.wait()

    if view.value is None:
        print("No value")
        return
    elif view.value:
        file_exists = os.path.exists('csv/records/users/wishlists/428198028864913408')
        print(file_exists)
        SaveItemToWishList().save()
        # with open(f'csv/records/users/wishlists/{interaction.user.id}.csv', mode="w", newline="") as csvfile:
        #     print(f'Writing {FILE_NAME} to file...')
        #     records = self.vinyl_link()
        #     fieldnames = (['name', 'price', 'link'])
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #     writer.writeheader()
        #     writer.writerows(records)
        #     csvfile.close()
        # print(f"File written: {FILE_NAME}")
        print('Added to your wishlist!')


client.run(token())
