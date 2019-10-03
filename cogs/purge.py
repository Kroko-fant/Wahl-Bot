import json
from _ast import Pass

from discord.ext import commands

from botdata import botparameters as bp


class Purge(commands.Cog):

    def _init_(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if bp.user(member):
            with open('./data/lastmsg.json', 'r') as f:
                members = json.load(f)

            members[str(member.id)] = str(b.today)

            with open('./data/lastmsg.json', 'w') as f:
                json.dump(members, f, indent=4)
        else:
            Pass

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if bp.user(ctx.author):
            with open('./data/lastmsg.json', 'r') as f:
                members = json.load(f)

            members[str(ctx.author.id)] = str(bp.datum)

            with open('./data/lastmsg.json', 'w') as f:
                json.dump(members, f, indent=4)
        else:
            Pass

    @commands.command()
    @commands.check(bp.botowner)
    async def purge(self, ctx, amount=90):
        if amount >= 90:
            ctx.send("Suche Mitglieder zum purgen... das kann einen Moment dauern!")

        elif 90 > amount > 0:
            ctx.send("Die eingegebene Tageszahl ist zu klein!")
        else:
            ctx.send("Bitte gebe eine natürliche Zahl größer als 90 ein")


def setup(client):
    client.add_cog(Purge(client))
