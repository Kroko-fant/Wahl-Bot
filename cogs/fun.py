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
            description='Eine Metafrage ist eine Frage über eine Frage, wie beispielsweise "Darf ich etwas fragen?" '
                        'oder "Kennt sich jemand mit Computern aus?". In der Regel wird der Begriff Metafrage aber '
                        'verallgemeinert und damit alle Fragen bezeichnet, die keine direkte Frage zum Problem des '
                        'Hilfesuchenden sind. Der Hilfesuchende fragt also zunächst allgemein, ob jemand helfen kann. '
                        'Gerade Neulinge oder unerfahrene Benutzer lassen sich zu Metafragen hinreißen, um einen '
                        'kompetenten und hilfsbereiten Ansprechpartner zu finden. Meistens werden Metafragen ignoriert '
                        'oder der Fragende wird rüde darauf hingewiesen, dass ihm niemand bei seinem Problem helfen '
                        'könne, ohne dies zu kennen. [...]\n\n **Beispiele** \n Kennt '
                        'sich jemand mit Computern aus? \n Kann mir jemand helfen? \n Kann ich dich mal sprechen? \n '
                        'Darf ich euch was fragen? \n Kann mir jemand mit FTP-Servern helfen? \n Ist hier zufällig '
                        'jemand, der sich mit Scheidungen auskennt? \n Hast du Zeit? \n Kannst du mal herkommen?\n')
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
