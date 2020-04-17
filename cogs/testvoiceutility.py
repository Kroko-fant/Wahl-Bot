import json

import discord
from discord.ext import commands

from botdata import botparameters as bp


class Voiceutility2(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addintelligentlounge(self, ctx, channelid):
        await bp.delete_cmd(ctx)
        with open('./data/channel/voicechannel.json', 'r') as f:
            channels = json.load(f)
        guildchannels = channels.get(ctx.guild.id)
        for lists in guildchannels:
            if channelid in lists:
                await ctx.send(discord.Embed(title="Error #VU01",
                                             description="Channel kann nicht hinzugefügt werden, da dieser bereits im "
                                                         "System vorhanden ist.", color=0xff0000))
                return
        else:
            guildchannels.append([channelid])
            with open('./data/channel/voicechannel.json', 'w') as f:
                json.dump(guildchannels, f, indent=4)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            channel = after.channel
            if len(channel.members) == 1:
                await channel.guild.create_voice_channel(channel.name, overwrites=channel.overwrites,
                                                         category=channel.category, reason="Auto-Create")

        if after.channel is None and before.channel is not None:
            guild = before.channel.guild
            for liste in self.channels[str(guild)]:
                if after.channel in liste:


def setup(client):
    client.add_cog(Voiceutility2(client))
