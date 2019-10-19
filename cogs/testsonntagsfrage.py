from discord.ext import commands

from botdata import botparameters as bp

votes = 0


class Sontagsumfrage(commands.cog):
    def __init__(self, client):
        self.client = client

    @commands.check(bp.verifiziert)
    @commands.command()
    async def vote(self, ctx):
        await bp.delete_cmd(ctx)
        await ctx.send("Dein Vote ist eingegangen!")


def setup(client):
    client.add_cog(Sontagsumfrage(client))
