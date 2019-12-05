
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

        player1 = ctx.author
        player2 = self.client.get_user(int(playerid))
        playerpkt = [0, 0]

        def check(m):
            return m.content.lower == 'accept' and m.channel == channel and m.author == player2

        boxes = [True, True, True, True, True, True, True, True]
        runde = 0

        def dice():
            return r.randint(1, 6)

        def boxesmsg():
            for var in boxes:
                boxesmsggg = ""
                if boxes[var]:
                    boxesmsggg = boxesmsggg + ":white_checkmark:\t"
                else:
                    return ":red_circle:"
                if var * 2 == len(boxes):
                    boxesmsggg = boxesmsggg + "\n\n"
            return boxesmsggg

        def close_boxes(box1, box2, summe, player):
            if box1 or box2 == 0:
                oldpkt = playerpkt[player]
                for box in boxes:
                    if boxes[box]:
                        playerpkt[player] = playerpkt[player] + box + 1
                return f'Dir wurden **{playerpkt[player] - oldpkt}** auf dein Konto hinzugefügt.'
            elif box1 > 0 and box2 > 0 and summe == box1 + box2 and box1 != box2 \
                    and boxes[box1 - 1] and boxes[box2 - 1]:
                boxes[box1 - 1] = False
                boxes[box2 - 1] = False
                return f"{box1} und {box2} erfolgreich geschlossen."
            else:
                return f"{box1} und {box2} sind keine gültigen Eingaben. Überprüfe ob die Summe der Boxen mit " \
                       f"deiner Summe übereinstimmt, und ob du Boxen auswählst die noch offen sind."

        def spielstand_ausgeben():
            if playerpkt[0] < playerpkt[1]:
                return f'{player1} gewinnt mit {playerpkt[0}} gegen {player2} mit {playerpkt[1]}.'
            elif playerpkt[0] > playerpkt[1]:
                return f'{player2} gewinnt mit {playerpkt[1]} gegen {player1} mit {playerpkt[1]}.'
            elif playerpkt[0] == playerpkt[1]:
                return f'Unentschieden beide Spieler haben {playerpkt[0]}'
            else:
                return "Error #SB01 Unerwarteter Fehler bei der Ausgabe kontaktiere bitte den Botbesitzer"

        if player1.id is not player2.id:
            await ctx.send("Hey <@" + str(playerid) + '> du wurdest herausgefordert zu ShuttheBox! Schreibe "accept" '
                                                      'um die Challegenge zu akzeptieren')

            msg1 = await self.client.wait_for('message', check=check, timeout=60)
            await channel.send('Spieler <@' + str(player2.id) +
                               '> hat die Herausforderung angenommen! \n Challenge startet!'.format(msg1))

            await channel.send(boxesmsg())
            # würfeln
            spieler1dices1 = dice()
            spieler1dices2 = dice()
            await ctx.send(
                f'{player1}hat folgende zwei Zahlen gewürfelt: **{spieler1dices1}** und **{spieler1dices2}**')

            while runde <= 8:

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
