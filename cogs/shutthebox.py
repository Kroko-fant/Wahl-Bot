import random as r

import discord
from discord.ext import commands


class Shutthebox(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def challenge(self, ctx, playerid):

        guild = ctx.guild
        channel = ctx.channel
        user1 = ctx.author
        user2 = self.client.get_user(int(playerid))
        if user1.id is not user2.id:
            await ctx.send("Hey <@" + str(playerid) + '> du wurdest herausgefordert zu ShuttheBox! Schreibe "accept" '
                                                      'um die Challegenge zu akzeptieren')

            def check(m):
                return m.content == 'accept' and m.channel == channel and m.author == user2

            msg1 = await self.client.wait_for('message', check=check, timeout=60)
            await channel.send('Spieler <@' + str(user2.id) +
                               '> hat die Herausforderung angenommen! \n Challenge startet!'.format(msg1))
            boxes = [":mailbox_with_no_mail:", ":mailbox_with_no_mail:", ":mailbox_with_no_mail:",
                     ":mailbox_with_no_mail:",
                     ":mailbox_with_no_mail:", ":mailbox_with_no_mail:", ":mailbox_with_no_mail:",
                     ":mailbox_with_no_mail:"]

            def dice():
                return r.randint(1, 6)

            def boxesmsg():
                boxesmsggg = str(boxes[0] + "   " + boxes[1] + "   " + boxes[2] + "   " + boxes[3] + "\n\n" +
                                 boxes[4] + "   " + boxes[5] + "   " + boxes[6] + "   " + boxes[7])
                return boxesmsggg

            await channel.send(boxesmsg())
            # würfeln
            spieler1dices1 = dice()
            spieler1dices2 = dice()
            await ctx.send(str(user1) + " hat folgende zwei Zahlen gewürfelt: **" + str(spieler1dices1) + "** und **" +
                           str(spieler1dices2) + "**")
        else:
            errorsb02embed = discord.Embed(title="Error #SB02",
                                           description="Du kannst dich nicht selbst herausfordern", color=0xff0000)
            await channel.send(embed=errorsb02embed)

    @challenge.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorsb01embed = discord.Embed(title="Error #SB01",
                                           description="Fehlende NutzerID! Syntax: challenge <userid>", color=0xff0000)
            await ctx.send(embed=errorsb01embed)


def setup(client):
    client.add_cog(Shutthebox(client))
