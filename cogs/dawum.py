import json
import urllib

import discord
from discord.ext import commands

from botdata import botparameters as bp


class Dawum(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Bundesländer
    async def search_parliament(self, shortcode):
        parlamentcodes = {'bt': 0, 'bundestag': 0, 'bw': 1, 'bawü': 1, 'de-bw': 1, 'baden': 1, 'badenwüttenberg': 1,
                          'by': 2, 'bay': 2, 'de-by': 2, 'bayern': 2, 'be': 3, 'de-be': 3, 'berlin': 3, 'ber': 3,
                          'bb': 4, 'de-bb': 4, 'brandenburg': 4, 'brand': 4, 'hb': 5, 'de-hb': 5, 'bremen': 5, 'hh': 6,
                          'de-hh': 6, 'hamburg': 6, 'ham': 6, 'he': 7, 'de-he': 7, 'hessen': 7, 'mv': 8, 'de-mv': 8,
                          'mecklemburg': 8, 'vorpommern': 8, 'mecklenburg-vorpommern': 8, 'ni': 9, 'de-ni': 9, 'nie': 9,
                          'nieder': 9, 'niedersachsen': 9, 'nw': 10, 'de-nw': 10, 'nrw': 10, 'nordrhein': 10,
                          'westfalen': 10, 'nordreihn-westfalen': 10, 'rp': 11, 'de-rp': 11, 'rheinland-pfalz': 11,
                          'rheinland': 11, 'pfalz': 11, 'sl': 12, 'de-sl': 12, 'saarland': 12, 'saar': 12, 'sn': 13,
                          'de-sn': 13, 'sachsen': 13, 'sac': 13, 'st': 14, 'de-st': 14, 'sachsen-anhalt': 14,
                          'anhalt': 14, 'sh': 15, 'de-sh': 15, 'schleswig-holstein': 15, 'schleswig': 15,
                          'holstein': 15, 'th': 16, 'de-th': 16, 'thüringen': 16, 'thü': 16, 'eu': 17, 'europa': 17}
        return str(parlamentcodes.get(shortcode.lower(), 'Error'))

    async def search_party(self, shortcode):
        partycodes = {'sonstige': 0, 'cducsu': 1, 'spd': 2, 'fdp': 3, 'gruene': 4, 'linke': 5, 'piraten': 6, 'afd': 7,
                      'fw': 8, 'ssw': 10, 'bp': 11, 'diepartei': 13, 'bvb': 14, 'tierschutz': 15, 'biw': 16, 'cdu': 101,
                      'csu': 102}

        return partycodes.get(shortcode.lower(), 'Error')

    async def umfrage_ausgeben(self, userinput):
        data = json.loads(urllib.request.urlopen("https://api.dawum.de/").read())
        if userinput.isdigit() and int(userinput) > 100:
            umfragenid = userinput
        elif userinput.isdigit() and int(userinput) < 100:
            umfragenid = max((k for k, v in data['Surveys'].items() if v['Parliament_ID'] == userinput), key=int)
        else:
            parlament = await self.search_parliament(userinput)
            umfragenid = max((k for k, v in data['Surveys'].items() if v['Parliament_ID'] == parlament), key=int)

        output = f"von **{data['Institutes'][data['Surveys'][umfragenid]['Institute_ID']]['Name']}** am" \
                 f" {data['Surveys'][umfragenid]['Date']}\n"

        for elements in data['Surveys'][umfragenid]['Results']:
            if data['Parties'][elements]['Shortcut'] != 'None':
                output += f"\n** {data['Parties'][elements]['Shortcut']}**: " \
                          f"{data['Surveys'][umfragenid]['Results'][elements]} %"

        wahlembed = discord.Embed(title=data['Parliaments'][data['Surveys'][umfragenid]['Parliament_ID']]['Name'],
                                  description=output, color=12370112)
        wahlembed.set_footer(text=f"UmfragenId: {umfragenid}\n Daten aus der Dawum APi: https://dawum.de/")

        return wahlembed

    @commands.command()
    async def poll(self, ctx, pollinput):
        """Gebe die aktuelle Wahlumfrage aus.
        Syntax: !poll <ländercode>
        Der Ländercode ist optional. Alle Ländercodes sind intuitiv. Bundesländer ausschreiben möglich."""
        if pollinput is None:
            dawumoutput = await self.umfrage_ausgeben("0")
            await bp.delete_cmd(ctx)
            await ctx.send(embed=dawumoutput)
        elif pollinput == "help":
            await bp.delete_cmd(ctx)
            wahlhelfembed = discord.Embed(title="Hilfe zum Befehl !poll",
                                          description="Verwendung: !poll oder !poll <Argument>. Als Argumente sind "
                                                      "Länderkürzel, Namen o.ä. zugelassen", color=12370112)
            await ctx.send(embed=wahlhelfembed, delete_after=bp.deltime)
        else:
            dawumoutput = await self.umfrage_ausgeben(pollinput)
            await bp.delete_cmd(ctx)
            await ctx.send(embed=dawumoutput)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await bp.delete_cmd(ctx)
            await ctx.send(embed=await self.umfrage_ausgeben('0'))


def setup(client):
    client.add_cog(Dawum(client))
