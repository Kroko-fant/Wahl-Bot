import json
import time

import discord
from discord.ext import commands

from botdata import blacklist as bl
from botdata import botparameters as bp


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    # async def delete_member_from_purge(self, member):
    # TODO: Mitglieder wieder aus purge löschen
    # print("Unfinished")

    async def update_member(self, member):
        lastmember = './data/servers/' + str(member.guild.id) + '/lastdata.json'
        with open(lastmember, 'r') as f:
            members = json.load(f)

        members[str(member.id)] = int(round(time.time() / 8640, 0))

        with open(lastmember, 'w') as f:
            json.dump(members, f, indent=4)

    @commands.command()
    async def verify(self, ctx):
        """Verifiziere deinen Account im Bot.
        Hat ansonsten keine weiteren Funktionen bisher."""
        await bp.delete_cmd(ctx)
        if await bp.unverifiziert(ctx):
            # USERID in Verify
            verifydir = './data/servers/' + str(ctx.guild.id) + '/verified.json'
            with open(verifydir, 'r') as f:
                verified = json.load(f)

            verified[str(ctx.author.id)] = True

            with open(verifydir, 'w') as f:
                json.dump(verified, f, indent=4)
            await ctx.send('Verifiziert')

            # Rolle geben
            with open(verifydir, 'r') as f:
                verified = json.load(f)

            await ctx.author.add_roles(verified[str(ctx.guild.id)], reason="Verify", atomic=True)
            await ctx.send('Verifiziert')
        elif await bp.verifiziert(ctx):
            await ctx.send("Du bist bereits verifiziert!")
        else:
            await ctx.send("Du konntest nicht verifiziert werden! Wende dich an das Team oder versuche es nochmal!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        """Löscht den gewählten Amount an Nachrichten
        Standardmenge: 10"""
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Es wurden **{amount}** Nachrichten gelöscht.", delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Kick-Befehl wurde benutzt"):
        """Kickt den User vom Server
        Syntax: {prefix}kick <@user>"""
        await bp.delete_cmd(ctx)
        await member.kick(reason=reason)
        await ctx.send(f"User **{str(member)}** wurde gekickt.", delete_after=bp.deltime)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorcm01embed = discord.Embed(title="Error #CM01",
                                           description="Fehlende NutzerID! Syntax: kick <userid> oder kick @<user>",
                                           color=0xff0000)
            await ctx.send(embed=errorcm01embed, delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban den User vom Server
        Syntax: {prefix}ban <@user>"""
        await bp.delete_cmd(ctx)
        await member.ban(reason=reason)
        await ctx.send(f"User **{str(member)}** wurde gebannt.", delete_after=bp.deltime)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorcm02embed = discord.Embed(title="Error #CM02",
                                           description="Fehlende NutzerID! Syntax: ban <userid> oder ban @<user>",
                                           color=0xff0000)
            await ctx.send(embed=errorcm02embed, delete_after=bp.deltime)
        elif isinstance(error, commands.BadArgument):
            errorcm03embed = discord.Embed(title="Error #CM03", description="Nutzer konnte nicht gefunden werden!",
                                           color=0xff0000)
            await ctx.send(embed=errorcm03embed, delete_after=bp.deltime)

    # @commands.command()
    # @commands.has_permissions(ban_members=True)
    # async def block(self, message):
    #  """Blockt den User vom Server
    # Syntax: {prefix}block <@user>"""
    # await bp.delete_cmd(message)
    # TODO

    # Member purgen
    @commands.command()
    @commands.check(bp.botowner)
    async def purge(self, ctx, amount=90):
        """Kickt User, welche zu lange nicht auf dem Server aktiv waren."""
        await bp.delete_cmd(ctx)
        if amount >= 90:
            ctx.send("Suche Mitglieder zum purgen... das kann einen Moment dauern!", delete_after=bp.deltime)
            await self.client.wait_for('message', check=lambda message: message.content.lower() == "accept", timeout=60)
        elif 90 > amount > 0:
            ctx.send("Die eingegebene Tageszahl ist zu klein!", delete_after=bp.deltime)
        else:
            ctx.send("Bitte gebe eine natürliche Zahl größer als 90 ein", delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unbanall(self, ctx):
        """Entbannt ALLE User. Dies kann nicht rückgängig gemacht werden."""
        await bp.delete_cmd(ctx)
        bans = await ctx.guild.bans()
        if len(bans) > 0:
            await ctx.send(f"Es wurden **{len(bans)}** User zum entbannen gefunden. Gebe Okay zum entbannen ein.",
                           delete_after=len(bans) + 20)
            await self.client.wait_for('message', check=lambda message: message.content.lower() == "okay", timeout=60)
            await ctx.send(
                f"Starte Unban.\n Dies kann etwas dauern.\n Geschätzte Zeit: **{round(len(bans) / 6.5)}** Sekunden")
            start = time.time()
            x = 0
            while x < len(bans):
                await ctx.guild.unban(bans[x][1], reason="Unbanall")
                x = x + 1
            ende = time.time()
            await ctx.send(
                f"Alle User erfolgreich entbannt. :white_check_mark:\nUserzahl: **{len(bans)}**\n"
                f"Zeit: **{'{:5.3f}'.format(ende - start)}**\nBans/Sekunde: **{round(len(bans) / (ende - start))}**")
        else:
            await ctx.send(f'Es wurden 0 User zum entbannen gefunden.')

    # LogChannel setzen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlogchannel(self, ctx, lchannelid):
        """Setze einen Logkanal
        Zum Setzen des Channels wird die Channelid als Argument benötigt.
        Syntax: !setlogchannel <channelid>"""
        if ctx.guild.get_channel(lchannelid) is not None:
            with open('./data/channel/logchannel.json', 'r') as f:
                logs = json.load(f)

            logs[str(ctx.guild.id)] = str(lchannelid)

            with open('./data/channel/logchannel.json', 'w') as f:
                json.dump(logs, f, indent=4)
            await bp.delete_cmd(ctx)
            await ctx.send(f"Channel <#{lchannelid}> ist jetzt der Channel für den Log.", delete_after=bp.deltime)
        else:
            pass  # TODO ERRORS

    @setlogchannel.error
    async def setlogchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorcm03embed = discord.Embed(title="Error #CM03",
                                           description=f'Fehlendes Argument! Syntax: !setlogchannel <channel>'
                                                       f' <channelid>', color=0xff0000)
            await ctx.send(embed=errorcm03embed)

    # Memberjoin
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not bp.user(member):
            return
        await self.update_member(member)
        try:
            with open('./data/channel/logchannel.json', 'r') as f:
                logs = json.load(f)
            logch = self.client.get_channel(int(logs[str(member.guild.id)]))
            await logch.send(f":inbox_tray: **{str(member)} ({str(member.id)})** ist dem Sever beigetreten.")
        except Exception:
            pass

    # Memberleave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not bp.user(member):
            return
        try:
            with open('./data/channel/logchannel.json', 'r') as f:
                logs = json.load(f)
            logch = self.client.get_channel(int(logs[str(member.guild.id)]))
            await logch.send(f":outbox_tray: **{str(member)} ({str(member.id)})** hat den Server verlassen.")
        except Exception:
            pass

    # Member wird gebannt
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        try:
            if bp.user(user):
                with open('./data/channel/logchannel.json', 'r') as f:
                    logs = json.load(f)
                logch = self.client.get_channel(int(logs[str(guild.id)]))
                await logch.send(f":no_entry_sign: **{str(user)} ({str(user.id)})** wurde gebannt.")
            else:
                pass
        except Exception:
            pass

    # Member wird entbannt
    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        if not bp.user(member):
            return
        try:
            with open('./data/channel/logchannel.json', 'r') as f:
                logs = json.load(f)
            logch = self.client.get_channel(int(logs[str(guild.id)]))
            await logch.send(f":white_check_mark: **{str(member)} ({str(member.id)})** wurde entgebannt.")
        except Exception:
            pass

    # Nachricht löschen
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.guild_id is None:
            return
        content = payload.cached_message.content
        user = payload.cached_message.author
        channel = payload.channel_id
        with open('./data/channel/logchannel.json', 'r') as f:
            logs = json.load(f)
        logch = self.client.get_channel(int(logs[str(payload.guild_id)]))
        if len(content) > 1800:
            await logch.send(':recycle: **Nachricht:**')
            await logch.send(str(content).replace("@", "👤"))
            await logch.send(f'von User: {str(user)} ({str(user.id)}) in Channel: {str(channel)} gelöscht.')
        else:
            await logch.send(f':recycle: **Nachricht: **{str(content).replace("@", "👤")}von User: '
                             f'{str(user)} ({str(user.id)}) in Channel: {str(channel)} gelöscht.')

    # Voice-Änderungen
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not bp.user(member) and member.guild is not None:
            return
        await self.update_member(member)
        try:
            with open('./data/channel/logchannel.json', 'r') as f:
                logs = json.load(f)
            logch = self.client.get_channel(int(logs[str(member.guild.id)]))
            if before.channel is None:
                await logch.send(f":mega: **{str(member)} ({str(member.id)})** hat den Voice Channel "
                                 f"**{str(before.channel)}** verlassen.")
            elif before.channel is not None and after.channel is None:
                await logch.send(f":mega: **{str(member)} ({str(member.id)})** hat den Voice Channel "
                                 f"**{str(before.channel)}** verlassen.")
            elif before.channel is not None and after.channel is not None:
                await logch.send(f":mega: **{str(member)} ({str(member.id)} )** hat den Voice Channel von ** "
                                 f"{str(before.channel)} ** zu ** {str(after.channel)}** gewechselt.")
        except Exception:
            pass

    # Linkblocker
    @commands.Cog.listener()
    async def on_message(self, message):
        if not bp.user(message.author):
            return
        await self.update_member(message.author)
        if any([curse in message.content.lower() for curse in bl.blacklist]):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, dieser Server verbietet das Senden von Discord-Links"
                                       )


def setup(client):
    client.add_cog(Moderation(client))
