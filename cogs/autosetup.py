import json
import shutil

from discord.ext import commands

from botdata import autosetupruns as asr
from botdata import botparameters as bp


class Autosetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fixserver(self, ctx):
        await bp.delete_cmd(ctx)
        try:
            asr.newserv(ctx.guild)
            await ctx.send("Serververzeichnis wurde erstellt :new:", delete_after=bp.deltime2)
        except FileExistsError:
            await ctx.send("Serververzeichnis bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
        if asr.verifyerstellen(ctx.guild):
            await ctx.send("Datei Verify wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Datei Verify bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
        if asr.lastdataerstellen(ctx.guild):
            await ctx.send("Datei Lastdata wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Datei Lastdata bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
        if asr.reactionserstellen(ctx.guild):
            await ctx.send("Datei Reactions wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Datei Reactions bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
        if asr.prefixzuweisen(ctx.guild):
            await ctx.send("Prefix wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Prefix zurückgesetzt :arrow_right_hook:", delete_after=bp.deltime2)
        if asr.sperrenerstellen(ctx.guild):
            await ctx.send("Datei Sperren wurde erstellt :new:", delete_after=bp.deltime2)
        else:
            await ctx.send("Datei Sperren bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)

        await ctx.send("Alle Probleme behoben.", delete_after=bp.deltime)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        asr.newserv(guild)
        asr.verifyerstellen(guild)
        asr.lastdataerstellen(guild)
        asr.reactionserstellen(guild)
        asr.prefixzuweisen(guild)

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
            await bp.delete_cmd(message)
            try:
                asr.newserv(message.guild)
                await channel.send("Serververzeichnis wurde erstellt :new:", delete_after=bp.deltime2)
            except FileExistsError:
                await channel.send("Serververzeichnis bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
            if asr.verifyerstellen(message.guild):
                await channel.send("Datei Verify wurde erstellt :new:", delete_after=bp.deltime2)
            else:
                await channel.send("Datei Verify bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
            if asr.lastdataerstellen(message.guild):
                await channel.send("Datei Lastdata wurde erstellt :new:", delete_after=bp.deltime2)
            else:
                await channel.send("Datei Lastdata bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
            if asr.reactionserstellen(message.guild):
                await channel.send("Datei Reactions wurde erstellt :new:", delete_after=bp.deltime2)
            else:
                await channel.send("Datei Reactions bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)
            if asr.prefixzuweisen(message.guild):
                await channel.send("Prefix wurde erstellt :new:", delete_after=bp.deltime2)
            else:
                await channel.send("Prefix zurückgesetzt :arrow_right_hook:", delete_after=bp.deltime2)
            if asr.sperrenerstellen(message.guild):
                await channel.send("Datei Sperren wurde erstellt :new:", delete_after=bp.deltime2)
            else:
                await channel.send("Datei Sperren bereits vorhanden :white_check_mark:", delete_after=bp.deltime2)

            await channel.send("Alle Probleme behoben.", delete_after=bp.deltime)


def setup(client):
    client.add_cog(Autosetup(client))
