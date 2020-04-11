from discord.ext import commands


class Xp(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Xp(client))
