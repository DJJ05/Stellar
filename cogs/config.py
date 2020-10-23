import discord
from discord.ext import commands
import json


class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.message.author.id == 670564722218762240:
            return True
        elif ctx.message.author.permissions_in(channel=ctx.message.channel).manage_messages:
            return True
        else:
            return False


def setup(bot):
    bot.add_cog(config(bot))
