import json
import logging
import os

import discord
from discord.ext import commands

import SECRETS
from botdata import botparameters as bp


def get_prefix(client, message):
    if message.guild is not None:
        try:
            with open('./data/prefixes.json', 'r') as f:
                prefixes = json.load(f)
            return prefixes[str(message.guild.id)]
        except KeyError:
            return '!'
    else:
        return '!'


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = commands.Bot(command_prefix=get_prefix)
print('Module werden geladen')


# Botstart
@client.event
async def on_ready():
    print(f'{client.user} ist jetzt online')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Bot online und bereit'))
    print('Status geändert')
    number = 0
    for s in range(len(client.guilds)):
        number += 1
    print(f'Bot läuft auf {number} Servern')


@client.command()
async def ping(ctx):
    """Zeigt den aktuellen Ping"""
    await bp.delete_cmd(ctx)
    await ctx.send(f'Pong! Meine Latenz sind aktuell {round(client.latency * 1000)} ms.')


@client.command()
@commands.is_owner()
async def status(ctx, *, status):
    await client.change_presence(status=discord.Status.online, activity=discord.Game(status))
    await ctx.send(f'Der Status lautet nun: **{status}**')


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    """Lädt ein Modul in den Bot"""
    await bp.delete_cmd(ctx)
    client.load_extension(f'cogs.{extension.lower()}')
    await ctx.send(f":green_circle: {extension} aktiviert")
    print(f'{extension} aktiviert')


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    """Lädt ein Modul aus dem Bot"""
    await bp.delete_cmd(ctx)
    client.unload_extension(f'cogs.{extension.lower()}')
    print(f'{extension} deaktiviert')
    await ctx.send(f':red_circle: {extension} deaktiviert')


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    """Lädt ein Modul neu"""
    await bp.delete_cmd(ctx)
    if extension == "all":
        for filename in os.listdir('./cogs'):
            if filename.endswith(".py"):
                if not filename.startswith('test'):
                    if filename.endswith('.py'):
                        try:
                            client.reload_extension(f'cogs.{filename[:-3]}')
                            await ctx.send(f':white_circle: {filename[:-3]} neugeladen')
                        except Exception:
                            await ctx.send(f':red_circle: {filename[:-3]} konnte nicht neugeladen werden')
            elif filename.endswith('__pycache__'):
                await ctx.send(f':whitecheckmark: Pycache vorhanden')
            else:
                await ctx.send(f"Fehlerhafte File auf dem Server gefunden! {filename}")
    else:
        client.reload_extension(f'cogs.{extension.lower()}')
        await ctx.send(f':white_circle: {extension} neugeladen')


@client.command()
@commands.is_owner()
async def shutdown(ctx):
    """Fährt den Bot herunter.
    Danach muss man ihn auf dem Server in der Console neustarten lol."""
    await bp.delete_cmd(ctx)
    await ctx.send("Bot wird heruntergefahren...")
    await client.logout()


# Module beim Botstart laden
for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        if not filename.startswith('test'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(filename[:-3] + ' aktiviert')
    elif filename.endswith('__pycache__'):
        print('Py-Cache gefunden')
    else:
        print('\x1b[6;30;42m' + f"Fehlerhafte File auf dem Server gefunden! {filename}" + '\x1b[0m')

print('Module geladen')
print("Botstart abgeschlossen!")

client.run(SECRETS.TOKEN)
