import json

from discord.ext import commands

from botdata import botparameters as bp


class Verify(commands.Cog):

    def _init_(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx):
        await bp.delete_cmd(ctx)
        if bp.unverifiziert(ctx):
            # USERID in Verify
            with open('./data/verified.json', 'r') as f:
                verified = json.load(f)

            verified[str(ctx.author.id)] = True

            with open('./data/verified.json', 'w') as f:
                json.dump(verified, f, indent=4)
            await ctx.send('Verifiziert')

            # Rolle geben
            with open('./data/verify-role.json', 'r') as f:
                verified = json.load(f)

            rolle = verified[str(ctx.author.guild)]

            await ctx.author.add_roles(rolle, reason="Verify", atomic=True)
            await ctx.send('Verifiziert')
        elif bp.verifiziert(ctx):
            await ctx.send("Du bist bereits verifiziert!")
        else:
            await ctx.send("Du konntest nicht verifiziert werden! Wende dich an das Team oder versuche es nochmal!")


def setup(client):
    client.add_cog(Verify(client))
