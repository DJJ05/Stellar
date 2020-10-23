from discord.ext import commands


def admin_or_owner():
    def predicate(ctx):
        if ctx.message.author.id == 670564722218762240:
            return True
        elif ctx.message.author.permissions_in(channel=ctx.message.channel).administrator:
            return True
        else:
            return False

    return commands.check(predicate)


def manage_messages_or_owner():
    def predicate(ctx):
        if ctx.message.author.id == 670564722218762240:
            return True
        elif ctx.message.author.permissions_in(channel=ctx.message.channel).manage_messages:
            return True
        else:
            return False

    return commands.check(predicate)
