import json
import time

import discord
from discord.ext import commands

from botdata import blacklist as bl
from botdata import botparameters as bp


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.feedbackchannel = 643540415919816717
        self.bugchannel = 643546804750909454
        self.dmchannel = 635544300834258995
        with open('./data/channel/logchannel.json', 'r') as f:
            self.logs = json.load(f)
        with open('./data/prefixes.json', 'r') as f:
            self.prefixes = json.load(f)

    # async def delete_member_from_purge(self, member):
    # TODO: Mitglieder wieder aus purge löschen
    # print("Unfinished")

    async def update_member(self, member):
        # TODO
        with open(f'./data/servers/{member.guild.id}/lastdata.json', 'r') as f:
            members = json.load(f)
        members[str(member.id)] = int(round(time.time() / 8640, 0))
        with open(f'./data/servers/{member.guild.id}/lastdata.json', 'w') as f:
            json.dump(members, f, indent=4)

    @commands.command()
    async def verify(self, ctx):
        """Verifiziere deinen Account im Bot.
        Hat ansonsten keine weiteren Funktionen bisher."""
        await bp.delete_cmd(ctx)
        if await bp.unverifiziert(ctx):
            # USERID in Verify
            verifydir = f'./data/servers/{ctx.guild.id}/verified.json'
            with open(verifydir, 'r') as f:
                verified = json.load(f)

            verified[str(ctx.author.id)] = True

            with open(verifydir, 'w') as f:
                json.dump(verified, f, indent=4)
            await ctx.send('Verifiziert')
            await ctx.author.add_roles(verified[str(ctx.guild.id)], reason="Verify", atomic=True)
        elif await bp.verifiziert(ctx):
            await ctx.send("Du bist bereits verifiziert!")
        else:
            await ctx.send("Du konntest nicht verifiziert werden! Wende dich an das Team oder versuche es nochmal!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        """Löscht den gewählten Amount an Nachrichten Standardmenge: 10"""
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Es wurden **{amount}** Nachrichten gelöscht.", delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Kick-Befehl wurde benutzt"):
        """Kickt den User vom Server Syntax: {prefix}kick <@user>"""
        await bp.delete_cmd(ctx)
        await member.kick(reason=reason)
        await ctx.send(f"User **{member}** wurde gekickt.", delete_after=bp.deltime)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorcm01embed = discord.Embed(title="Error #CM01", color=0xff0000,
                                           description="Fehlende NutzerID! Syntax: kick <userid> oder kick @<user>")
            await ctx.send(embed=errorcm01embed, delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Ban den User vom Server Syntax: {prefix}ban <@user>"""
        await bp.delete_cmd(ctx)
        await member.ban(reason=reason)
        await ctx.send(f"User **{member}** wurde gebannt.", delete_after=bp.deltime)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            errorcm02embed = discord.Embed(title="Error #CM02", color=0xff0000,
                                           description="Fehlende NutzerID! Syntax: ban <userid> oder ban @<user>")
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
            await ctx.send(f"Es wurden **{len(bans)}** User zum Entbannen gefunden. Gebe Okay zum Entbannen ein.",
                           delete_after=bp.deltime)
            await self.client.wait_for('message', check=lambda message: message.content.lower() == "okay", timeout=60)
            await ctx.send(
                f"Starte Unban.\n Dies kann etwas dauern.\n Geschätzte Zeit: **{round(len(bans) / 6.5)}** Sekunden")
            start = time.time()
            for ban in bans:
                await ctx.guild.unban(ban[1], reason="Unbanall")
            ende = time.time()
            await ctx.send(f"Alle User erfolgreich entbannt. :white_check_mark:\nUserzahl: **{len(bans)}**\nZeit: **"
                           f"{'{:5.3f}'.format(ende - start)}**\nBans/Sekunde: **{round(len(bans) / (ende - start))}**")
        else:
            await ctx.send(f'Es wurden 0 User zum Entbannen gefunden.')

    # LogChannel setzen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlogchannel(self, ctx, lchannelid=None):
        """Setze einen Logkanal Zum Setzen des Channels wird die Channelid als Argument benötigt.
        Syntax: !setlogchannel <channelid>"""
        if not lchannelid.isnumeric():
            await ctx.send("Channelid ungültig!")
            return
        if self.client.get_channel(lchannelid) is None:
            await ctx.send("Channelid ungültig!")
            return
        self.logs[str(ctx.guild.id)] = int(lchannelid)
        with open('./data/channel/logchannel.json', 'w') as f:
            json.dump(self.logs, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send(f"Channel <#{lchannelid}> ist jetzt der Channel für den Log.", delete_after=bp.deltime)

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx, ch, *, text):
        try:
            await self.client.get_channel(int(ch)).send(text)
            await ctx.message.add_reaction(self.client.get_emoji(634870836255391754))
        except Exception:
            await ctx.message.add_reaction("⚠")

    # Memberjoin
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not bp.user(member):
            return
        await self.update_member(member)
        try:
            logch = self.client.get_channel(self.logs[str(member.guild.id)])
            await logch.send(f":inbox_tray: **{member} ({member.id})** ist dem Sever beigetreten.")
        except Exception:
            pass

    # Memberleave
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not bp.user(member):
            return
        try:
            logch = self.client.get_channel(self.logs[str(member.guild.id)])
            await logch.send(f":outbox_tray: **{member} ({member.id})** hat den Server verlassen.")
        except Exception:
            pass

    # Member wird gebannt
    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        try:
            if bp.user(member):
                logch = self.client.get_channel(self.logs[str(member.guild.id)])
                await logch.send(f":no_entry_sign: **{member} ({member.id})** wurde gebannt.")
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
            logch = self.client.get_channel(self.logs[str(guild.id)])
            await logch.send(f":white_check_mark: **{member} ({member.id})** wurde entgebannt.")
        except Exception:
            pass

    # Nachricht löschen
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.guild_id is None or payload is None or payload.cached_message is None \
                or str(payload.guild_id) not in self.logs.keys():
            return
        logch = self.client.get_channel(self.logs[str(payload.cached_message.author.guild.id)])
        if len(payload.cached_message.content) > 1800:
            await logch.send(':recycle: **Nachricht:**|')
            await logch.send(payload.cached_message.content)
            await logch.send(f'|von User: {payload.cached_message.author} ({payload.cached_message.author.id}'
                             f') in Channel: {payload.channel_id} gelöscht.')
        else:
            await logch.send(f':recycle: **Nachricht: **{payload.cached_message.content} von User: '
                             f'{payload.cached_message.author} ({payload.cached_message.author.id}) in Channel: '
                             f'{payload.channel_id} gelöscht.')

    # Voice-Änderungen
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not bp.user(member) and member.guild is not None:
            return

        await self.update_member(member)
        logch = self.client.get_channel(self.logs[str(member.guild.id)])
        if before.channel is None:
            await logch.send(f":mega: **{member} ({member.id})** hat den Voice Channel **{before.channel}** verlassen.")
        elif before.channel is not None and after.channel is None:
            await logch.send(f":mega: **{member} ({member.id})** hat den Voice Channel **{before.channel}** verlassen.")
        elif before.channel is not None and after.channel is not None:
            await logch.send(f":mega: **{member} ({member.id} )** hat den Voice Channel von ** "
                             f"{before.channel} ** zu ** {after.channel}** gewechselt.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def newprefix(self, ctx, prefix='!'):
        """Weist einen neuen Prefix zu.
        Syntax: {prefix} newprefix <prefix>
        Wird kein Prefix angegeben wird ! gesetzt."""
        await bp.delete_cmd(ctx)
        self.prefixes[str(ctx.guild.id)] = prefix
        with open('./data/prefixes.json', 'w') as f:
            json.dump(self.prefixes, f, indent=4)
        await ctx.send(f'Prefix zu:** {prefix} **geändert', delete_after=bp.deltime)

    # ErrorHandler
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error, force=False):
        # Skippen, wenn wir einen lokalen Handler haben
        if hasattr(ctx.command, 'on_error') and not force:
            return
        error = getattr(error, 'original', error)

        # Missing Permissions
        if isinstance(error, (commands.errors.MissingPermissions, commands.errors.NotOwner)):
            await ctx.send("Dazu fehlen dir die Permissions :P")
        # Fehlendes erwartetes Argument
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("Fehlendes Argument! gucke dir doch !help <command> an")
        elif isinstance(error, commands.errors.CommandNotFound):
            if ctx.message.content[1:].startswith("bump") or ctx.message.content[1:].isnumeric() or \
                    ctx.message.content[1:].startswith("d bump") or ctx.message.content[1:].startswith("disboard"):
                return
            await ctx.send("Diesen Befehl gibt es nicht :(")
        # DiscordErrors
        elif isinstance(error, commands.CommandError):
            await ctx.send(f"Irgendwas funktioniert da nicht ganz...{error} {type(error)} "
                           f"<@!137291894953607168>")
        # Sonstige Errors
        else:
            await ctx.send(f"Ein unerwarteter Fehler ist aufgetreten!... \n {error} "
                           f"{type(error)} <@!137291894953607168>")

    # Linkblocker
    @commands.Cog.listener()
    async def on_message(self, message):
        if not bp.user(message.author) or message.guild is None:
            return
        # DMs empfangen
        if message.guild is None and bp.user(message.author):
            channel = self.client.get_channel(int(635544300834258995))
            content = f'**{message.author}** sagt: "{message.content}"'
            if len(message.content) < 1800:
                await channel.send(content)
            else:
                await channel.send(content[0:1800])
                await channel.send(content[1801])
            return
        # DMs senden
        if (message.channel.id == self.bugchannel or message.channel.id == self.feedbackchannel
            or message.channel.id == self.dmchannel) and message.content[0:18].isnumeric():
            await message.add_reaction("✅")
            dmchannel = self.client.get_user(int(message.content[0:18]))
            if dmchannel.dm_channel is None:
                await dmchannel.create_dm()
            await dmchannel.dm_channel.send(message.content[19:])
            return
        await self.update_member(message.author)
        if "prefix" in message.content.lower() and bp.user(message.author) and "bot" in message.content.lower():
            await message.channel.send(f"Dieser Server hat den Prefix: **{self.prefixes[str(message.guild.id)]}**")
        if any([curse in message.content.lower() for curse in bl.blacklist]):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, dieser Server verbietet das Senden von "
                                       f"Discord-Links")


def setup(client):
    client.add_cog(Moderation(client))
