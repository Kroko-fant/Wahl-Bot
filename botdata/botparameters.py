import discord

deltime = 30
deltime2 = 60


# Personen
def botowner(ctx):
    return ctx.author.id == 137291894953607168


def ultimatebotid():
    return 612702321985585172


def user(member):
    if not member.bot:
        return True
    else:
        return False


# Versionen
def apiversion():
    apiversionstr = discord.__version__
    return apiversionstr


# Userstatus
async def verifiziert(ctx):
    verifydir = './data/servers/' + str(ctx.guild.id) + '/verified.json'
    with open(verifydir, 'r') as f:
        trueuserid = str(ctx.author.id) + '": true'
        data = f.read()
        if trueuserid in data:
            return True
        else:
            return False


async def unverifiziert(ctx):
    verifydir = './data/servers/' + str(ctx.guild.id) + '/verified.json'
    with open(verifydir, 'r') as f:
        trueuserid = str(ctx.author.id) + '": true'
        data = f.read()
        if trueuserid in data:
            return False
        else:
            return True


# Tasks
async def delete_cmd(ctx):
    await ctx.channel.purge(limit=1)
