from discord.ext import commands


class Logging(commands.cog):

    def _init_(self, client):
        self.client = client

        @commands.Cog.listener()
        async def


def setup(client):
    client.addcog(Logging(client))
