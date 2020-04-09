import discord
from discord.ext import commands

from botdata import botparameters as bp


class Voiceutility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queues = dict()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.id not in self.queues.keys():
            return
        else:
            channels = self.queues[member.guild.id].keys()
            if before.channel != after.channel:
                if after.channel is not None and after.channel.id in channels:
                    self.queues[member.guild.id][after.channel.id].append(member.id)
                elif before.channel is not None and before.channel.id in channels:
                    self.queues[member.guild.id][before.channel.id].remove(member.id)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addque(self, ctx, chid):
        if self.client.get_channel(int(chid)) is not None:
            if ctx.guild.id not in self.queues.keys():
                self.queues[ctx.guild.id] = dict()
            self.queues[ctx.guild.id][int(chid)] = []
            await ctx.send("Warteschlangenchannel hinzugefügt!")
        else:
            await ctx.send("Kanal konnte nicht gefunden werden.")
        await bp.delete_cmd(ctx)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removeque(self, ctx, chid):
        result = self.queues[ctx.guild.id].pop(int(chid), None)
        if result is None:
            await ctx.send("Channel konnte nicht gefunden werden!")
        else:
            await ctx.send("Channel erfolgreich entfernt")
        await bp.delete_cmd(ctx)

    @commands.command()
    async def checkpos(self, ctx, que=None):
        if ctx.guild.id not in self.queues.keys():
            await ctx.send(embed=discord.Embed(title="Error!", description="Keine Queues auf diesem Server gefunden"))
        elif len(self.queues[ctx.guild.id].keys()) == 0:
            await ctx.send(embed=discord.Embed(title="Error!", description="Keine Queues auf diesem Server gefunden"))
        elif len(self.queues[ctx.guild.id].keys()) == 1:
            key = list(self.queues[ctx.guild.id].keys())[0]
            liste = self.queues[ctx.guild.id][key]
            if ctx.author.id in liste:
                position = f'{liste.index(ctx.author.id) + 1} / {len(liste)}'
            else:
                position = "Nicht in der Queue"
            body = ""
            for index, obj in enumerate(liste):
                body += f"{index + 1}. {self.client.get_user(obj)}\n"
                if index == 4:
                    break
            await ctx.send(embed=discord.Embed(title="Aktuelle Queue:", description=f"Deine Position: "
                                                                                    f"{position}\n{body}"))


def setup(client):
    client.add_cog(Voiceutility(client))
