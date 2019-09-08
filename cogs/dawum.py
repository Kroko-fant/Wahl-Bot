import json
import urllib
from urllib import request

from discord.ext import commands

url = "https://api.dawum.de/"
response = urllib.request.urlopen(url)
data = json.loads(response.read())
print(data)


class Moderation(commands.Cog):

    def _init_(self, client):
        self.client = client


def setup(client):
    client.add_cog(Moderation(client))
