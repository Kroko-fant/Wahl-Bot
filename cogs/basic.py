import asyncio

import discord
from discord.ext import commands

from botdata import botparameters as bp


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def version(self, ctx):
        """Zeigt die aktuelle Bot-Version."""
        await bp.delete_cmd(ctx)
        await ctx.send(f'Der Bot läuft auf :eyes~1: **Version Beta 1.3.4a**. '
                       f'Die API läuft auf Version :mailbox: **{discord.__version__}**', delete_after=bp.deltime)

    @commands.command()
    async def bug(self, ctx, *, bugt):
        """"Reiche einen Bug ein.
        Syntax: {Prefix}bug <bugtext>"""
        channel = self.client.get_channel(int(643546804750909454))
        if 1800 >= len(bugt) >= 1:
            await channel.send(f"**Bug von {ctx.author} ({ctx.author.id}):**{bugt}")
            await bp.delete_cmd(ctx)
            await ctx.send(f'Danke <@{ctx.author.id}> für das einreichen deines Bugs, wir melden uns zurück.',
                           delete_after=bp.deltime)
        else:
            await ctx.send("Dein Bug darf maximal 1800 Zeichen lang sein.", delete_after=bp.deltime)

    @commands.command()
    async def feedback(self, ctx, *, feedbackt):
        """Reiche Feedback ein
        Syntax; {Prefix}feedback <feedbacktext>"""
        channel = self.client.get_channel(int(643540415919816717))
        if 1800 >= len(feedbackt) >= 1:
            await channel.send(f'**Feedback von {ctx.author} ({ctx.author.id}):**  {feedbackt}')
            await bp.delete_cmd(ctx)
            await ctx.send(f'Danke <@{ctx.author.id}> für das einreichen deines Feedbacks, wir melden uns zurück.',
                           delete_after=bp.deltime)
        else:
            await ctx.send("Dein Feedback darf maximal 1800 Zeichen umfassen.")

    @commands.command()
    async def about(self, ctx):
        """Zeigt Informationen über den Bot an."""
        await bp.delete_cmd(ctx)
        embed = discord.Embed(description='Bot programmiert von Krokofant#0909. Bei Bugs bitte Bug mit !bug <bug> '
                                          'einreichen. Feedback mit !feedback <feedback> einreichen. ',
                              title='Über den Bot!')
        embed.set_footer(text='UltimateBot 2019')
        await ctx.send(embed=embed, delete_after=bp.deltime)

    @commands.command()
    @commands.is_owner()
    async def purge(self, ctx):
        users = {}
        ignore = [636690560811532310, 137291894953607168]
        for member in await ctx.guild.fetch_members(limit=1500).flatten():
            if member.bot or member.id in ignore:
                print(member.id)
                continue
            users[f"{member.id}"] = member.roles
            await member.edit(roles=[member.roles[0]])

        await ctx.send("Sleeping für 2 min!")
        await asyncio.sleep(30)
        await ctx.send("Sleeping done!")
        memberlist = await ctx.guild.fetch_members(limit=1500).flatten()

        for member in memberlist:
            if member.bot or member.id in ignore:
                continue
            roleids = users[f"{member.id}"]
            roles = []
            for role in roleids:
                roles.append(role)
            await member.edit(roles=roles)
        await ctx.send("Fertig")


def setup(client):
    client.add_cog(Basic(client))
