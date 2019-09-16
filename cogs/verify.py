import json

from discord.ext import commands


async def unverifiziert(ctx):
    with open('./data/verified.json', 'r') as f:
        trueuserid = str(ctx.author.id) + '": true'
        falseuserid = str(ctx.author.id) + '": false'
        data = f.read()
        if trueuserid in data:
            await ctx.send("Du bist bereits verifiziert!")
            return False
        elif falseuserid in data:
            await ctx.send("Du bist gesperrt!")
            return False
        else:
            await ctx.send("Verifiziere...")
            return True


class Verify(commands.Cog):

    def _init_(self, client):
        self.client = client

    @commands.command()
    @commands.check(unverifiziert)
    async def verify(self, ctx):
        with open('./data/verified.json', 'r') as f:
            verified = json.load(f)

        verified[str(ctx.author.id)] = True

        with open('./data/verified.json', 'w') as f:
            json.dump(verified, f, indent=4)
        await ctx.send('Verifiziert')


def setup(client):
    client.add_cog(Verify(client))
