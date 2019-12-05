import random

from discord.ext import commands

from botdata import blacklist as bl
from botdata import botparameters as bp


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def coinflip(self, ctx):
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
        await bp.delete_cmd(ctx)
        randomnumber = "Die zufällige Zahl zwischen **0** und **" + str(int2) + "** ist: **" + \
                       str(random.randint(0, int2)) + "**"
        await ctx.send(randomnumber)

    @commands.command()
    async def card(self, ctx):
        await bp.delete_cmd(ctx)
        karten = [":diamonds: 7", ":diamonds: 8", ":diamonds: 9", ":diamonds: 10", ":diamonds: Bube",
                  ":diamonds: Dame", ":diamonds: Koenig", ":diamonds: Ass", ":hearts: 7", ":hearts: 8",
                  ":hearts: 9", ":hearts: 10", ":hearts: Bube", ":hearts: Dame", ":hearts: Koenig", ":hearts: Ass",
                  ":spades: 7", ":spades: 8", ":spades: 9", ":spades: 10", ":spades: Bube", ":spades: Dame",
                  ":spades: Koenig", ":spades: Ass", ":clubs: 7", ":clubs: 8", ":clubs: 9", ":clubs: 10",
                  ":clubs: Bube", ":clubs: Dame", ":clubs: Koenig", ":clubs: Ass", ]
        gezogene_karte = "Du hast folgende Karte gezogen: **" + karten[random.randint(0, 31)] + "**"
        await ctx.send(gezogene_karte)

    @commands.Cog.listener()
    async def on_message(self, message):
        if ((message.content.startswith("py.print('") and message.content.count("'") == 2
             and message.content.endswith("')")) or
            (message.content.startswith('py.print("') and message.content.count('"') == 2
             and message.content.endswith('")'))) and bp.user(message.author) \
                and not any([curse in message.content.lower() for curse in bl.blacklist]):
            content = message.content[:-2]
            content = content[10:]
            await bp.delete_cmd(message)
            await message.channel.send(f'{message.author} sagt {content}')
        elif ((message.content.startswith('java.System.out.println("') or
               (message.content.startswith('java.System.out.print("')) and message.content.count('"') == 2
               and message.content.endswith('");'))) and bp.user(message.author) \
                and not any([curse in message.content.lower() for curse in bl.blacklist]):
            content = message.content[:-2]
            content = content[24:]
            await bp.delete_cmd(message)
            await message.channel.send(f'{message.author} sagt {content}')


def setup(client):
    client.add_cog(Fun(client))
