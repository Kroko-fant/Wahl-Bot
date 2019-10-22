# class Money(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(Money(client))
