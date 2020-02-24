import json
import urllib

import discord
from discord.ext import commands

from botdata import botparameters as bp


class Dawum(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def umfrage_ausgeben(self, userinput, count):
        parlamentcodes = {'bt': 0, 'bundestag': 0, 'bw': 1, 'bawü': 1, 'de-bw': 1, 'baden': 1, 'badenwürttemberg': 1,
                          'by': 2, 'bay': 2, 'de-by': 2, 'bayern': 2, 'be': 3, 'de-be': 3, 'berlin': 3, 'ber': 3,
                          'bb': 4, 'de-bb': 4, 'brandenburg': 4, 'brand': 4, 'hb': 5, 'de-hb': 5, 'bremen': 5, 'hh': 6,
                          'de-hh': 6, 'hamburg': 6, 'ham': 6, 'he': 7, 'de-he': 7, 'hessen': 7, 'mv': 8, 'de-mv': 8,
                          'mecklenburg': 8, 'vorpommern': 8, 'mecklenburg-vorpommern': 8, 'ni': 9, 'de-ni': 9, 'nie': 9,
                          'nieder': 9, 'niedersachsen': 9, 'nw': 10, 'de-nw': 10, 'nrw': 10, 'nordrhein': 10,
                          'westfalen': 10, 'nordrhein-westfalen': 10, 'rp': 11, 'de-rp': 11, 'rheinland-pfalz': 11,
                          'rheinland': 11, 'pfalz': 11, 'sl': 12, 'de-sl': 12, 'saarland': 12, 'saar': 12, 'sn': 13,
                          'de-sn': 13, 'sachsen': 13, 'sac': 13, 'st': 14, 'de-st': 14, 'sachsen-anhalt': 14,
                          'anhalt': 14, 'sh': 15, 'de-sh': 15, 'schleswig-holstein': 15, 'schleswig': 15,
                          'holstein': 15, 'th': 16, 'de-th': 16, 'thüringen': 16, 'thü': 16, 'eu': 17, 'europa': 17}
        partycodes = {'CDU': 101, 'CSU': 102, 'CDU/CSU': 1, 'SPD': 2, 'Die Grünen': 4, 'Afd': 7, 'Linke': 5, 'FDP': 3,
                      'Freie-Wähler': 8, 'Brandenburger Vereinigte Bürgerbewegungen/Freie Wähler': 14, 'Piraten': 6,
                      'Die Partei': 13, 'SSW': 10, 'Bayernpartei': 11, 'Tierschutz': 15, 'Bürger in Wut': 16,
                      'Sonstige': 0}
        data = json.loads(urllib.request.urlopen("https://api.dawum.de/").read())
        if userinput.isdigit():
            umfragenid = [userinput] if int(userinput) > 100 else [int(k) for k, v in data['Surveys'].items()
                                                                   if v['Parliament_ID'] == str(userinput.lower())]
        else:
            umfragenid = [int(k) for k, v in data['Surveys'].items() if v['Parliament_ID'] ==
                          str(parlamentcodes.get(userinput.lower(), 'Error'))]
        if len(umfragenid) < count:
            count = len(umfragenid)
        newids = []
        for ids in range(count):
            newids.append(max(umfragenid))
            umfragenid.remove(max(umfragenid))

        if count == 1:
            output = f"von **{data['Institutes'][data['Surveys'][str(newids[0])]['Institute_ID']]['Name']}** am" \
                     f" {data['Surveys'][str(newids[0])]['Date']}\n"
        else:
            output = f"Die aktuellsten {count} Umfragen.\n"

        for party in partycodes.keys():
            score = 0.0
            for elements in newids:
                try:
                    score += int(data['Surveys'][str(elements)]['Results'][str(partycodes[party])])
                except KeyError:
                    pass
            if score > 0:
                output += f"\n** {party}**: {round(score / count, 2)} %"

        wahlembed = discord.Embed(title=data['Parliaments'][data['Surveys'][str(newids[0])]['Parliament_ID']]['Name'],
                                  description=output, color=12370112)
        wahlembed.set_footer(text=f"UmfragenId: {newids[0]}\n Daten aus der Dawum APi: "
                                  f"https://dawum.de/" if count == 1 else "Daten aus der Dawum APi: https://dawum.de/")

        return wahlembed

    @commands.command(aliases=["umfrage"])
    async def poll(self, ctx, parla="bt", count=1):
        """Gebe die aktuelle Wahlumfrage aus.
        Syntax: !poll <ländercode> <Umfragenzahl>
        Der Ländercode ist optional. Alle Ländercodes sind intuitiv. Umfragenzahl"""
        await bp.delete_cmd(ctx)
        if parla.lower() == "help":
            wahlhelfembed = discord.Embed(description="Verwendung: !poll oder !poll <ländercode> <range>. Länderkürzel "
                                                      "der deutschen Bundesländer, Bundestag oder EU Range beliebig "
                                                      "wählbar (<= 10) und es wird ein gemittelter Durchschnitt "
                                                      "berechnet", title="Hilfe zum Befehl !poll", color=12370112)
            await ctx.send(embed=wahlhelfembed, delete_after=bp.deltime)
        else:
            await ctx.send(embed=await self.umfrage_ausgeben(parla, count))


def setup(client):
    client.add_cog(Dawum(client))
