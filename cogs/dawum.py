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
        await bp.delete_cmd()
        await ctx.send(embed=dawumoutput)

    @poll.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await bp.delete_cmd()
            await ctx.send(embed=dwa.umfrage_ausgeben('0'))


def setup(client):
    client.add_cog(Dawum(client))
