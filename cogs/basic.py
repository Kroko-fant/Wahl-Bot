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
        await ctx.send(f'Der Bot läuft auf :eyes: **Version Beta 1.3.1a**. '
                       f'Die API läuft auf Version :mailbox: **{discord.__version__}**', delete_after=bp.deltime)

    @commands.command()
    async def bug(self, ctx, *, bugt):
        """"Reiche einen Bug ein.
        Syntax: {Prefix}bug <bugtext>"""
        channel = self.client.get_channel(int(643546804750909454))
        if 1800 >= len(bugt) >= 100:
            await channel.send(f"**Bug von {str(ctx.author)}:**{bugt}")
            await bp.delete_cmd(ctx)
            await ctx.send(f'Danke <@{str(ctx.author.id)}> für das einreichen deines Bugs, wir melden uns zurück.',
                           delete_after=bp.deltime)
        else:
            await ctx.send("Dein Bugtest muss zwischen 100 und 1800 Zeichen lang sein.", delete_after=bp.deltime)

    @bug.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorba02embed = discord.Embed(title="Error #BA02",
                                           description="Fehlendes Feedback! Syntax: bug <userid>", color=0xff0000)
            await ctx.send(embed=errorba02embed)

    @commands.command()
    async def feedback(self, ctx, *, feedbackt):
        """Reiche Feedback ein
        Syntax; {Prefix}feedback <feedbacktext>"""
        channel = self.client.get_channel(int(643540415919816717))
        if 1800 >= len(feedbackt) >= 100:
            await channel.send(f'**Feedback von {str(ctx.author)}:**  {feedbackt}')
            await bp.delete_cmd(ctx)
            await ctx.send(f'Danke <@{str(ctx.author.id)}> für das einreichen deines Feedbacks, wir melden uns zurück.',
                           delete_after=bp.deltime)
        else:
            await ctx.send("Dein Feedback darf zwischen 100 und 1800 Zeichen umfassen.")

    @feedback.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorba01embed = discord.Embed(title="Error #BA01",
                                           description="Fehlendes Feedback! Syntax: feedback <userid>", color=0xff0000)
            await ctx.send(embed=errorba01embed)

    @commands.command()
    async def about(self, ctx):
        """Zeigt Informationen über den Bot an."""
        await bp.delete_cmd(ctx)
        embed = discord.Embed(
            title='Über den Bot!', description='Bot programmiert von Krokofant#0909. '
                                               'Bei Bugs bitte Bug mit !bug <bug> einreichen. '
                                               'Feedback mit !feedback <feedback> einreichen. '
        )
        embed.set_footer(text='UltimateBot 2019')
        await ctx.send(embed=embed, delete_after=bp.deltime)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            channel = self.client.get_channel(int(635544300834258995))
            content = f'**{str(message.author)}** sagt: "{str(message.content)}"'
            if len(message.content) < 1800:
                await channel.send(content)
            else:
                await channel.send(content[0:1800])
                await channel.send(content[1801])


def setup(client):
    client.add_cog(Basic(client))
