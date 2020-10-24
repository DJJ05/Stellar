import discord
from discord.ext import commands
import json
import asyncio

from discord.ext.commands.core import check
from .utils.templates import NEW_ACC
from .utils.checks import check_account


class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        with open('users.json', 'r') as f:
            users = json.load(f)
        if str(ctx.author.id) in users.keys():
            return await ctx.send(f'You already have an account. Close your existing account using `{ctx.prefix}close`.')
        users[str(ctx.author.id)] = NEW_ACC
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        return await ctx.send('Account successfully created! Enjoy!')

    @commands.command()
    async def close(self, ctx):
        with open('users.json', 'r') as f:
            users = json.load(f)
        if not str(ctx.author.id) in users.keys():
            return await ctx.send(f'You do not have an account. Create your account using `{ctx.prefix}create`.')
        await ctx.send('Are you certain you wish to close your account? Type "yes" to confirm.')

        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("You took too long, and so the request timed out.")
        else:
            if msg.content.lower() == 'yes':
                users.pop(str(ctx.author.id))
                with open('users.json', 'w') as f:
                    json.dump(users, f, indent=4)
                return await ctx.send(f'Alright, I deleted your account for you, feel free to use `{ctx.prefix}create` at any time.')
            return await ctx.send(f'Cancelled.')

    @commands.command(aliases=['balance'])
    @check_account()
    async def bal(self, ctx):
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = users[str(ctx.author.id)]


def setup(bot):
    bot.add_cog(economy(bot))
