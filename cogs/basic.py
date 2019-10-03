import json

from discord.ext import commands

from botdata import botparameters as b
from botdata import botparameters as bp


class Basic(commands.Cog):

    def _init_(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)} ms')

    @commands.command()
    async def version(self, ctx):
        await ctx.send("Der Bot läuft auf " + bp.version + ". Die API läuft auf Version " + bp.apiversion())

    @commands.command()
    async def bug(self, ctx, *, bug):
        with open('./botdata/bugs.json', 'r') as f:
            bugs = json.load(f)
            bugtext = str(ctx.author.id), bug
        bugs[str(b.today)] = bugtext

        with open('./botdata/bugs.json', 'w') as f:
            json.dump(bugs, f, indent=4)

        await ctx.send('Danke <@' + str(ctx.author.id) + '> für das einreichen deines Bugs, wir melden uns zurück.')


def setup(client):
    client.add_cog(Basic(client))
