from discord.ext import commands


class Xp(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.xps = dict()
        # for file in os.listdir("data\servers"):


def setup(client):
    client.add_cog(Xp(client))
