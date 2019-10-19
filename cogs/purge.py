import json
from _ast import Pass

from discord.ext import commands

from botdata import botparameters as bp


class Purge(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    # Member join => wird erstellt
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if bp.user(member):
            bp.update_member(member)
        else:
            Pass

    # Member schreibt nachricht
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if bp.user(ctx.author):
            bp.update_member(ctx.author)
        else:
            Pass

    # Member joint Voice
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if bp.user(member):
            bp.update_member(member)
        else:
            Pass

    # Member verlässt Server
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if bp.user(member):
            lastmember = './data/servers/' + str(member.guild.id) + '/lastdata.json'
            with open(lastmember, 'r') as f:
                members = json.load(f)

            await members.pop[str(member.id)]

            with open(lastmember, 'w') as f:
                json.dump(members, f, indent=4)
        else:
            Pass

    # Member purgen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount=90):
        await bp.delete_cmd(ctx)
        if amount >= 90:
            ctx.send("Suche Mitglieder zum purgen... das kann einen Moment dauern!")

        elif 90 > amount > 0:
            ctx.send("Die eingegebene Tageszahl ist zu klein!")
        else:
            ctx.send("Bitte gebe eine natürliche Zahl größer als 90 ein")


def setup(client):
    client.add_cog(Purge(client))
