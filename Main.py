import json
import os
from _ast import Pass

import discord
from discord.ext import commands

import SECRETS
from botdata import botparameters as bp


def get_prefix(message):
    try:
        with open('./data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(message.guild.id)]
    except KeyError:
        return '!'


client = commands.Bot(command_prefix=get_prefix)
modulliste = []
server = client.guilds
print('Module werden geladen')


# Botstart
@client.event
async def on_ready():
    print('{0.user} ist jetzt online'.format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Bot online und bereit'))
    print('Status geändert')
    number = 0
    for s in range(len(client.guilds)):
        number += 1
    print('Bot läuft auf', number, 'Servern')


@client.command()
@commands.check(bp.botowner)
async def load(ctx, extension):
    e = extension.lower()
    client.load_extension(f'cogs.{e}')
    print(e + ' aktiviert')


@client.command()
@commands.check(bp.botowner)
async def unload(ctx, extension):
    e = extension.lower()
    client.unload_extension(f'cogs.{e}')
    print(e + ' deaktiviert')


@client.command()
@commands.check(bp.botowner)
async def reload(ctx, extension):
    e = extension.lower()
    client.reload_extension(f'cogs.{e}')
    print(e + ' neugeladen')


@client.command()
@commands.check(bp.botowner)
async def module(ctx):
    await ctx.send(modulliste)


@client.command()
@commands.check(bp.botowner)
async def shutdown(ctx):
    await ctx.send("Bot wird heruntergefahren...")
    await client.logout()


for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        if filename.startswith('test'):
            try:
                client.load_extension(f'cogs.{filename[:-3]}')
            except Exception as e:
                print("TestModul " + f'{filename}' + " ist fehlerhaft")
        else:
            if filename.endswith('.py'):
                client.load_extension(f'cogs.{filename[:-3]}')
                print(filename[:-3] + ' aktiviert')
                modulliste.append({filename[:-3]})
            elif filename.endswith('__pycache__'):
                print('Py-Cache gefunden')
            else:
                print(F'{filename}' + ' ist fehlerhaft')
    else:
        Pass

print('Module geladen')
print(modulliste)

print("Botstart abgeschlossen!")
client.run(SECRETS.TOKEN)
