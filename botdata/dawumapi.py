import json
import urllib
from urllib import request

import discord

with urllib.request.urlopen("https://api.dawum.de/") as response:
    data = json.loads(response.read())
lastupdate = data['Database']['Last_Update']


async def update_data():
    with urllib.request.urlopen("https://api.dawum.de/") as response:
        global data
        data = json.loads(response.read())


# Bundesländer
def search_parliament(shortcode):
    if any([code in shortcode.lower() for code in ['bt', 'bundestag']]):
        return 0
    elif any([code in shortcode.lower() for code in ['bw', 'bawü', 'de-bw', 'baden', 'badenwüttenberg']]):
        return 1
    elif any([code in shortcode.lower() for code in ['by', 'bay', 'de-by', 'bayern']]):
        return 2
    elif any([code in shortcode.lower() for code in ['be', 'de-be', 'berlin', 'ber']]):
        return 3
    elif any([code in shortcode.lower() for code in ['bb', 'de-bb', 'brandenburg', 'brand']]):
        return 4
    elif any([code in shortcode.lower() for code in ['hb', 'de-hb', 'bremen']]):
        return 5
    elif any([code in shortcode.lower() for code in ['hh', 'de-hh', 'hamburg', 'ham']]):
        return 6
    elif any([code in shortcode.lower() for code in ['he', 'de-he', 'hessen']]):
        return 7
    elif any([code in shortcode.lower() for code in ['mv', 'de-mv', 'mecklemburg', 'vorpommern',
                                                     'mecklenburg-vorpommern']]):
        return 8
    elif any([code in shortcode.lower() for code in ['ni', 'de-ni', 'nieder', 'nie', 'niedersachsen']]):
        return 9
    elif any([code in shortcode.lower() for code in ['nw', 'de-nw', 'nrw', 'nordrhein', 'westfalen',
                                                     'nordreihn-westfalen']]):
        return 10
    elif any([code in shortcode.lower() for code in ['rp', 'de-rp', 'rheinland', 'pfalz', 'rheinland-pfalz']]):
        return 11
    elif any([code in shortcode.lower() for code in ['sl', 'de-sl', 'saarland', 'saar']]):
        return 12
    elif any([code in shortcode.lower() for code in ['st', 'de-st', 'sachsen-anhalt', 'anhalt']]):
        return 14
    elif any([code in shortcode.lower() for code in ['sn', 'de-sn', 'sachsen', 'sac']]):
        return 13
    elif any([code in shortcode.lower() for code in ['sh', 'de-sh', 'schleswig', 'holstein', 'schleswig-holstein']]):
        return 15
    elif any([code in shortcode.lower() for code in ['th', 'de-th', 'thüringen', 'thü']]):
        return 16
    elif any([code in shortcode.lower() for code in ['eu', 'europa']]):
        return 17
    else:
        return 'Error'


def search_party(shortcode):
    if shortcode.lower() == 'sonstige':
        return 0
    elif shortcode.lower() == 'cducsu':
        return 1
    elif shortcode.lower() == 'spd':
        return 2
    elif shortcode.lower() == 'fdp':
        return 3
    elif shortcode.lower() == 'gruene':
        return 4
    elif shortcode.lower() == 'linke':
        return 5
    elif shortcode.lower() == 'piraten':
        return 6
    elif shortcode.lower() == 'afd':
        return 7
    elif shortcode.lower() == 'fw':
        return 8
    elif shortcode.lower() == 'ssw':
        return 10
    elif shortcode.lower() == 'diepartei':
        return 13
    elif shortcode.lower() == 'bvb':
        return 14
    elif shortcode.lower() == 'tierschutz':
        return 15
    elif shortcode.lower() == 'biw':
        return 16
    elif shortcode.lower() == 'cdu':
        return 101
    elif shortcode.lower() == 'csu':
        return 102
    else:
        return 'Error'


def search_newest_poll(shortcode):
    if shortcode.isdigit():
        parlament = int(shortcode)
    else:
        parlament = search_parliament(shortcode)
    newest = max((k for k, v in data['Surveys'].items() if v['Parliament_ID'] == str(parlament)), key=int)
    return newest


def umfrage_ausgeben(userinput):
    if userinput.isdigit() and int(userinput) > 100:
        umfragenid = userinput
    elif userinput.isdigit() and int(userinput) < 100:
        umfragenid = search_newest_poll(userinput)
    else:
        umfragenid = search_newest_poll(userinput)

    parlament = data['Parliaments'][data['Surveys'][umfragenid]['Parliament_ID']]['Name']
    institut = data['Institutes'][data['Surveys'][umfragenid]['Institute_ID']]['Name']
    time = data['Surveys'][umfragenid]['Date']

    output = 'von **' + str(institut) + '** am ' + str(time) + "\n"

    for elements in data['Surveys'][umfragenid]['Results']:
        element = data['Parties'][elements]['Shortcut']
        if element != 'None':
            output = str(output) + "\n**" + str(element) + "**: " + \
                     str(data['Surveys'][umfragenid]['Results'][elements]) + " %"

    wahlembed = discord.Embed(title=str(parlament), description=output,
                              color=12370112)
    wahlembed.set_footer(text="UmfragenId: " + str(umfragenid) + "\n Daten aus der Dawum APi: " + "https://dawum.de/")

    return wahlembed