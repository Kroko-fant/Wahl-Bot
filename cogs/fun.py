import random

from discord.ext import commands


class Fun(commands.Cog):

    def _init_(self, client):
        self.client = client

    @commands.command()
    async def coinflip(self, ctx):
        flip = random.randint(0, 1)
        if flip == 1:
            await ctx.send("Du hast **Kopf** geworfen!")
        elif flip == 0:
            await ctx.send("Du hast **Zahl** geworfen!")
        else:
            await ctx.send("Irgendwie hat das nicht ganz geklappt...")

    @commands.command()
    async def randomnumber(self, ctx, int2=100):
        randomnumber = "Die zufällige Zahl zwischen **0** und **" + str(int2) + "** ist: **" + \
                       str(random.randint(0, int2)) + "**"
        await ctx.send(randomnumber)

    @commands.command()
    async def card(self, ctx):
        karten = [":diamonds: 7", ":diamonds: 8", ":diamonds: 9", ":diamonds: 10", ":diamonds: Bube",
                  ":diamonds: Dame", ":diamonds: Koenig", ":diamonds: Ass", ":hearts: 7", ":hearts: 8",
                  ":hearts: 9", ":hearts: 10", ":hearts: Bube", ":hearts: Dame", ":hearts: Koenig", ":hearts: Ass",
                  ":spades: 7", ":spades: 8", ":spades: 9", ":spades: 10", ":spades: Bube", ":spades: Dame",
                  ":spades: Koenig", ":spades: Ass", ":clubs: 7", ":clubs: 8", ":clubs: 9", ":clubs: 10",
                  ":clubs: Bube", ":clubs: Dame", ":clubs: Koenig", ":clubs: Ass", ]
        gezogene_karte = "Du hast folgende Karte gezogen: **" + karten[random.randint(0, 31)] + "**"
        await ctx.send(gezogene_karte)


def setup(client):
    client.add_cog(Fun(client))
