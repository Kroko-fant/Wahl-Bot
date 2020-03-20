import json
from ast import Pass

from discord.ext import commands

from botdata import botparameters as bp
from botdata import raidprotectiontimers as rpt


class Raidprotection(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Member betritt Server => Raid-Protection tritt in Kraft
    @commands.Cog.listener()
    async def on_member_join(self, member):
        rpt.printtimers()
        if rpt.timer1 == 0:
            # Timer 1 Starten
            rpt.timer1 = rpt.timer1 + 1

            # Andere Timer gegenchecken
            if rpt.timer2 > 0:
                rpt.timer2 = rpt.timer2 + 1
            if rpt.timer3 > 0:
                rpt.timer3 = rpt.timer3 + 1
            if rpt.timer4 > 0:
                rpt.timer4 = rpt.timer4 + 1
            if rpt.timer5 > 0:
                rpt.timer5 = rpt.timer5 + 1
            if rpt.timer6 > 0:
                rpt.timer6 = rpt.timer6 + 1
            if rpt.timer7 > 0:
                rpt.timer7 = rpt.timer7 + 1
            if rpt.timer8 > 0:
                rpt.timer8 = rpt.timer8 + 1
            if rpt.timer9 > 0:
                rpt.timer9 = rpt.timer9 + 1
            if rpt.timer10 > 0:
                rpt.timer10 = rpt.timer10 + 1
            rpt.printtimers()
            rpt.cleartimer1()
        else:
            if rpt.timer2 == 0:
                # Timer 2 Starten
                rpt.timer2 = rpt.timer1 + 1

                # Andere Timer gegenchecken
                if rpt.timer1 > 0:
                    rpt.timer1 = rpt.timer1 + 1
                if rpt.timer3 > 0:
                    rpt.timer3 = rpt.timer3 + 1
                if rpt.timer4 > 0:
                    rpt.timer4 = rpt.timer4 + 1
                if rpt.timer5 > 0:
                    rpt.timer5 = rpt.timer5 + 1
                if rpt.timer6 > 0:
                    rpt.timer6 = rpt.timer6 + 1
                if rpt.timer7 > 0:
                    rpt.timer7 = rpt.timer7 + 1
                if rpt.timer8 > 0:
                    rpt.timer8 = rpt.timer8 + 1
                if rpt.timer9 > 0:
                    rpt.timer9 = rpt.timer9 + 1
                if rpt.timer10 > 0:
                    rpt.timer10 = rpt.timer10 + 1

                # Timer2 resetten
                rpt.printtimers()
                rpt.cleartimer2()

            else:
                # Timer 3 Starten
                if rpt.timer3 == 0:
                    rpt.timer3 = rpt.timer3 + 1

                    # Andere Timer gegenchecken
                    if rpt.timer1 > 0:
                        rpt.timer1 = rpt.timer1 + 1
                    if rpt.timer2 > 0:
                        rpt.timer2 = rpt.timer2 + 1
                    if rpt.timer4 > 0:
                        rpt.timer4 = rpt.timer4 + 1
                    if rpt.timer5 > 0:
                        rpt.timer5 = rpt.timer5 + 1
                    if rpt.timer6 > 0:
                        rpt.timer6 = rpt.timer6 + 1
                    if rpt.timer7 > 0:
                        rpt.timer7 = rpt.timer7 + 1
                    if rpt.timer8 > 0:
                        rpt.timer8 = rpt.timer8 + 1
                    if rpt.timer9 > 0:
                        rpt.timer9 = rpt.timer9 + 1
                    if rpt.timer10 > 0:
                        rpt.timer10 = rpt.timer10 + 1

                    # Timer3 resetten
                    rpt.printtimers()
                    rpt.cleartimer3()

                else:
                    # Timer 4 Starten
                    if rpt.timer4 == 0:
                        rpt.timer4 = rpt.timer4 + 1

                        # Andere Timer gegenchecken
                        if rpt.timer1 > 0:
                            rpt.timer1 = rpt.timer1 + 1
                        if rpt.timer2 > 0:
                            rpt.timer2 = rpt.timer2 + 1
                        if rpt.timer3 > 0:
                            rpt.timer3 = rpt.timer3 + 1
                        if rpt.timer5 > 0:
                            rpt.timer5 = rpt.timer5 + 1
                        if rpt.timer6 > 0:
                            rpt.timer6 = rpt.timer6 + 1
                        if rpt.timer7 > 0:
                            rpt.timer7 = rpt.timer7 + 1
                        if rpt.timer8 > 0:
                            rpt.timer8 = rpt.timer8 + 1
                        if rpt.timer9 > 0:
                            rpt.timer9 = rpt.timer9 + 1
                        if rpt.timer10 > 0:
                            rpt.timer10 = rpt.timer10 + 1

                        # Timer4 resetten
                        rpt.printtimers()
                        rpt.cleartimer4()

                    else:
                        # Timer 5 Starten
                        if rpt.timer5 == 0:
                            rpt.timer5 = rpt.timer5 + 1

                            # Andere Timer gegenchecken
                            if rpt.timer1 > 0:
                                rpt.timer1 = rpt.timer1 + 1
                            if rpt.timer2 > 0:
                                rpt.timer2 = rpt.timer2 + 1
                            if rpt.timer3 > 0:
                                rpt.timer3 = rpt.timer3 + 1
                            if rpt.timer4 > 0:
                                rpt.timer4 = rpt.timer4 + 1
                            if rpt.timer6 > 0:
                                rpt.timer6 = rpt.timer6 + 1
                            if rpt.timer7 > 0:
                                rpt.timer7 = rpt.timer7 + 1
                            if rpt.timer8 > 0:
                                rpt.timer8 = rpt.timer8 + 1
                            if rpt.timer9 > 0:
                                rpt.timer9 = rpt.timer9 + 1
                            if rpt.timer10 > 0:
                                rpt.timer10 = rpt.timer10 + 1

                            # Timer5 resetten
                            rpt.printtimers()
                            rpt.cleartimer5()

                        else:
                            # Timer 6 Starten
                            if rpt.timer6 == 0:
                                rpt.timer6 = rpt.timer6 + 1

                                # Andere Timer gegenchecken
                                if rpt.timer1 > 0:
                                    rpt.timer1 = rpt.timer1 + 1
                                if rpt.timer2 > 0:
                                    rpt.timer2 = rpt.timer2 + 1
                                if rpt.timer3 > 0:
                                    rpt.timer3 = rpt.timer3 + 1
                                if rpt.timer4 > 0:
                                    rpt.timer4 = rpt.timer4 + 1
                                if rpt.timer5 > 0:
                                    rpt.timer5 = rpt.timer5 + 1
                                if rpt.timer7 > 0:
                                    rpt.timer7 = rpt.timer7 + 1
                                if rpt.timer8 > 0:
                                    rpt.timer8 = rpt.timer8 + 1
                                if rpt.timer9 > 0:
                                    rpt.timer9 = rpt.timer9 + 1
                                if rpt.timer10 > 0:
                                    rpt.timer10 = rpt.timer10 + 1

                                # Timer6 resetten
                                rpt.printtimers()
                                rpt.cleartimer6()

                            else:
                                # Timer 7 Starten
                                if rpt.timer7 == 0:
                                    rpt.timer7 = rpt.timer7 + 1

                                    # Andere Timer gegenchecken
                                    if rpt.timer1 > 0:
                                        rpt.timer1 = rpt.timer1 + 1
                                    if rpt.timer2 > 0:
                                        rpt.timer2 = rpt.timer2 + 1
                                    if rpt.timer3 > 0:
                                        rpt.timer3 = rpt.timer3 + 1
                                    if rpt.timer4 > 0:
                                        rpt.timer4 = rpt.timer4 + 1
                                    if rpt.timer5 > 0:
                                        rpt.timer5 = rpt.timer5 + 1
                                    if rpt.timer6 > 0:
                                        rpt.timer6 = rpt.timer6 + 1
                                    if rpt.timer8 > 0:
                                        rpt.timer8 = rpt.timer8 + 1
                                    if rpt.timer9 > 0:
                                        rpt.timer9 = rpt.timer9 + 1
                                    if rpt.timer10 > 0:
                                        rpt.timer10 = rpt.timer10 + 1
                                    # Timer7 resetten
                                    rpt.printtimers()
                                    rpt.cleartimer7()

                                else:
                                    # Timer 8 Starten
                                    if rpt.timer8 == 0:
                                        rpt.timer8 = rpt.timer8 + 1

                                        # Andere Timer gegenchecken
                                        if rpt.timer1 > 0:
                                            rpt.timer1 = rpt.timer1 + 1
                                        if rpt.timer2 > 0:
                                            rpt.timer2 = rpt.timer2 + 1
                                        if rpt.timer3 > 0:
                                            rpt.timer3 = rpt.timer3 + 1
                                        if rpt.timer4 > 0:
                                            rpt.timer4 = rpt.timer4 + 1
                                        if rpt.timer5 > 0:
                                            rpt.timer5 = rpt.timer5 + 1
                                        if rpt.timer6 > 0:
                                            rpt.timer6 = rpt.timer6 + 1
                                        if rpt.timer7 > 0:
                                            rpt.timer7 = rpt.timer7 + 1
                                        if rpt.timer9 > 0:
                                            rpt.timer9 = rpt.timer9 + 1
                                        if rpt.timer10 > 0:
                                            rpt.timer10 = rpt.timer10 + 1

                                        # Timer8 resetten
                                        rpt.printtimers()
                                        rpt.cleartimer8()

                                    else:  # Timer 9 Starten
                                        if rpt.timer9 == 0:
                                            rpt.timer9 = rpt.timer9 + 1

                                            # Andere Timer gegenchecken
                                            if rpt.timer1 > 0:
                                                rpt.timer1 = rpt.timer1 + 1
                                            if rpt.timer2 > 0:
                                                rpt.timer2 = rpt.timer2 + 1
                                            if rpt.timer3 > 0:
                                                rpt.timer3 = rpt.timer3 + 1
                                            if rpt.timer4 > 0:
                                                rpt.timer4 = rpt.timer4 + 1
                                            if rpt.timer5 > 0:
                                                rpt.timer5 = rpt.timer5 + 1
                                            if rpt.timer6 > 0:
                                                rpt.timer6 = rpt.timer6 + 1
                                            if rpt.timer7 > 0:
                                                rpt.timer7 = rpt.timer7 + 1
                                            if rpt.timer8 > 0:
                                                rpt.timer8 = rpt.timer8 + 1
                                            if rpt.timer10 > 0:
                                                rpt.timer10 = rpt.timer10 + 1

                                            # Timer9 resetten
                                            rpt.printtimers()
                                            rpt.cleartimer9()

                                        else:  # Timer 10 Starten
                                            if rpt.timer10 == 0:
                                                rpt.timer10 = rpt.timer10 + 1

                                                # Andere Timer gegenchecken
                                                if rpt.timer1 > 0:
                                                    rpt.timer1 = rpt.timer1 + 1
                                                if rpt.timer2 > 0:
                                                    rpt.timer2 = rpt.timer2 + 1
                                                if rpt.timer3 > 0:
                                                    rpt.timer3 = rpt.timer3 + 1
                                                if rpt.timer4 > 0:
                                                    rpt.timer4 = rpt.timer4 + 1
                                                if rpt.timer5 > 0:
                                                    rpt.timer5 = rpt.timer5 + 1
                                                if rpt.timer6 > 0:
                                                    rpt.timer6 = rpt.timer6 + 1
                                                if rpt.timer7 > 0:
                                                    rpt.timer7 = rpt.timer7 + 1
                                                if rpt.timer8 > 0:
                                                    rpt.timer8 = rpt.timer8 + 1
                                                if rpt.timer9 > 0:
                                                    rpt.timer9 = rpt.timer9 + 1

                                                # Timer10 resetten
                                                rpt.printtimers()
                                                rpt.cleartimer10()

        if rpt.checkraid():
            # Checken ob ein Raid aktiv ist
            print("raid=True")
            try:
                guild = member.guild
                with open('./data/roles/raiderrole.json', 'r') as f:
                    roles = json.load(f)
                roleid = (roles[str(guild.id)])
                role = guild.get_role(roleid)
                await member.add_roles(role, reason="raid")
            except KeyError:
                Pass
        else:
            print("raid=False")

    # Raiderrolle setzen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setraiderrole(self, ctx, roleid):
        with open('./data/roles/raiderrole.json', 'r') as f:
            roles = json.load(f)

        roles[str(ctx.guild.id)] = int(roleid)

        with open('./data/roles/raiderrole.json', 'w') as f:
            json.dump(roles, f, indent=4)
        await ctx.send("Raider-Rolle gesetzt.", delete_after=bp.deltime)
        await bp.delete_cmd(ctx)


def setup(client):
    client.add_cog(Raidprotection(client))
