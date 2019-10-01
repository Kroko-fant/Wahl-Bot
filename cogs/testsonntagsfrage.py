from discord.ext import commands

votes = 0


async def verifiziert(ctx):
    with open('./data/verified.json', 'r') as f:
        trueuserid = str(ctx.author.id) + '": true'
        data = f.read()
        if trueuserid in data:
            return True
        else:
            return False


class Sontagsumfrage(commands.cog):
    def _init_(self, client):
        self.client = client

    @commands.check(verifiziert)
    @commands.command()
    async def vote(self, ctx):
        await ctx.send("Dein Vote ist eingegangen!")


def setup(client):
    client.add_cog(Sontagsumfrage(client))
