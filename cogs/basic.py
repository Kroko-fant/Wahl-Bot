import discord
from discord.ext import commands

from botdata import botparameters as bp


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def version(self, ctx):
        await bp.delete_cmd(ctx)
        versiontext = "Der Bot läuft auf " + "Version Beta 1.1.3" + ". Die API läuft auf Version " + bp.apiversion()
        await ctx.send(versiontext, delete_after=bp.deltime)

    @commands.command()
    async def bug(self, ctx, *, bugt):
        channel = self.client.get_channel(int(643546804750909454))
        content = "**Bug von " + str(ctx.author) + ":** " + bugt
        await channel.send(content)
        await bp.delete_cmd(ctx)
        await ctx.send('Danke <@' + str(ctx.author.id) + '> für das einreichen deines Bugs, wir melden uns zurück.',
                       delete_after=bp.deltime)

    @bug.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorba02embed = discord.Embed(title="Error #BA02",
                                           description="Fehlendes Feedback! Syntax: bug <userid>", color=0xff0000)
            await ctx.send(embed=errorba02embed)

    @commands.command()
    async def feedback(self, ctx, *, feedbackt):
        channel = self.client.get_channel(int(643540415919816717))
        content = "**Feedback von " + str(ctx.author) + ":** " + feedbackt
        await channel.send(content)
        await bp.delete_cmd(ctx)
        await ctx.send('Danke <@' + str(ctx.author.id) +
                       '> für das einreichen deines Feedbacks, wir melden uns zurück.', delete_after=bp.deltime)

    @feedback.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorba01embed = discord.Embed(title="Error #BA01",
                                           description="Fehlendes Feedback! Syntax: feedback <userid>", color=0xff0000)
            await ctx.send(embed=errorba01embed)

    @commands.command()
    async def about(self, ctx):
        await bp.delete_cmd(ctx)
        embed = discord.Embed(
            title='Über den Bot!',
            description='Bot programmiert von Krokofant#0909. '
                        'Bei Bugs bitte Bug mit !bug <bug> einreichen. '
                        'Feedback mit !feedback <feedback> einreichen. '
        )
        embed.set_footer(text='UltimateBot 2019')
        await ctx.send(embed=embed, delete_after=bp.deltime)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            channel = self.client.get_channel(int(635544300834258995))
            content = "**" + str(message.author) + '** sagt: "' + str(message.content) + '"'
            await channel.send(content)


def setup(client):
    client.add_cog(Basic(client))
