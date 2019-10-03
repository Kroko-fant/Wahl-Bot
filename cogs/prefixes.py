import json

from discord.ext import commands


class Prefixes(commands.Cog):

    def _init_(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('./data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '!'

        with open('./data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    async def newprefix(self, ctx, prefix):
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('./data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'Prefix zu: {prefix} geändert')


def setup(client):
    client.add_cog(Prefixes(client))
