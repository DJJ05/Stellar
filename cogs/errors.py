import discord
from discord.ext import commands
import traceback
import sys


'''
Error Handler taken from eevie's gist, go check it out!
https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
'''


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(ctx.channel, discord.DMChannel):
            return

        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled by my owner. Please check back later.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} cannot be used in Private Messages. Please use it in your guild.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            await ctx.send('\n'.join(error.args))

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('\n'.join(error.args))

        elif isinstance(error, commands.CheckFailure):
            if 'The check functions for command' in error.args[0]:
                return
            await ctx.send('\n'.join(error.args))

        elif isinstance(error, discord.Forbidden):
            await ctx.send('\n'.join(error.args))

        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

            errchannel = self.bot.get_channel(748962623487344753)

            etype = type(error)
            trace = error.__traceback__
            verbosity = 2
            lines = traceback.format_exception(etype, error, trace, verbosity)
            traceback_text = f'```py\n{"".join(lines)}\n```'.replace(
                'rajsharma', 'dev').replace('pinboard', 'stellar')

            embed = discord.Embed(colour=self.bot.colour.Stellar(), title=f'Error during `{ctx.command.qualified_name}`',
                                  description=f'ID: {ctx.message.id}\n[Jump]({ctx.message.jump_url})\n{traceback_text}')

            await errchannel.send(embed=embed)
            lines = traceback.format_exception(etype, error, trace, 1)
            traceback_text = f'```py\n{"".join(lines)}\n```'.replace(
                'rajsharma', 'dev').replace('pinboard', 'stellar')
            embed.description = f'ID: {ctx.message.id}\n[Jump]({ctx.message.jump_url})\n{traceback_text}'
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
