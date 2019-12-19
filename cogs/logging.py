import json

import discord
from discord.ext import commands

from botdata import botparameters as bp


class Logging(commands.Cog):

    def __init__(self, client):
        self.client = client

    # LogChannel setzen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlogchannel(self, ctx, lchannelid):
        """Zum Setzen des Channels wird die Channelid als Argument benötigt.
        Syntax: !setlogchannel <channelid>"""
        guild = ctx.guild
        with open('./data/logchannel.json', 'r') as f:
            logs = json.load(f)

        logs[str(guild.id)] = str(lchannelid)

        with open('./data/logchannel.json', 'w') as f:
            json.dump(logs, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send("Channel <#" + lchannelid + "> ist jetzt der Channel für den Log.", delete_after=bp.deltime)

    @setlogchannel.error
    async def setlogchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorlg01embed = discord.Embed(title="Error #LG01",
                                           description=f'Fehlendes Argument! Syntax: !setlogchannel <channel>'
                                                       f' <channelid>', color=0xff0000)
            await ctx.send(embed=errorlg01embed)

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
                pass
        except Exception:
            pass

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
                pass
        except Exception:
            pass

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
                pass
        except Exception:
            pass

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
                pass
        except Exception:
            pass

    # Nachricht löschen
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        try:
            if payload.guild_id is not None:
                guild = payload.guild_id
                msg = payload.message_id
                content = payload.cached_message.content
                user = payload.cached_message.author
                channel = payload.channel_id
                with open('./data/logchannel.json', 'r') as f:
                    logs = json.load(f)
                logchannelid = logs[str(guild)]
                logch = self.client.get_channel(int(logchannelid))
                if (len(content) > 1800):
                    await logch.send(':recycle: **Nachricht:**')
                    await logch.send(str(content).replace("@", "👤"))
                    await logch.send('von User: ' + str(user) + ' (' + str(user.id) + ") in Channel: " + str(channel) +
                                     " gelöscht.")
                else:
                    await logch.send(':recycle: **Nachricht: **' + str(content).replace("@", "👤") + 'von User: ' +
                                     str(user) + ' (' + str(user.id) + ") in Channel: " + str(channel) + " gelöscht.")
        except Exception:
            pass

    # Voice-Änderungen
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
                        ":mega: **" + str(member) + " (" + str(member.id) + ")** hat den Voice Channel von **" +
                        str(before.channel) + "** zu **" + str(after.channel) + "** gewechselt.")
            else:
                pass
        except Exception:
            pass


def setup(client):
    client.add_cog(Logging(client))
