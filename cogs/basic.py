import discord
from discord.ext import commands


def botowner(ctx):
    return ctx.author.id == 137291894953607168


def user(member):
    if not member.bot:
        return True
    else:
        return False


class Basic(commands.Cog):

    def _init_(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)} ms')

    @commands.command()
    async def version(self, ctx):
        await ctx.send("Der Bot läuft auf Pre-Version 1.1.3 ." + "Die API läuft auf Version" + discord.version_info)


def setup(client):
    client.add_cog(Basic(client))
