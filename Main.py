import SECRETS
import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix=".")
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


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(filename[:-3] + ' aktiviert')
    elif filename.endswith('__pycache__'):
        print('Py-Cache gefunden')
    else:
        print(F'{filename}' + ' ist fehlerhaft')
print('Module geladen')

client.run(SECRETS.TOKEN)