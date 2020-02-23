import json

from discord.ext import commands

from botdata import botparameters as bp


class Autoverify(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmainrole(self, ctx, roleid):
        """Setze die Rolle die neue User bekommen"""
        if ctx.guild.get_role(roleid) is not None:
            with open('./data/roles/mainrole.json', 'r') as f:
                roles = json.load(f)

            roles[str(ctx.guild.id)] = int(roleid)

            with open('./data/roles/mainrole.json', 'w') as f:
                json.dump(roles, f, indent=4)
            await bp.delete_cmd(ctx)
            await ctx.send("Main-Rolle gesetzt.", delete_after=bp.deltime)
        else:
            pass  # TODO ERROR

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setspacerone(self, ctx, roleid):
        """Setze die Spacerrolle 1, welche jeder User bekommen soll."""
        if ctx.guild.get_role(roleid) is not None:
            with open('./data/roles/spacerone.json', 'r') as f:
                roles = json.load(f)

            roles[str(ctx.guild.id)] = int(roleid)

            with open('./data/roles/spacerone.json', 'w') as f:
                json.dump(roles, f, indent=4)
            await bp.delete_cmd(ctx)
            await ctx.send("Spacer 1 Rolle gesetzt.", delete_after=bp.deltime)
        else:
            pass  # TODO ERROR

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setspacertwo(self, ctx, roleid):
        """Setze die Spacerrolle 2, welche jeder User bekommen soll."""
        if ctx.guild.get_role(roleid) is not None:
            with open('./data/roles/spacertwo.json', 'r') as f:
                roles = json.load(f)

            roles[str(ctx.guild.id)] = int(roleid)

            with open('./data/roles/spacertwo.json', 'w') as f:
                json.dump(roles, f, indent=4)
            await bp.delete_cmd(ctx)
            await ctx.send("Spacer 2 Rolle gesetzt.", delete_after=bp.deltime)
        else:
            pass  # TODO ERROR

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setspacerthree(self, ctx, roleid):
        """Setze die Spacerrolle 3, welche jeder User bekommen soll."""
        if ctx.guild.get_role(roleid) is not None:
            with open('./data/roles/spacerthree.json', 'r') as f:
                roles = json.load(f)

            roles[str(ctx.guild.id)] = int(roleid)

            with open('./data/roles/spacerthree.json', 'w') as f:
                json.dump(roles, f, indent=4)
            await bp.delete_cmd(ctx)
            await ctx.send("Spacer 3 Rolle gesetzt.", delete_after=bp.deltime)
        else:
            pass  # TODO ERROR

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            try:
                guild = message.guild
                member = message.guild.get_member(int(message.author.id))
                # Main Rolle setzen
                with open('./data/roles/mainrole.json', 'r') as f:
                    roles = json.load(f)
                roleid = (roles[str(guild.id)])
                role = guild.get_role(roleid)
                await member.add_roles(role, reason="verify")
                # Spacer 1 Setzen
                with open('./data/roles/spacerone.json', 'r') as f:
                    roles = json.load(f)
                roleid = (roles[str(guild.id)])
                role = guild.get_role(roleid)
                await member.add_roles(role, reason="verify")
                # Spacer 2 Setzen
                with open('./data/roles/spacertwo.json', 'r') as f:
                    roles = json.load(f)
                roleid = (roles[str(guild.id)])
                role = guild.get_role(roleid)
                await member.add_roles(role, reason="verify")
                # Spacer 3 setzen
                with open('./data/roles/spacerthree.json', 'r') as f:
                    roles = json.load(f)
                roleid = (roles[str(guild.id)])
                role = guild.get_role(roleid)
                await member.add_roles(role, reason="verify")
            except KeyError:
                pass


def setup(client):
    client.add_cog(Autoverify(client))
