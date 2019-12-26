import json

from discord.ext import commands

from botdata import botparameters as bp


class Prefixes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def newprefix(self, ctx, prefix='!'):
        """Weißt einen neuen Prefix zu.
        Syntax: {prefix} newprefix <prefix>
        Wird kein prefix angegeben wird ! gesetzt."""
        await bp.delete_cmd(ctx)
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('./data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix zu:** {prefix} **geändert', delete_after=bp.deltime)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if "prefix" in str(ctx.content).lower() and bp.user(ctx.author) and "bot" in str(ctx.content).lower():
            with open('./data/prefixes.json', 'r') as f:
                prefixes = json.load(f)
            await ctx.send("Dieser Server hat den Prefix: **" + prefixes[str(ctx.guild.id)] + "**")


def setup(client):
    client.add_cog(Prefixes(client))
