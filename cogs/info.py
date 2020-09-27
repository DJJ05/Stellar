import discord
from discord.ext import commands

from .utils import embedder

embedder = embedder.client()

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=0xDC0724)
            await destination.send(embed=emby)

class infoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command(aliases=['invite'])
    async def inv(self, ctx):
        """Bot invite link, with multiple permission stages"""
        admin = discord.utils.oauth_url(758065684218380350, permissions=discord.Permissions(permissions=8))
        required = discord.utils.oauth_url(758065684218380350, permissions=discord.Permissions(permissions=67456065))
        none = discord.utils.oauth_url(758065684218380350, permissions=discord.Permissions(permissions=0))
        await ctx.send(embed=embedder.simpleembedder(title='Permission Classes:', colour=self.bot.colour.PinBoard(), desc=f':closed_lock_with_key: [`Admininstrator`]({admin})\n:closed_lock_with_key: [`Required`]({required})\n:closed_lock_with_key: [`None`]({none})'))

def setup(bot):
    bot.add_cog(infoCog(bot))
