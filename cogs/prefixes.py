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

        await ctx.send(f'Prefix zu:** {prefix} **geändert', delete_after=bp.deltime)

    # unnötig
    @commands.command()
    async def prefix(self, ctx):
        await bp.delete_cmd(ctx)
        try:
            with open('./data/prefixes.json', 'r') as f:
                prefixes = json.load(f)
            await ctx.send("Dieser Server hat den Prefix: **" + prefixes[str(ctx.guild.id)] + "**")
        except KeyError:
            await ctx.send("Dieser Server hat den Prefix: **!**", delete_after=bp.deltime)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            channel = self.client.get_channel(int(635544300834258995))
            content = "**" + str(message.author) + '** sagt: "' + str(message.content) + '"'
            await channel.send(content)

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.content)
        if "prefix" in str(message.content).lower() and bp.user(message.author):
            print(True)
            channel = message.channel
            with open('./data/prefixes.json', 'r') as f:
                prefixes = json.load(f)
            await channel.send("Dieser Server hat den Prefix: **" + prefixes[str(message.guild.id)] + "**")


def setup(client):
    client.add_cog(Prefixes(client))
