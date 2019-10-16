import datetime
import json

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
    apiversionstr = discord.__version__
    return apiversionstr


def version():
    versionstr = "Pre Version 1.1.8"
    return versionstr


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


def update_member(member):
    with open('./data/lastmsg.json', 'r') as f:
        members = json.load(f)

    members[str(member.id)] = str(datum)

    with open('./data/lastmsg.json', 'w') as f:
        json.dump(members, f, indent=4)
