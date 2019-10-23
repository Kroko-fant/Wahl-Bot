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

        roles[str(ctx.guild.id)] = roleid

        with open('./data/mainrole.json', 'w') as f:
            json.dump(roles, f, indent=4)
        await bp.delete_cmd(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:

            member = message.author
            with open('./data/mainrole.json', 'r') as f:
                roles = json.load(f)
            role = message.guild.get_role(roles[str(message.guild.id)])
            try:
                await member.addroles(role, reason="verify")
            except Exception:
                Pass


def setup(client):
    client.add_cog(Autoverify(client))
