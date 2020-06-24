import random

import discord
from discord.ext import commands

from botdata import botparameters as bp


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def metafrage(self, ctx):
        """Gibt den Meta-Fragen-Text wider"""
        await bp.delete_cmd(ctx)
        metafrageembed = discord.Embed(
            title="Metafrage",
            description='Du hast gerade eine Metafrage gestellt. Eine Metafrage ist eine unnötige Frage über der '
                        'HauptFrage. Dies ist zwar höflich, aber ziemlich umständlich, da man seine Frage dann zwei mal'
                        ' stellen muss. \n\nDie Frage "Kennt sich jemand mit x aus?" hilft leider auch nicht weiter. '
                        'Die Anwesenden könnten eventuell bei dem Problem helfen, obwohl sie nicht von sich behaupten '
                        'würden, mit dem Thema vertraut zu sein. Und auch wenn jemand mit dem erfragten Thema vertraut '
                        'ist, bedeutet dies nicht, dass er/sie eine spezielle Frage zu diesem Thema beantworten kann – '
                        'niemand ist allwissend.\n\nDeswegen, stelle bitte einfach deine Frage anstatt "Darf ich etwas'
                        ' fragen" oder "kennt sich jemand mit x und y aus?" zu schreiben. Selbst, wenn es eine'
                        ' komplizierte oder sehr spezielle Frage ist, die du mehrere Minuten lang formulieren müsstest,'
                        ' dann mach das bitte. Wir wissen sonst nicht, ob wir sie beantworten könnten.'
                        '\nWeitere Infos findest du unter http://metafrage.de/')
        metafrageembed.set_footer(text="Quelle: http://metafrage.de/")
        metafrageembed.set_thumbnail(url="https://cdn.pixabay.com/photo/2015/10/31/12/00/question-1015308_960_720.jpg")
        await ctx.send(embed=metafrageembed)

    @commands.command()
    async def coinflip(self, ctx):
        """Werfe eine Münze und erhalte kopf oder Zahl."""
        await bp.delete_cmd(ctx)
        flip = random.randint(0, 1)
        if flip == 1:
            await ctx.send("Du hast **Kopf** geworfen!")
        elif flip == 0:
            await ctx.send("Du hast **Zahl** geworfen!")
        else:
            await ctx.send("Irgendwie hat das nicht ganz geklappt...", delete_after=bp.deltime)

    @commands.command()
    async def randomnumber(self, ctx, int2=100):
        """Gebe eine zufällige Zahl zwischen 0 und x ein.
        Syntax: {prefix}randomnumber <x>
        Hat x keinen Wert bekommt x automatisch 100 zugewiesen."""
        await bp.delete_cmd(ctx)
        await ctx.send(f"Die zufällige Zahl zwischen **0** und **{str(int2)}** ist: **{str(random.randint(0, int2))}**")

    @commands.command()
    async def card(self, ctx):
        """Ziehe eine Karte"""
        await bp.delete_cmd(ctx)
        karten = [":diamonds: 7", ":diamonds: 8", ":diamonds: 9", ":diamonds: 10", ":diamonds: Bube",
                  ":diamonds: Dame", ":diamonds: Koenig", ":diamonds: Ass", ":hearts: 7", ":hearts: 8",
                  ":hearts: 9", ":hearts: 10", ":hearts: Bube", ":hearts: Dame", ":hearts: Koenig", ":hearts: Ass",
                  ":spades: 7", ":spades: 8", ":spades: 9", ":spades: 10", ":spades: Bube", ":spades: Dame",
                  ":spades: Koenig", ":spades: Ass", ":clubs: 7", ":clubs: 8", ":clubs: 9", ":clubs: 10",
                  ":clubs: Bube", ":clubs: Dame", ":clubs: Koenig", ":clubs: Ass", ]
        await ctx.send(f"Du hast folgende Karte gezogen: **{karten[random.randint(0, 31)]}**")


def setup(client):
    client.add_cog(Fun(client))
