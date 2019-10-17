from discord.ext import commands


class Reactions(commands.Cog):

    def _init_(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction, user):


def setup(client):
    client.add_cog(Reactions(client))
