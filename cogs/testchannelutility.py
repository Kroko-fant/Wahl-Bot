import json

import discord
from discord.ext import commands
from discord.ext import tasks

from botdata import botparameters as bp


class ChannelUtility(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open("./data/channel/archives.json", "r") as f:
            self.archives = json.load(f)
        with open('./data/channel/newtopicchannel.json', 'r') as f:
            self.topiccreate = json.load(f)
        with open('./data/channel/topiccategorys.json', 'r') as f:
            self.categorys = json.load(f)
        with open('./data/channel/addreactchannel.json', 'r') as f:
            self.addreactchannel = json.load(f)
        self.archiver.start()

    def cog_unload(self):
        self.archiver.cancel()

    @tasks.loop(hours=6)
    async def archiver(self):
        # TODO
        # Kategorie finden
        for channel in:  # loopen

    # channel überprüfen
    # archivieren
    # abschließen

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setarchiv(self, ctx, archiv):
        """Setze eine Archivkategorie"""
        self.archives[str[ctx.guild.id]] = str(archiv)
        with open("./data/channel/archives.json", "w") as f:
            json.dump(self.archives, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send(f'Kategorie {archiv} wurde erfolgreich als Archiv gesetzt')

    # kategorie setzen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcategory(self, ctx, category):
        """"Setze eine Kategorie, in der neue Themen erstellt werden."""
        self.categorys[str(ctx.guild.id)] = str(category)
        with open('./data/channel/topiccategorys.json', 'w') as f:
            json.dump(self.categorys, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send(f"Kategorie {category} ist jetzt die Kategorie für neue Themen.", delete_after=bp.deltime)

    # thema erstellen channel setzen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settopiccreate(self, ctx, newtopicchannel):
        """Setze einen Kanal, in welchem neue Themen erstellt werden."""
        self.topiccreate[str(ctx.guild.id)] = str(newtopicchannel)
        with open('./data/channel/newtopicchannel.json', 'w') as f:
            json.dump(self.topiccreate, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send(f"Channel <#{newtopicchannel}> ist jetzt der Channel für die Themenerstellung.",
                       delete_after=bp.deltime)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setaddreactchannel(self, ctx, addreactchannelarg, *emojis):
        """Setze einen Kanal, in welchem immer mit einer Liste von Emojis
        Benutzung: !setaddreactchannel <channel> <emoji-liste>"""
        # emojis checken
        if emojis[0].lower() == "clear":
            self.addreactchannel.pop(addreactchannelarg, None)
            with open('./data/channel/addreactchannel.json', 'w') as f:
                json.dump(self.addreactchannel, f, indent=4)
            await ctx.send(f'Emojis für Channel <#{addreactchannelarg}> entfernt.')
        else:
            self.addreactchannel[addreactchannelarg] = emojis
            with open('./data/channel/addreactchannel.json', 'w') as f:
                json.dump(self.addreactchannel, f, indent=4)
            await bp.delete_cmd(ctx)
            await ctx.send(f"Channel <#{addreactchannelarg}> ist jetzt der Channel für das hinzufügen von Reaktionen."
                           f"Folgende Reaktionen wurden hinzugefügt: {emojis}",
                           delete_after=bp.deltime)

    # wenn message im Topic Channel
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild is None or not bp.user(ctx.author):
            if not bp.user:
                await bp.delete_cmd(ctx)
                errorct02embed = discord.Embed(title="Error #CT02",
                                               description="Nachrichten anderer Bots sind hier nichte erlaubt bitte "
                                                           "führe hier keine Befehle aus!", color=0xff0000)
                await ctx.channel.send(embed=errorct02embed, delete_after=bp.deltime)
            return
        if str(ctx.channel.id) in self.addreact:
            for emoji in self.addreact[str(ctx.channel.id)]:
                await ctx.add_reaction(emoji)
        if not self.topiccreate[str(ctx.guild.id)] == str(ctx.channel.id):
            return

        if len(str(ctx.content)) <= 100:
            # if str(ctx.content).isalnum():
            try:
                # neuer channel erstellen
                if str(ctx.channel.category.id) == str(self.categorys[str(ctx.guild.id)]):
                    await bp.delete_cmd(ctx)
                    # TODO Channel first NAchricht
                    await ctx.guild.create_text_channel(
                        ctx.content, category=ctx.channel.category, position=0,
                        topic=ctx.content, reason=f"Neuer Channel von User {str(ctx.author)}")
                    createdchannel01embed = discord.Embed(
                        title="Erfolgreich erstellt", description="Channel erfolgreich erstellt. Bitte füge eine "
                                                                  "Themenbeschreibung in deinen Kanal ein",
                        color=0xff0000)
                    await ctx.channel.send(embed=createdchannel01embed, delete_after=bp.deltime)
            except KeyError:  # Konnte Kategorie nicht finden
                await bp.delete_cmd(ctx)
                errorct03embed = discord.Embed(
                    title="Error #CT03", description="Konnte keine Kategorie für ein neues Thema finden. Bitte "
                                                     "kontaktiere einen Admin und bitte ihn eine Kategorie mit "
                                                     "setcategory zu setzen.", color=0xff0000)
                await ctx.channel.send(embed=errorct03embed, delete_after=bp.deltime)
        # else:
        #     errorct04embed = discord.Embed(title="Error #CT04",
        #                                    description="Der Kanalname muss alphanumerisch sein! Bitte"
        #                                                " verwende keine Commands in diesem Kanal",
        #                                    color=0xff0000)
        #     await ctx.channel.send(embed=errorct04embed, delete_after=bp.deltime)
        else:  # Nachrichten-LÃ¤nge
            await bp.delete_cmd(ctx)
            errorct01embed = discord.Embed(
                title="Error #CT01", description="Zu Langer Titel! Dein Titel beim Thema erstellen ist zu lang! "
                                                 "(>100 Zeichen)", color=0xff0000)
            await ctx.channel.send(embed=errorct01embed, delete_after=bp.deltime)


def setup(client):
    client.add_cog(ChannelUtility(client))
