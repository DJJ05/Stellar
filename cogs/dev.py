import discord
from discord.ext import commands

from .utils.commons import loadjson, dumpjson


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == 670564722218762240

    @commands.group(invoke_without_command=True)
    async def dev(self, ctx):
        """Developer commands used for manually editing configuration files"""
        await ctx.send_help(ctx.command)

    @dev.command(aliases=['as'])
    async def addstellics(self, ctx, member: discord.Member, amount: int):
        """Manually edits users.json to add Stellics to a user's account. Can be negative"""
        m = ctx.author if not member else member
        us = loadjson('users')
        try:
            u = us[str(m.id)]
        except KeyError:
            raise commands.BadArgument('Member does not have a registered account.')
        u['balance'] += amount
        dumpjson('users', us)
        return await ctx.send(f'Added `{amount}` Stellics to {m}\'s account.')


def setup(bot):
    bot.add_cog(Dev(bot))
