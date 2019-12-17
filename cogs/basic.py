import discord
from discord.ext import commands

from botdata import botparameters as bp
from main import get_prefix


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands
    # Zeigt die aktuelle Version des Bots.
    @commands.command()
    async def version(self, ctx):
        """Zeigt die aktuelle Version des Bots und die aktuelle Version der API an."""
        await bp.delete_cmd(ctx)
        versiontext = "Der Bot läuft auf " + "Version Beta 1.1.3b" + ". Die API läuft auf Version " + bp.apiversion()
        await ctx.send(versiontext, delete_after=bp.deltime)

    # Lässt den User einen Bug einreichen.
    @commands.command()
    async def bug(self, ctx, *, bugt):
        """Reiche einen Bug ein. Dieser wird dem Team des Bots übermittelt. Eventuell bekommst du sogar eine Rückmeldung
        Syntax: !bug <bugtext>"""
        channel = self.client.get_channel(int(643546804750909454))
        content = "**Bug von " + str(ctx.author) + ":** " + bugt
        await channel.send(content)
        await bp.delete_cmd(ctx)
        await ctx.send('Danke <@' + str(ctx.author.id) + '> für das einreichen deines Bugs, wir melden uns zurück.',
                       delete_after=bp.deltime)

    # Error fürs Bug einreichen
    @bug.error
    async def bug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorba02embed = discord.Embed(title="Error #BA02",
                                           description=f'Fehlender Bug! Syntax: {get_prefix(self.client, ctx)}bug'
                                                       f' <userid>', color=0xff0000)
            await ctx.send(embed=errorba02embed)

    # Feedback einreichen
    @commands.command()
    async def feedback(self, ctx, *, feedbackt):
        f""""Hinterlasse mit !feedback dein Feedback zum Bot. Das Tem bemüht sich dieses zu bearbeiten.
        Syntax: {get_prefix(self.client, ctx)}feedback <dein_feedback> """
        channel = self.client.get_channel(int(643540415919816717))
        content = "**Feedback von " + str(ctx.author) + ":** " + feedbackt
        if content.lower() is "<dein_feedback>":
            await ctx.send("<dein_feedback> ist kein gültiges Argument")
        else:
            await channel.send(content)
            await bp.delete_cmd(ctx)
            await ctx.send('Danke <@' + str(ctx.author.id) +
                           '> für das einreichen deines Feedbacks, wir melden uns zurück.', delete_after=bp.deltime)

    @feedback.error
    async def feedback_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorba01embed = discord.Embed(title="Error #BA01",
                                           description=f'Fehlendes Feedback! Syntax: '
                                                       f'{get_prefix(self.client, ctx)}feedback <userid>',
                                           color=0xff0000)
            await ctx.send(embed=errorba01embed)

    @commands.command()
    async def about(self, ctx):
        """Liefert eine Kurzbeschreibung über den Bot."""
        await bp.delete_cmd(ctx)
        embed = discord.Embed(
            title='Über den Bot!',
            description='Bot programmiert von <@Krokofant#0909> in Python 3.7/3.8 '
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
