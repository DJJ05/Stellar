import discord
from discord.ext import commands
from .utils import checks, embedder

import json

embedder = embedder.client()

class configCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.message.author.id == 670564722218762240:
            return True
        elif ctx.message.author.permissions_in(channel=ctx.message.channel).manage_messages:
            return True
        else:
            return False

    @commands.group(invoke_without_command=True)
    async def config(self, ctx):
        """Configuration command grouping. All config commands require manage message permissions."""

        with open('guildconfig.json', 'r') as f:
            guildconfig = json.load(f)
        guildconfig = guildconfig[str(ctx.guild.id)]

        desc = f'**Trigger Emotes:**\n{" ".join([i for i in guildconfig["emotes"]])}\n\n**Reaction Threshold:**\n{guildconfig["threshold"]}\n\n**Channel Redirects:**\n{[i for i in guildconfig["redirects"]] or "None"}\n\n**Pin Alerts:**\n{guildconfig["pinalerts"]}'

        await ctx.send(embed=embedder.thumbembedder(
            thumb=ctx.guild.icon_url,
            title=f'Current guild configuration for: {ctx.guild.name}',
            desc=desc,
            colour=self.bot.colour.PinBoard()
        ))

def setup(bot):
    bot.add_cog(configCog(bot))
