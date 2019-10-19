import json
import shutil
from ast import Pass

from discord.ext import commands

from botdata import autosetupruns as asr
from botdata import botparameters as bp


class Autosetup(commands.Cog):

    def _init_(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fixserver(self, ctx):
        await bp.delete_cmd(ctx)
        try:
            asr.newserv(ctx.guild)
        except FileExistsError:
            Pass
        try:
            asr.verifyerstellen(ctx.guild)
        except FileExistsError:
            Pass
        try:
            asr.lastdataerstellen(ctx.guild)
        except FileExistsError:
            Pass
        try:
            asr.reactionserstellen(ctx.guild)
        except FileExistsError:
            Pass
        try:
            asr.prefixzuweisen(ctx.guild)
        except FileExistsError:
            Pass
        await ctx.send("Alle Probleme behoben.")

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


def setup(client):
    client.add_cog(Autosetup(client))
