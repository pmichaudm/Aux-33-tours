import os
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

TOKEN = 'token.txt'
command_prefix = '/'
intents = nextcord.Intents.all()
client = commands.Bot(intents=intents, command_prefix=command_prefix)


def token():
    with open(TOKEN, "r") as f:
        return f.read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


@client.command()
async def load(interaction: Interaction, extension):
    client.load_extension(f"cogs.{extension}")
    await interaction.send(f"Loaded {extension} cog!")


@client.command()
async def unload(interaction: Interaction, extension):
    client.unload_extension(f"cogs.{extension}")
    await interaction.send(f"Unloaded {extension} cog!")


@client.command()
async def reload(interaction: Interaction, extension):
    client.reload_extension(f"cogs.{extension}")
    await interaction.send(f"Reloaded {extension} cog")


initial_extensions = []
for fn in os.listdir("cogs"):
    if fn.endswith(".py"):
        initial_extensions.append(f"cogs.{fn[:-3]}")

if __name__ == "__main__":
    for extension in initial_extensions:
        client.load_extension(extension)
        print(f"Loaded {extension} cog!")
    client.run(token())


