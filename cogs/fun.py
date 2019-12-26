import random

import discord
from discord.ext import commands

from botdata import blacklist as bl
from botdata import botparameters as bp


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

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

    @commands.command()
    async def sayinxyz(self, ctx):
        """Sage etwas in einer Programmiersprache."""
        await bp.delete_cmd(ctx)
        sayinxyzembed = discord.Embed(
            title='Sayxyz Help',
            description='Um eine Nachricht in einer bestimmten Programmiersprache zu sagen, muss die Korrekte Syntax '
                        'des Statements eingehalten werden. Dafür wird die Sprache vor dem Command aufgerufen mit '
                        '<sprachkürzel>.<befehl> \n'
                        '\nBsp.: python.print("Hello World")\n'
                        'Folgende Sprachen sind verfügbar:\n'
                        'Python: py\t\tJava: java.\t\tJavaScript: js.\t\tC#: c#\n'
                        'C++: c++\t\tGO: go.\t\tPHP: php.'
        )
        await ctx.send(embed=sayinxyzembed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Python
        if ((message.content.startswith("py.print('") and message.content.count("'") == 2
             and message.content.endswith("')")) or
            (message.content.startswith('py.print("') and message.content.count('"') == 2
             and message.content.endswith('")'))) and bp.user(message.author) \
                and not any([curse in message.content.lower() for curse in bl.blacklist]):
            content = message.content[:-2]
            content = content[10:]
            await bp.delete_cmd(message)
            await message.channel.send(f'**{message.author}** sagt "{content}" in Python.')
        # Java
        elif (message.content.startswith('java.System.out.println("') or
              message.content.startswith('java.System.out.print("')) and message.content.count('"') == 2 and \
                message.content.endswith('");') and bp.user(message.author) \
                and not any([curse in message.content.lower() for curse in bl.blacklist]):
            content = message.content[:-3]
            if message.content.startswith('java.System.out.println("'):
                content = content[25:]
            else:
                content = content[23:]
            await bp.delete_cmd(message)
            await message.channel.send(f'**{message.author}** sagt "{content}" in Java.')
        # C#
        elif ((message.content.startswith('c#.Console.Write("') or
               (message.content.startswith('c#.Console.WriteLine("'))) and message.content.count('"') == 2
              and message.content.endswith('");')) and bp.user(message.author) \
                and not any([curse in message.content.lower() for curse in bl.blacklist]):
            content = message.content[:-3]
            if content.startswith('c#.Console.WriteLine'):
                content = content[22:]
            else:
                print(content)
                content = content[18:]
            await bp.delete_cmd(message)
            await message.channel.send(f'**{message.author}** sagt "{content}" in C#.')
        # Java Script
        elif ((message.content.startswith('js.console.log("') or
               (message.content.startswith('js.alert("'))) and message.content.count('"') == 2
              and message.content.endswith('");')) and bp.user(message.author) \
                and not any([curse in message.content.lower() for curse in bl.blacklist]):
            content = message.content[:-3]
            if content.startswith('js.console.log("'):
                content = content[16:]
            else:
                print(content)
                content = content[10:]
            await bp.delete_cmd(message)
            await message.channel.send(f'**{message.author}** sagt "{content}" in JavaScript.')
        # Go
        if (message.content.startswith('go.fmt.Println("') or message.content.startswith('go.fmt.Print("')) \
                and message.content.count('"') == 2 and message.content.endswith('")') and bp.user(message.author) \
                and not any([curse in message.content.lower() for curse in bl.blacklist]):
            content = message.content[:-2]
            if message.content.startswith('go.fmt.Println("'):
                content = content[16:]
            else:
                content = content[14:]
            await bp.delete_cmd(message)
            await message.channel.send(f'**{message.author}** sagt "{content}" in GO.')
        # C++
        elif message.content.startswith('c++.cout << "') and message.content.count('"') == 2 and \
                message.content.endswith('";') and bp.user(message.author) \
                and not any([curse in message.content.lower() for curse in bl.blacklist]):
            content = message.content[:-3]
            content = content[13:]
            await bp.delete_cmd(message)
            await message.channel.send(f'**{message.author}** sagt "{content}" in C++.')
        # PHP
        elif message.content.startswith('php.echo "') and message.content.count('"') == 2 and \
                message.content.endswith('";') and bp.user(message.author) \
                and not any([curse in message.content.lower() for curse in bl.blacklist]):
            content = message.content[:-3]
            content = content[10:]
            await bp.delete_cmd(message)
            await message.channel.send(f'**{message.author}** sagt "{content}" in PHP.')


def setup(client):
    client.add_cog(Fun(client))
