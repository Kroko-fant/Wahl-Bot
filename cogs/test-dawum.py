import json
import urllib
from urllib import request

from discord.ext import commands

url = "https://api.dawum.de/"
response = urllib.request.urlopen(url)
data = json.loads(response.read())
print(data)


class Dawum(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Dawum(client))
