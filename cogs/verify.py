import json

from discord.ext import commands

from botdata import botparameters as bp


class Verify(commands.Cog):

    def _init_(self, client):
        self.client = client

    @commands.command()
    async def verify(self, ctx):
        await bp.delete_cmd(ctx)
        if await bp.unverifiziert(ctx):
            # USERID in Verify
            verifydir = './data/servers/' + str(ctx.guild.id) + '/verified.json'
            with open(verifydir, 'r') as f:
                verified = json.load(f)

            verified[str(ctx.author.id)] = True

            with open(verifydir, 'w') as f:
                json.dump(verified, f, indent=4)
            await ctx.send('Verifiziert')

            # Rolle geben
            with open(verifydir, 'r') as f:
                verified = json.load(f)

            rolle = verified[str(ctx.guild.id)]

            await ctx.author.add_roles(rolle, reason="Verify", atomic=True)
            await ctx.send('Verifiziert')
        elif await bp.verifiziert(ctx):
            await ctx.send("Du bist bereits verifiziert!")
        else:
            await ctx.send("Du konntest nicht verifiziert werden! Wende dich an das Team oder versuche es nochmal!")


def setup(client):
    client.add_cog(Verify(client))
