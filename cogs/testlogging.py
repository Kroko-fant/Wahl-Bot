from discord.ext import commands


class Logging(commands.cog):

    def _init_(self, client):
        self.client = client


def setup(client):
    client.add_cog(Logging(client))
