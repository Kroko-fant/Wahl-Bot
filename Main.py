import SECRETS
import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix=".")
modulliste = []
testmodule = []
print('Module werden geladen')


@client.event
async def on_ready():
    print('{0.user} ist jetzt online'.format(client))
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Bot online und bereit'))
    print('Status geändert')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print(extension + ' aktiviert')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print(extension + ' deaktiviert')


@client.command()
async def module(ctx):
    await ctx.send(modulliste)


for filename in os.listdir('./cogs'):
    if filename.startswith('test'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}')
        except:
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

client.run(SECRETS.TOKEN)
