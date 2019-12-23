import json
from ast import Pass

from discord.ext import commands

from botdata import botparameters as bp


class Logging(commands.Cog):

    def __init__(self, client):
        self.client = client

    # LogChannel setzen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlogchannel(self, ctx, lchannelid):
        guild = ctx.guild
        with open('./data/logchannel.json', 'r') as f:
            logs = json.load(f)

        logs[str(guild.id)] = str(lchannelid)

        with open('./data/logchannel.json', 'w') as f:
            json.dump(logs, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send("Channel <#" + lchannelid + "> ist jetzt der Channel für den Log.", delete_after=bp.deltime)

    # Memberjoin
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            if bp.user(member):
                guild = member.guild
                with open('./data/logchannel.json', 'r') as f:
                    logs = json.load(f)
                logchannelid = logs[str(guild.id)]
                logch = self.client.get_channel(int(logchannelid))
                await logch.send(
                    ":inbox_tray: **" + str(member) + "(" + str(member.id) + ")** ist dem Sever beigetreten.")
            else:
                Pass
        except Exception:
            Pass

    # Memberleave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            if bp.user(member):
                guild = member.guild
                with open('./data/logchannel.json', 'r') as f:
                    logs = json.load(f)
                logchannelid = logs[str(guild.id)]
                logch = self.client.get_channel(int(logchannelid))
                await logch.send(
                    ":outbox_tray: **" + str(member) + " (" + str(member.id) + ")** hat den Server verlassen.")
            else:
                Pass
        except Exception:
            Pass

    # Member wird gebannt
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            if bp.user(user):
                with open('./data/logchannel.json', 'r') as f:
                    logs = json.load(f)
                logchannelid = logs[str(guild.id)]
                logch = self.client.get_channel(int(logchannelid))
                await logch.send(":no_entry_sign: **" + str(user) + " (" + str(user.id) + ")** wurde gebannt.")
            else:
                Pass
        except Exception:
            Pass

    # Member wird entbannt
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        try:
            if bp.user(user):
                with open('./data/logchannel.json', 'r') as f:
                    logs = json.load(f)
                logchannelid = logs[str(guild.id)]
                logch = self.client.get_channel(int(logchannelid))
                await logch.send(":white_check_mark: **" + str(user) + " (" + str(user.id) + ")** wurde entgebannt.")
            else:
                Pass
        except Exception:
            Pass

    # Nachricht löschen
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        try:
            if payload.guild_id is not None:
                ch = payload.channel_id
                guild = payload.guild_id
                msg = payload.message_id
                content = payload.cached_message.content
                user = payload.cached_message.author
                channel = payload.channel_id
                with open('./data/logchannel.json', 'r') as f:
                    logs = json.load(f)
                logchannelid = logs[str(guild)]
                logch = self.client.get_channel(int(logchannelid))
                await logch.send(':recycle: **Nachricht:** "' + str(content) + '" von User: ' + str(user) + ' (' +
                                 str(user.id) + ") in Channel " + str(channel) + " gelöscht.")
        except Exception:
            Pass

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            guild = member.guild
            if bp.user(member):
                with open('./data/logchannel.json', 'r') as f:
                    logs = json.load(f)
                logchannelid = logs[str(guild.id)]
                logch = self.client.get_channel(int(logchannelid))
                if before.channel is None:
                    await logch.send(
                        ":mega: **" + str(member) + " (" + str(member.id) + ")** hat den Voice Channel **" +
                        str(after.channel) + "** betreten.")
                elif before.channel is not None and after.channel is None:
                    await logch.send(
                        ":mega: **" + str(member) + " (" + str(member.id) + ")** hat den Voice Channel **" +
                        str(before.channel) + "** verlassen.")
                elif before.channel is not None and after.channel is not None:
                    await logch.send(
                        f":mega: **{str(member)} ({str(member.id)} )** hat den Voice Channel von ** "
                        f"{str(before.channel)} ** zu ** {str(after.channel)}** gewechselt.")
            else:
                Pass
        except Exception:
            Pass


def setup(client):
    client.add_cog(Logging(client))
