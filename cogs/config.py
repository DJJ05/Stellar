from discord.ext import commands

from .utils.commons import loadjson, dumpjson


class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.message.author.id == 670564722218762240:
            return True
        elif ctx.message.author.permissions_in(channel=ctx.message.channel).manage_guild:
            return True
        else:
            return False

    @commands.group(aliases=['pre'], invoke_without_command=True)
    async def prefix(self, ctx):
        """Prefix configuration commands"""
        gc = loadjson('guildconfig')
        gp = gc[str(ctx.guild.id)]['prefix']
        await ctx.send(f'The prefix for this guild is `{gp}`. Use `{gp}pre change` to change this.')

    @prefix.command(name='change')
    async def prefix_change(self, ctx, newprefix: str = 'st+'):
        gc = loadjson('guildconfig')
        g = gc[str(ctx.guild.id)]
        gp = g['prefix']

        if newprefix == gp:
            return await ctx.send('This is already the guild prefix!')

        if newprefix == 'st+':
            m = 'reset'
        else:
            m = 'changed'

        g['prefix'] = newprefix

        dumpjson('guildconfig', gc)
        return await ctx.send(f'Successfully {m} guild prefix to {newprefix}')


def setup(bot):
    bot.add_cog(Config(bot))
