import io
import json
import os
import shutil

from discord.ext import commands

from botdata import botparameters as bp


class Autosetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def newserv(self, guild):
        newdir = './data/servers/' + str(guild.id)
        os.mkdir(newdir)

    async def jsonerstellen(self, data, newdir):
        with io.open(newdir, 'w', encoding='utf8') as outfile:
            string = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
            outfile.write(str(string))

    async def verifyerstellen(self, guild):
        data = {}
        newdir = './data/servers/' + str(guild.id) + '/verified.json'
        try:
            with open(newdir) as f:
                return False
        except FileNotFoundError:
            await self.jsonerstellen(data, newdir)
            return True

    async def reactionserstellen(self, guild):
        data = {}
        newdir = './data/servers/' + str(guild.id) + '/reactions.json'
        try:
            with open(newdir) as f:
                return False
        except FileNotFoundError:
            await self.jsonerstellen(data, newdir)
            return True

    async def sperrenerstellen(self, guild):
        data = {}
        newdir = './data/servers/' + str(guild.id) + '/sperren.json'
        try:
            with open(newdir) as f:
                return False
        except FileNotFoundError:
            await self.jsonerstellen(data, newdir)
            return True

    async def prefixzuweisen(self, guild):
        # Prefix zuweisen
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '!'

        with open('./data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    async def lastdataerstellen(self, guild):
        data = {}
        newdir = './data/servers/' + str(guild.id) + '/lastdata.json'
        await self.jsonerstellen(data, newdir)

    async def fixstuff(self, ctx):
        await bp.delete_cmd(ctx)
        try:
            await self.newserv(ctx.guild)
            await ctx.send("Serververzeichnis wurde erstellt :new:", delete_after=bp.deltime2)
        except FileExistsError:
            await ctx.send("Serververzeichnis bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
        if await self.verifyerstellen(ctx.guild):
            await ctx.send("Datei Verify wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Datei Verify bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
        if await self.lastdataerstellen(ctx.guild):
            await ctx.send("Datei Lastdata wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Datei Lastdata bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
        if await self.reactionserstellen(ctx.guild):
            await ctx.send("Datei Reactions wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Datei Reactions bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
        if await self.prefixzuweisen(ctx.guild):
            await ctx.send("Prefix wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Prefix zurückgesetzt :arrow_right_hook:", delete_after=bp.deltime2)
        if await self.sperrenerstellen(ctx.guild):
            await ctx.send("Datei Sperren wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Datei Sperren bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)

        await ctx.send("Alle Probleme behoben.", delete_after=bp.deltime2)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fixserver(self, channel):
        """Fixt Probleme"""
        await self.fixstuff(channel)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.newserv(guild)
        await self.verifyerstellen(guild)
        await self.lastdataerstellen(guild)
        await self.reactionserstellen(guild)
        await self.prefixzuweisen(guild)

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
            await self.fixstuff(channel)


def setup(client):
    client.add_cog(Autosetup(client))
