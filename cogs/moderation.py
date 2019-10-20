from ast import Pass

import discord
from discord.ext import commands

from botdata import blacklist as bl
from botdata import botparameters as bp


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=100):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await bp.delete_cmd(ctx)
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await bp.delete_cmd(ctx)
        await member.ban(reason=reason)

    @commands.Cog.listener()
    async def on_message(self, message):
        member = message.author
        if bp.user(member):
            if any([curse in message.content.lower() for curse in bl.blacklist]):
                await message.delete()
                await message.channel.send(f"{message.author.mention}, du meintest wohl https://discord.gg/HFQX3Gz")
                return True
            else:
                Pass
        else:
            Pass


def setup(client):
    client.add_cog(Moderation(client))
