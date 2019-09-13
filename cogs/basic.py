from discord.ext import commands


class Basic(commands.Cog):

    def _init_(self, client):
        self.client = client

    # Events
    # @commands.Cog.listener()

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(client.latency * 1000)} ms')


def setup(client):
    client.add_cog(Basic(client))
