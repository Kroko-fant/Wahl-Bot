import io
import json
import os
import shutil

from discord.ext import commands

from botdata import botparameters as bp


async def newserv(guild):
    newdir = './data/servers/' + str(guild.id)
    os.mkdir(newdir)


async def jsonerstellen(data, newdir):
    with io.open(newdir, 'w', encoding='utf8') as outfile:
        string = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
        outfile.write(str(string))


async def verifyerstellen(guild):
    data = {}
    newdir = './data/servers/' + str(guild.id) + '/verified.json'
    try:
        with open(newdir) as f:
            return False
    except FileNotFoundError:
        await jsonerstellen(data, newdir)
        return True


async def reactionserstellen(guild):
    data = {}
    newdir = './data/servers/' + str(guild.id) + '/reactions.json'
    try:
        with open(newdir) as f:
            return False
    except FileNotFoundError:
        await jsonerstellen(data, newdir)
        return True


async def sperrenerstellen(guild):
    data = {}
    newdir = './data/servers/' + str(guild.id) + '/sperren.json'
    try:
        with open(newdir) as f:
            return False
    except FileNotFoundError:
        await jsonerstellen(data, newdir)
        return True


async def prefixzuweisen(guild):
    # Prefix zuweisen
    with open('./data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('./data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


async def lastdataerstellen(guild):
    data = {}
    newdir = './data/servers/' + str(guild.id) + '/lastdata.json'
    await jsonerstellen(data, newdir)


async def fixstuff(ctx):
    await bp.delete_cmd(ctx)
    try:
        await newserv(ctx.guild)
        await ctx.send("Serververzeichnis wurde erstellt :new:", delete_after=bp.deltime2)
    except FileExistsError:
        await ctx.send("Serververzeichnis bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
    if await verifyerstellen(ctx.guild):
        await ctx.send("Datei Verify wurde erstellt :new:", delete_after=bp.deltime2)
    else:
        await ctx.send("Datei Verify bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
    if await lastdataerstellen(ctx.guild):
        await ctx.send("Datei Lastdata wurde erstellt :new:", delete_after=bp.deltime2)
    else:
        await ctx.send("Datei Lastdata bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
    if await reactionserstellen(ctx.guild):
        await ctx.send("Datei Reactions wurde erstellt :new:", delete_after=bp.deltime2)
    else:
        await ctx.send("Datei Reactions bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
    if await prefixzuweisen(ctx.guild):
        await ctx.send("Prefix wurde erstellt :new:", delete_after=bp.deltime2)
    else:
        await ctx.send("Prefix zurückgesetzt :arrow_right_hook:", delete_after=bp.deltime2)
    if await sperrenerstellen(ctx.guild):
        await ctx.send("Datei Sperren wurde erstellt :new:", delete_after=bp.deltime2)
    else:
        await ctx.send("Datei Sperren bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)

    await ctx.send("Alle Probleme behoben.", delete_after=bp.deltime)


class Autosetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fixserver(self, channel):
        f"""Dieser Command dient zum beheben von Problemen, die aus verschiedenen Grüden entstehen können. 
            Dabei werden fehlende Dateien erstellt und der Prefix zurückgesetzt."""
        await fixstuff(channel)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await newserv(guild)
        await verifyerstellen(guild)
        await lastdataerstellen(guild)
        await reactionserstellen(guild)
        await prefixzuweisen(guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # Serverdata löschen
        serverdir = './data/servers/' + str(guild.id)
        shutil.rmtree(serverdir)

        # Prefix löschen
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('./data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if bp.botowner(message) and message.content == "admin.fixserver":
            channel = message.channel
            await fixstuff(channel)


def setup(client):
    client.add_cog(Autosetup(client))
