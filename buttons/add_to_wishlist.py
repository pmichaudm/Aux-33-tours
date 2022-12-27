import nextcord
from buttons.save_item_to_wishlist import SaveToWishlist


class AddToWishlist(nextcord.ui.View):
    def __init__(self, vinyl_dict: dict):
        super().__init__(timeout=None)
        self.user_id = None
        self.value = None
        self.vinyl_dict = vinyl_dict
        self.add_wishlist = None

    @nextcord.ui.button(label="Add to wishlist", style=nextcord.ButtonStyle.green)
    async def add_wishlist(self, button, interaction: nextcord.Interaction):
        self.user_id = interaction.user.id
        self.wishlist = SaveToWishlist(interaction.user.id)
        self.wishlist.save_item(self.vinyl_dict)
        self.msg_id = interaction.message.id
        button1 = [x for x in self.children if x.label == "Add to wishlist"][0]
        if not self.wishlist.file_exists():
            self.wishlist.create_file()
        if not self.wishlist.is_in_wishlist(self.vinyl_dict):
            await interaction.response.send_message(f"Added to wishlist", ephemeral=True)
            button1.label = "Added to wishlist"
            self.wishlist.save()
        elif self.wishlist.is_in_wishlist(self.vinyl_dict):
            interaction.response.send_message(f"Already in wishlist", ephemeral=True)
            button1.label = "Already in wishlist"
        button1.disabled = True
        await interaction.followup.edit_message(message_id=self.msg_id, view=self)
        self.value = True
        self.stop()


# def setup(client):
#     client.add_cog(AddToWishlist(client))


