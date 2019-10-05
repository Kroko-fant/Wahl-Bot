import datetime

import discord

version = "Pre Version 1.1.6b"
today = datetime.datetime.today()
datum = today.strftime("%d/%m/%Y")


def botowner(ctx):
    return ctx.author.id == 137291894953607168


def user(member):
    if not member.bot:
        return True
    else:
        return False


def apiversion():
    return discord.__version__


async def verifiziert(ctx):
    with open('./data/verified.json', 'r') as f:
        trueuserid = str(ctx.author.id) + '": true'
        data = f.read()
        if trueuserid in data:
            return True
        else:
            return False
