import datetime

import discord

today = datetime.datetime.today()
datum = today.strftime("%d/%m/%Y")


# Personen
def botowner(ctx):
    return ctx.author.id == 137291894953607168


def user(member):
    if not member.bot:
        return True
    else:
        return False


# Versionen
def apiversion():
    return discord.__version__


def version():
    return "Pre Version 1.1.7"


# Userstatus
async def verifiziert(ctx):
    with open('./data/verified.json', 'r') as f:
        trueuserid = str(ctx.author.id) + '": true'
        data = f.read()
        if trueuserid in data:
            return True
        else:
            return False


async def unverifiziert(ctx):
    with open('./data/verified.json', 'r') as f:
        trueuserid = str(ctx.author.id) + '": true'
        data = f.read()
        if trueuserid in data:
            return False
        else:
            return True


# Tasks
async def delete_cmd(ctx):
    await ctx.channel.purge(limit=1)
