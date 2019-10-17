from discord.ext import commands


class Money(commands.Cog):

    def _init_(self, client):
        self.client = client


def setup(client):
    client.add_cog(Money(client))
