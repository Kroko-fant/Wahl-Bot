import json
from ast import Pass

from discord.ext import commands

from botdata import botparameters as bp


class Autoverify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmainrole(self, ctx, roleid):
        with open('./data/mainrole.json', 'r') as f:
            roles = json.load(f)

        roles[str(ctx.guild.id)] = int(roleid)

        with open('./data/mainrole.json', 'w') as f:
            json.dump(roles, f, indent=4)
        await ctx.send("Main-Rolle gesetzt.")
        await bp.delete_cmd(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            try:
                guild = message.guild
                member = message.guild.get_member(int(message.author.id))
                with open('./data/mainrole.json', 'r') as f:
                    roles = json.load(f)
                roleid = (roles[str(guild.id)])
                role = guild.get_role(roleid)
                await member.add_roles(role, reason="verify")
            except KeyError:
                Pass


def setup(client):
    client.add_cog(Autoverify(client))
