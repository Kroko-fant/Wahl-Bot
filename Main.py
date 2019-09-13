import json
import os

import discord
from discord.ext import commands

import SECRETS


def get_prefix(client, message):
    with open('./Data/prefixes.json', 'r') as prefix:
        prefixes = json.load(prefix)

    return prefixes[str(message.guild.id)]


def botowner(ctx):
    return ctx.author.id == 137291894953607168


client = commands.Bot(command_prefix=get_prefix)
modulliste = []
testmodule = []

print('Module werden geladen')


# Botstart
@client.event
async def on_ready():
    print('{0.user} ist jetzt online'.format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Bot online und bereit'))
    print('Status geändert')
    print('------------------------------------------------------------------')
    for s in client.guilds:
        print(s)
    print('------------------------------------------------------------------')


# Start-Prefix
@client.event
async def on_guild_join(guild):
    with open('./Data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('./Data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('./Data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop[str(guild.id)] = '!'

    with open('./Data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command()
@commands.check(botowner)
async def newprefix(ctx, prefix):
    with open('./Data/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('./Data/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix zu: {prefix} geändert')


@client.command()
@commands.check(botowner)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(extension + ' aktiviert')


@client.command()
@commands.check(botowner)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(extension + ' deaktiviert')


@client.command()
@commands.check(botowner)
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')
    print(extension + ' neugeladen')


@client.command()
@commands.check(botowner)
async def module(ctx):
    await ctx.send(modulliste)


@client.command()
@commands.check(botowner)
async def restart(ctx):
    await client.logout()
    await client.run(SECRETS.TOKEN)


@client.command()
@commands.check(botowner)
async def shutdown(ctx):
    await client.logout()
    await ctx.send("Bot wird heruntergefahren...")


for filename in os.listdir('./cogs'):
    if filename.startswith('test'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
        except Exception as e:
            print("TestModul " + f'{filename}' + "ist fehlerhaft")
        testmodule.append({filename[:-3]})
    else:
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(filename[:-3] + ' aktiviert')
            modulliste.append({filename[:-3]})
        elif filename.endswith('__pycache__'):
            print('Py-Cache gefunden')
        else:
            print(F'{filename}' + ' ist fehlerhaft')
print('Module geladen')
print(modulliste)

print("Botstart abgeschlossen!")
client.run(SECRETS.TOKEN)
