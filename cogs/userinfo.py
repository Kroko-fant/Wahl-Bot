import discord
from discord.ext import commands


class Userinfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member):
        roles = [role for role in member.roles]

        embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

        embed.set_author(name=f'Információk róla: {member}')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'{ctx.author} kérésére', icon_url=ctx.author.avatar_url)

        embed.add_field(name='ID:', value=str(member.id))
        embed.add_field(name='Name:', value=str(member.display_name))

        embed.add_field(name='Status:', value=str(member.status))
        embed.add_field(name='Aktivität:', value=str(member.activity.name))

        embed.add_field(name='Account erstellt:', value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        embed.add_field(name='Beigetreten:', value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

        embed.add_field(name=f'Role-ok ({len(roles)})', value='  '.join([role.mention for role in roles]))
        embed.add_field(name='Hauptrolle:', value=str(member.top_role.mention))

        embed.add_field(name='Bot?', value=str(member.bot))

        await ctx.send(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):  # ez itt hibás még
            embed = discord.Embed(title="Hiba", description="Kérlek add meg a megfigyelendő tagot is.", color=0xff0000)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Userinfo(bot))
