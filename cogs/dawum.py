import discord
from discord.ext import commands

from botdata import botparameters as bp
from botdata import dawumapi as dwa


class Dawum(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def poll(self, ctx, pollinput):
        if pollinput is None:
            pollinput = 0
            dawumoutput = dwa.umfrage_ausgeben(pollinput)
            await bp.delete_cmd(ctx)
            await ctx.send(embed=dawumoutput)
        elif pollinput == "help":
            await bp.delete_cmd(ctx)
            wahlhelfembed = discord.Embed(title=str("Hilfe zum Befehl !poll"),
                                          description="Verwendung: !poll oder !poll <Argument>. Als Argumente sind "
                                                      "Länderkürzel, Namen o.ä. zugelassen", color=12370112)
            await ctx.send(embed=wahlhelfembed, delete_after=bp.deltime)
        else:
            dawumoutput = dwa.umfrage_ausgeben(pollinput)
            await bp.delete_cmd(ctx)
            await ctx.send(embed=dawumoutput)

    @commands.command()
    @commands.check(bp.botowner)
    async def lastupdate(self, ctx):
        dwa.update_data()
        await ctx.send(dwa.lastupdate)

    @poll.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await bp.delete_cmd(ctx)
            await ctx.send(embed=dwa.umfrage_ausgeben('0'))


def setup(client):
    client.add_cog(Dawum(client))
