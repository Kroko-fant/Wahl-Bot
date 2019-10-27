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
    async def clear(self, ctx, amount=10):
        amount = amount + 1
        await ctx.channel.purge(limit=amount)
        await ctx.send("Es wurden **" + str(amount) + "** Nachrichten gelöscht.", delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await bp.delete_cmd(ctx)
        await member.kick(reason=reason)
        await ctx.send("User **" + str(member) + "** wurde gekickt.", delete_after=bp.deltime)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorcm01embed = discord.Embed(title="Error #CM01",
                                           description="Fehlende NutzerID! Syntax: kick <userid> oder kick @<user>",
                                           color=0xff0000)
            await ctx.send(embed=errorcm01embed, delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await bp.delete_cmd(ctx)
        await member.ban(reason=reason)
        await ctx.send("User **" + str(member) + "** wurde gebannt.", delete_after=bp.deltime)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorcm02embed = discord.Embed(title="Error #CM02",
                                           description="Fehlende NutzerID! Syntax: ban <userid> oder ban @<user>",
                                           color=0xff0000)
            await ctx.send(embed=errorcm02embed, delete_after=bp.deltime)
        elif isinstance(error, commands.BadArgument):
            errorcm03embed = discord.Embed(title="Error #CM03",
                                           description="Nutzer konnte nicht gefunden werden!",
                                           color=0xff0000)
            await ctx.send(embed=errorcm03embed, delete_after=bp.deltime)

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

    @commands.command()
    @commands.check(bp.botowner)
    async def unbanall(self, message):
        guild = message.guild
        bans = await guild.bans()
        counter = len(bans)
        x = 0

        while x < counter:
            await guild.unban(bans[x][1], reason="Unbanall")
            x = x + 1
        await bp.delete_cmd(message)


def setup(client):
    client.add_cog(Moderation(client))
