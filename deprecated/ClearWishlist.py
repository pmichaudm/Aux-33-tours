import csv
import os

import nextcord
from nextcord.ext import commands
from nextcord import Interaction



def file_exists(FILE_NAME: str) -> bool:
    return os.path.exists(FILE_NAME)


#
# def setup(client):
#     client.add_cog(ClearWishlist(client))