from discord.ext import commands


def botowner(ctx):
    return ctx.author.id == 137291894953607168


class Basic(commands.Cog):

    def _init_(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)} ms')


def setup(client):
    client.add_cog(Basic(client))
