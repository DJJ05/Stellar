import discord
from discord.ext import commands

import traceback
from .utils import embedder

embedder = embedder.client()

skip = [
    commands.TooManyArguments,
    commands.CommandNotFound,
]

perms = [
    commands.MissingPermissions,
    commands.MissingAnyRole,
    commands.MissingRole,
    commands.BotMissingAnyRole,
    commands.BotMissingPermissions,
    commands.BotMissingRole,
    commands.NotOwner,
    commands.CheckFailure
]

args = [
    commands.ArgumentParsingError,
    commands.BadArgument,
    commands.BadUnionArgument,
    commands.MissingRequiredArgument,
]

cooldown = [
    commands.CommandOnCooldown
]

concurrency = [
    commands.MaxConcurrencyReached
]

disabled = [
    commands.DisabledCommand
]

conversion = [
    commands.ConversionError
]

warning = '\U000026a0'

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        etype = type(error)
        trace = error.__traceback__
        verbosity = 4
        lines = traceback.format_exception(etype, error, trace, verbosity)
        traceback_text = f'```py\n{"".join(lines)}\n```'

        if etype in skip:
            return
        elif etype in perms:
            return await ctx.send(f'{warning} *{ctx.author.name}*, either you or I are missing required permissions or roles to perform this command:\n`{etype}`')
        elif etype in args:
            return await ctx.send(f'{warning} *{ctx.author.name}*, you incorrectly passed, or forgot to pass an argument to me:\n`{etype}`')
        elif etype in cooldown:
            return await ctx.send(f'{warning} *{ctx.author.name}*, you, this command, this channel, or this guild are still on cooldown\n`{etype}`')
        elif etype in concurrency:
            return await ctx.send(f'{warning} *{ctx.author.name}*, this channel or this guild are only allowed to run one instance of this command at a time.\n`{etype}`')
        elif etype in disabled:
            return await ctx.send(f'{warning} *{ctx.author.name}*, this command has been disabled by my owner. Please check back later.\n`{etype}`')
        elif etype in conversion:
            return await ctx.send(f'{warning} *{ctx.author.name}*, the argument(s) provided could not be converted into objects.\n`{etype}`')
        else:
            await ctx.send(f'{warning} *{ctx.author.name}*, an unexpected or untracked error occured. My owner has been notified of the issue:\n`{etype}`')
            logging = self.bot.get_channel(758766461282943007)
            return await logging.send('<@!670564722218762240>', embed=embedder.simpleembedder(title=f'Error on {ctx.command.qualified_name}', colour=self.bot.colour.PinBoard(), desc=f'{traceback_text}\n[`Jump URL`]({ctx.message.jump_url})\n`Author: {ctx.author}`\n`Guild: {ctx.guild.name}`\n`Created at: {ctx.message.created_at.strftime("%A, %B %d %Y at %H:%M:%S GMT")}`'))

def setup(bot):
    bot.add_cog(ErrorHandler(bot))
