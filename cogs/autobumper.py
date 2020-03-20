import asyncio

from discord.ext import commands


class Autobumper(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def mytask(self):
        await asyncio.sleep(20)
        print("Processing Task")

    @commands.command()
    async def test(self, ctx):
        asyncio.ensure_future(self.mytask())


def setup(client):
    client.add_cog(Autobumper(client))
