import nextcord
from nextcord import Interaction
from nextcord.ext import commands


class Help(commands.Cog):
    serverID = 603653205477425152

    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(name="help", description="Shows a list of commands", guild_ids=[serverID])
    async def help(self, interaction: Interaction):
        embed = nextcord.Embed(title="__**Aux 33 Tours - Command list**__", color=1079206)
        embed.add_field(name="/help", value="Shows this list of commands.", inline=False)
        embed.add_field(name="/new", value="Browse through all new vinyl records from the new arrivals page.", inline=False)
        embed.add_field(name="/used", value="Browse through all used vinyl from the new arrivals page.", inline=False)
        embed.add_field(name="/random_new", value="Fetch a random new vinyl from the new arrivals page.", inline=False)
        embed.add_field(name="/random_used", value="Fetch a random used vinyl from the new arrivals page.", inline=False)
        embed.add_field(name="/search", value="Search for a vinyl record and browse the results.", inline=False)
        embed.add_field(name="/wishlist", value="Shows your wishlist", inline=False)
        embed.add_field(name="/add",
                        value="Add a record to your wishlists from a URL. Input a link to a used or new record.",
                        inline=False)
        embed.add_field(name="/remove",
                        value="Removes a vinyl from your wishlists. You need to input the full name of the record.",
                        inline=False)
        embed.add_field(name="/clear_wishlist", value="Clears your wishlists.", inline=False)
        await interaction.response.send_message(embed=embed)


def setup(client):
    client.add_cog(Help(client))
