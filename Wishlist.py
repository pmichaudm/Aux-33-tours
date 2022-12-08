import nextcord

class Wishlist(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Add to wishlist", style=nextcord.ButtonStyle.green)
    async def add_wishlist(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"Added to wishlist", ephemeral=True)
        self.value = True
        self.stop()

