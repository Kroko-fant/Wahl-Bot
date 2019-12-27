import json

import discord
from discord.ext import commands

from botdata import botparameters as bp


class Themen(commands.Cog):

    def __init__(self, client):
        self.client = client

    # kategorie setzen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcategory(self, ctx, category):
        """"Setze eine Kategorie, in der neue Themen erstellt werden."""
        with open('./data/topiccategorys.json', 'r') as f:
            categorys = json.load(f)

        categorys[str(ctx.guild.id)] = str(category)

        with open('./data/topiccategorys.json', 'w') as f:
            json.dump(categorys, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send(f"Kategorie {category} ist jetzt die Kategorie für neue Themen.", delete_after=bp.deltime)

    # thema erstellen channel setzen
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def settopiccreate(self, ctx, newtopicchannel):
        """Setze einen Kanal, in welchem neue Themen erstellt werden."""
        with open('./data/newtopicchannel.json', 'r') as f:
            topiccreate = json.load(f)

        topiccreate[str(ctx.guild.id)] = str(newtopicchannel)

        with open('./data/newtopicchannel.json', 'w') as f:
            json.dump(topiccreate, f, indent=4)
        await bp.delete_cmd(ctx)
        await ctx.send(f"Channel <#{newtopicchannel}> ist jetzt der Channel für die Themenerstellung.",
                       delete_after=bp.deltime)

    # wenn message im Topic Channel
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            with open('./data/newtopicchannel.json', 'r') as f:
                topiccreate = json.load(f)
            try:
                if topiccreate[str(message.guild.id)] == str(message.channel.id):
                    if bp.user(message.author):
                        if len(str(message.content)) <= 100:
                            # if str(message.content).isalnum():
                            try:
                                # neuer channel erstellen
                                with open('./data/topiccategorys.json', 'r') as f:
                                    categorys = json.load(f)

                                if str(message.channel.category.id) == str(categorys[str(message.guild.id)]):
                                    await bp.delete_cmd(message)
                                    await message.guild.create_text_channel(
                                        message.content, category=message.channel.category, position=0,
                                        topic=message.content, reason=f"Neuer Channel von User {str(message.author)}")
                                    createdchannel01embed = discord.Embed(
                                        title="Erfolgreich erstellt",
                                        description="Channel erfolgreich erstellt. Bitte füge eine Themenbeschreibung "
                                                    "in deinen Kanal ein", color=0xff0000)
                                    await message.channel.send(embed=createdchannel01embed, delete_after=bp.deltime)
                            except KeyError:  # Konnte Kategorie nicht finden
                                await bp.delete_cmd(message)
                                errorct03embed = discord.Embed(
                                    title="Error #CT03",
                                    description="Konnte keine Kategorie für ein neues Thema finden. Bitte kontaktiere "
                                                "einen Admin und bitte ihn eine Kategorie mit setcategory zu setzen.",
                                    color=0xff0000)
                                await message.channel.send(embed=errorct03embed, delete_after=bp.deltime)

                        # else:
                        #     errorct04embed = discord.Embed(title="Error #CT04",
                        #                                    description="Der Kanalname muss alphanumerisch sein! Bitte"
                        #                                                " verwende keine Commands in diesem Kanal",
                        #                                    color=0xff0000)
                        #     await message.channel.send(embed=errorct04embed, delete_after=bp.deltime)

                        else:  # Nachrichten-Länge
                            await bp.delete_cmd(message)
                            errorct01embed = discord.Embed(
                                title="Error #CT01",
                                description="Zu Langer Titel! Dein Titel beim Thema erstellen ist zu lang! "
                                            "(>100 Zeichen)", color=0xff0000)
                            await message.channel.send(embed=errorct01embed, delete_after=bp.deltime)
                    elif bp.ultimatebotid:
                        pass
                    else:
                        await bp.delete_cmd(message)
                        errorct02embed = discord.Embed(
                            title="Error #CT02", description="Nachrichten anderer Bots sind hier nichte erlaubt bitte "
                                                             "führe hier keine Befehle aus!", color=0xff0000)
                        await message.channel.send(embed=errorct02embed, delete_after=bp.deltime)
                else:  # nicht im Channel
                    pass
            except KeyError:
                pass
        else:
            pass


def setup(client):
    client.add_cog(Themen(client))
