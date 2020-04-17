import json

import discord
from discord.ext import commands

from botdata import botparameters as bp


class Autoverify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmainrole(self, ctx, role: discord.Role):
        """Setze die Rolle die neue User bekommen"""
        if role.guild is ctx.guild:
            with open('./data/roles/mainrole.json', 'r') as f:
                roles = json.load(f)

            roles[str(ctx.guild.id)] = int(role.id)

            with open('./data/roles/mainrole.json', 'w') as f:
                json.dump(roles, f, indent=4)
            await bp.delete_cmd(ctx)
            await ctx.send("Main-Rolle gesetzt.", delete_after=bp.deltime)
        else:
            await ctx.send("Rolle wurde auf dem Server nicht gefunden.", delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addspacer(self, ctx, role: discord.Role):
        """Füge eine Spacerrolle hinzu"""
        if role.guild is ctx.guild:
            with open('./data/roles/spacer.json', 'r') as f:
                spacers = json.load(f)
            if str(ctx.guild.id) not in spacers.keys():
                spacers[str(ctx.guild.id)] = []
            spacers[str(ctx.guild.id)].append(int(role.id))
            with open('./data/roles/spacer.json', 'w') as f:
                json.dump(spacers, f, indent=4)
            await ctx.send(f'Rolle {discord.role} hinzugefügt.')
        else:
            await ctx.send("Rolle wurde auf dem Server nicht gefunden.", delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removespacer(self, ctx, role: discord.Role):
        """Entfernt einen Spacer"""
        if role.guild is ctx.guild:
            with open('./data/roles/spacer.json', 'r') as f:
                roles = json.load(f)

            roles[str(ctx.guild.id)].remove(int(role.id))

            with open('./data/roles/spacer.json', 'w') as f:
                json.dump(roles, f, indent=4)
            await bp.delete_cmd(ctx)
            await ctx.send("Spacerrolle entfernt.", delete_after=bp.deltime)
        else:
            await ctx.send("Rolle wurde auf dem Server nicht gefunden.", delete_after=bp.deltime)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None and message.author is not None and len(message.author.roles) == 1:
            try:
                guild = message.guild
                member = message.guild.get_member(int(message.author.id))
                # Main Rolle setzen
                with open('./data/roles/mainrole.json', 'r') as f:
                    servers = json.load(f)
                roleid = (servers[str(guild.id)])
                role = guild.get_role(roleid)
                await member.add_roles(role, reason="verify")
                # Spacer setzen
                with open('./data/roles/spacer.json', 'r') as f:
                    servers = json.load(f)
                roles = servers[str(guild.id)]
                for rid in roles:
                    print(rid)
                    trole = guild.get_role(rid)
                    await member.add_roles(trole, reason="verify")
            except KeyError:
                pass


def setup(client):
    client.add_cog(Autoverify(client))
