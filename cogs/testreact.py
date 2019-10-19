import json

from discord.ext import commands


class Reactions(commands.Cog):

    def _init_(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message = payload.message_id
        guild = payload.guild_id
        user = payload.user_id

        print('reaction erfasst""')

    @commands.command()
    async def addreactionmsg(self, ctx, msgid):
        guild = ctx.guild
        with open('./data/reactionmsg.json', 'r') as f:
            reacts = json.load(f)

        reacts[str(guild.id)] = str(msgid)

        with open('./data/reactionmsg.json', 'w') as f:
            json.dump(reacts, f, indent=4)


def setup(client):
    client.add_cog(Reactions(client))
