import os
import threading
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import schedule
import time
from scripts.WriteNew import WriteNewVinyl
from scripts.WriteUsed import WriteUsedVinyl
from scripts.Timer import Timer

TOKEN = 'token.txt'
command_prefix = '/'
intents = nextcord.Intents.all()
client = commands.Bot(intents=intents, command_prefix=command_prefix)


def token():
    with open(TOKEN, "r") as f:
        return f.read()


def admin():
    with open("admin.txt", "r") as f:
        return f.read()


def scheduled_update():
    print("Update scheduler started on thread: " + threading.current_thread().name)
    timer = Timer()

    def writeNewRecords():
        print("Writing new records")
        timer.start()
        WriteNewVinyl()
        elapsedTime = timer.stop()
        print(f"Finished writing new records in {elapsedTime:0.4f} seconds.")

    def writeUsedRecords():
        print("Writing new records")
        timer.start()
        WriteUsedVinyl()
        elapsedTime = timer.stop()
        print(f"Finished writing used records in {elapsedTime:0.4f} seconds.")

    schedule.every().day.at("18:30").do(writeNewRecords)
    schedule.every().day.at("18:40").do(writeUsedRecords)
    while True:
        schedule.run_pending()
        time.sleep(1)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(
        activity=nextcord.Activity(type=nextcord.ActivityType.listening, name="Dark Side of the Moon"))


def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


@client.command()
async def load(interaction: Interaction, extension):
    if interaction.user.id == admin():
        try:
            client.load_extension(f"cogs.{extension}")
            await interaction.send(f"Loaded {extension} cog!")
        except Exception as e:
            await interaction.send(f"Error loading {extension} cog: {e}")


@client.command()
async def unload(interaction: Interaction, extension):
    if interaction.user.id == admin():
        try:
            client.unload_extension(f"cogs.{extension}")
            await interaction.send(f"Unloaded {extension} cog!")
        except Exception as e:
            await interaction.send(f"Error unloading {extension} cog: {e}")


@client.command()
async def reload(interaction: Interaction, extension):
    if interaction.user.id == admin():
        try:
            client.reload_extension(f"cogs.{extension}")
            await interaction.send(f"Reloaded {extension} cog")
        except Exception as e:
            await interaction.send(f"Error reloading {extension} cog: {e}")


@client.command()
async def ping(interaction: Interaction):
    if interaction.user.id == admin():
        for guild in client.guilds:  # guild stands for server
            for channel in guild.channels:
                if isinstance(channel, nextcord.TextChannel):  # Check if channel is a text channel
                    if channel.name == 'comp-sci':
                        await channel.send("Hi")


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def set_channel(interaction: Interaction):
    await interaction.send("Guild: " + str(interaction.guild.id) + " Channel set to: " + str(interaction.channel.id))



initial_extensions = []
for fn in os.listdir("cogs"):
    if fn.endswith(".py"):
        initial_extensions.append(f"cogs.{fn[:-3]}")

if __name__ == "__main__":
    for extension in initial_extensions:
        client.load_extension(extension)
        print(f"Loaded {extension} cog!")
    threading.Thread(target=scheduled_update).start()
    client.run(token())
