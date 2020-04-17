import json

from discord.ext import commands, tasks

from botdata import botparameters as bp


class Autobumper(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open("./data/channel/bumpchannels.json", 'r') as f:
            self.channels = json.load(f)
        self.bump.start()

    def cog_unload(self):
        self.bump.cancel()

    @tasks.loop(hours=8.1)
    async def bump(self):
        for ch in self.channels.values():
            channel = self.client.get_channel(ch)
            await channel.send("dlm!bump")

    @bump.before_loop
    async def before_loop(self):
        await self.client.wait_until_ready()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def setbumpchannel(self, ctx, channelid):
        self.channels[str(ctx.guild.id)] = int(channelid)
        with open("./data/channel/bumpchannels.json", 'w') as f:
            json.dump(self.channels, f)
        await bp.delete_cmd(ctx)
        await ctx.send("Bumpchannel erfolgreich gesetzt!")


def setup(client):
    client.add_cog(Autobumper(client))
