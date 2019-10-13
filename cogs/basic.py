import json

import discord
from discord.ext import commands

from botdata import botparameters as bp


class Basic(commands.Cog):

    def _init_(self, client):
        self.client = client

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await bp.delete_cmd(ctx)
        await ctx.send(f'Pong! {round(self.client.latency * 1000)} ms')

    @commands.command()
    async def version(self, ctx):
        await ctx.send("Der Bot läuft auf ", bp.version, ". Die API läuft auf Version ", bp.apiversion())

    @commands.command()
    async def bug(self, ctx, *, bugt):
        await bp.delete_cmd(ctx)
        with open('./botdata/bugs.json', 'r') as f:
            bugs = json.load(f)
        bugs[str(bugt)] = str(ctx.author.id)

        with open('./botdata/bugs.json', 'w') as f:
            json.dump(bugs, f, indent=4)

        await ctx.send('Danke <@' + str(ctx.author.id) + '> für das einreichen deines Bugs, wir melden uns zurück.')

    @commands.command()
    async def feedback(self, ctx, *, feedbackt):
        await bp.delete_cmd(ctx)
        with open('./botdata/feedback.json', 'r') as f:
            feedbacks = json.load(f)
        feedbacks[str(feedbackt)] = str(ctx.author.id)

        with open('./botdata/feedback.json', 'w') as f:
            json.dump(feedbacks, f, indent=4)

        await ctx.send('Danke <@' + str(ctx.author.id) + '> für das einreichen deines Bugs, wir melden uns zurück.')

    @commands.command()
    async def about(self, ctx):
        await bp.delete_cmd(ctx)
        embed = discord.Embed(
            title='Über den Bot!',
            description='Bot programmiert von Krokofant#0909.'
                        'Bei Bugs bitte Bug mit !bug <bug> einreichen.'
                        'Feedback mit !feedback <feedback> einreichen.'
        )
        embed.set_footer(text='2019')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Basic(client))
