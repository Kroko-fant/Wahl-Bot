import json
from ast import Pass

from discord.ext import commands

from botdata import botparameters as bp


class Themen(commands.Cog):

    def _init_(self, client):
        self.client = client

    # kategorie setzen
    @commands.command()
    async def category(self, ctx, category):
        guild = ctx.guild
        with open('./data/topiccategorys.json', 'r') as f:
            categorys = json.load(f)

        categorys[str(guild.id)] = str(category)

        with open('./data/topiccategorys.json', 'w') as f:
            json.dump(categorys, f, indent=4)

    # thema erstellen channel setzen
    @commands.command()
    async def topiccreate(self, ctx, newtopicchannel):
        guild = ctx.guild
        with open('./data/newtopicchannel.json', 'r') as f:
            topiccreate = json.load(f)

        topiccreate[str(guild.id)] = str(newtopicchannel)

        with open('./data/newtopicchannel.json', 'w') as f:
            json.dump(topiccreate, f, indent=4)

    # wenn message im Topic Channel
    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild
        with open('./data/newtopicchannel.json', 'r') as f:
            topiccreate = json.load(f)
            if topiccreate[str(guild.id)] == str(message.channel.id):
                # neuer channel erstellen
                with open('./data/topiccategorys.json', 'r') as f:
                    categorys = json.load(f)
                categoryy = message.channel.category.id
                titel = message.content
                print(categoryy)
                print(message.channel.category)
                reasonfc = "Neuer Channel von User " + str(message.author)
                if str(message.channel.category.id) == str(categoryy):
                    await guild.create_text_channel(titel, category=message.channel.category, position=0, topic=titel,
                                                    reason=reasonfc)
                    await bp.delete_cmd(message)
            else:
                Pass


def setup(client):
    client.add_cog(Themen(client))