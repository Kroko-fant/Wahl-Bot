import json

from discord.ext import commands

from botdata import botparameters as bp


# class Reactions(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild_id = int(payload.guild_id)
        guild = self.client.get_guild(guild_id)

        channel_id = payload.channel_id
        emoji = payload.emoji
        with open('./data/reactionchannel.json', 'r') as f:
            reacts = json.load(f)
            reactionchannel = reacts[str(guild.id)]

        if int(channel_id) == int(reactionchannel):
            addreactdir = './data/servers/' + str(guild_id) + '/reactions.json'
            with open(addreactdir, 'r') as f:
                reactions = json.load(f)
            user = guild.get_member(payload.user_id)
            rawroleid = (str(reactions[str(emoji)]))
            role = guild.get_role(int(rawroleid))
            await user.add_roles(role)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addreact(self, ctx, emoji, *, roleid):
        addreactdir = './data/servers/' + str(ctx.guild.id) + '/reactions.json'
        with open(addreactdir, 'r') as f:
            reactions = json.load(f)

        reactions[str(emoji)] = str(roleid)

        with open(addreactdir, 'w') as f:
            json.dump(reactions, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send("**Emoji** :" + emoji + ": auf **Rolle mit der ID:** " + roleid + " gebunden!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setreactionchannel(self, ctx, rchannelid):
        guild = ctx.guild
        with open('./data/reactionchannel.json', 'r') as f:
            reacts = json.load(f)

        reacts[str(guild.id)] = str(rchannelid)

        with open('./data/reactionchannel.json', 'w') as f:
            json.dump(reacts, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send("Channel <#" + rchannelid + "> ist jetzt der Channel für Reaction-Roles.")

def setup(client):
    client.add_cog(Reactions(client))
