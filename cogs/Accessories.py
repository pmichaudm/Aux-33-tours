import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class Accessories(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="accessories", description="Shows a list of commands", guild_ids=[serverID])
    async def accessories(self, interaction: Interaction):
        await interaction.response.send_message("This command is not yet implemented.")


def setup(client):
    client.add_cog(Accessories(client))