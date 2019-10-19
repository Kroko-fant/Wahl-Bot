import json

from discord.ext import commands

from botdata import botparameters as bp


class Prefixes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def newprefix(self, ctx, prefix):
        await bp.delete_cmd(ctx)
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('./data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix zu:** {prefix} **geändert')

    @commands.command()
    async def prefix(self, ctx):
        await bp.delete_cmd(ctx)
        try:
            with open('./data/prefixes.json', 'r') as f:
                prefixes = json.load(f)
            await ctx.send("Dieser Server hat den Prefix: **" + prefixes[str(ctx.guild.id)] + "**")
        except KeyError:
            await ctx.send("Dieser Server hat den Prefix: **!**")


def setup(client):
    client.add_cog(Prefixes(client))
