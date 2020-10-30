import asyncio
import collections
import random

import discord
from discord.ext import commands, tasks

from .utils.checks import check_account
from .utils.commons import loadjson, dumpjson
from .utils.dbl import getvotes


class Crates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voters = None
        self.crates = {
            'voter': 0.1
        }
        self.check_voters.start()

    @tasks.loop(minutes=1.5)
    async def check_voters(self):
        us = loadjson('users')
        r = await getvotes()
        li = []
        for d in r:
            li.append(str(d['id']))
        c = collections.Counter(li)
        if not self.voters:
            self.voters = c
            return
        di = dict(c - self.voters)
        self.voters = c
        if not len(di):
            return
        for u, a in di.items():
            if u not in us:
                continue
            m = await self.bot.fetch_user(u)
            try:
                await m.send(
                    f'Thank you for voting for me! You have recieved {a} voter crates as a reward! Use the `open` command to open them!')
            except discord.Forbidden:
                pass
            try:
                us[str(u)]['crates']['voter'] += a
            except KeyError:
                us[str(u)]['crates']['voter'] = a
        dumpjson('users', us)

    @commands.command()
    async def vote(self, ctx):
        """Vote link and info"""
        e = self.bot.Embed(
            title='Vote for me!',
            description='You can vote for Stellar [here](https://top.gg/bot/758065684218380350/vote), and you will receieve a vote crate. Please wait 1m 30s after voting for a DM to come through.'
        )
        return await ctx.send(embed=e)

    @commands.command()
    @check_account()
    async def open(self, ctx, cratename: str, quantity: int = 1):
        """Open a specified crate type in a specified quanity. Defaults to one."""
        c = cratename.lower()
        u = loadjson('users')
        cr = u[str(ctx.author.id)]['crates']
        if not len(cr):
            return await ctx.send(f'You do not own any crates! You can get voter crates using `{ctx.prefix}vote`.')
        if not cr.get(c) or cr.get(c) == 0:
            return await ctx.send(
                f'Specified crate not located in your account! Make sure you own it with `{ctx.prefix}inv`.')
        p = self.crates.get(c)
        if not p:
            return await ctx.send(
                'This crate does not have a set price at this point. It will remain in your account until the market settles or the price fluctuates to a stable amount.')
        if u[str(ctx.author.id)]['balance'] == 0:
            return await ctx.send(
                f'You do not have any money, and so this crate will earn you nothing. It has been sent back to your account for the time being, use `{ctx.prefix}scavenge` to search for Stellics.')
        be = u[str(ctx.author.id)]['balance']
        ps = []
        if quantity > u[str(ctx.author.id)]['crates'][cratename]:
            return await ctx.send('You do not have that many crates!')
        for i in range(quantity):
            p = random.uniform(p, 0.2)
            ps.append(p)
        for p in ps:
            b = u[str(ctx.author.id)]['balance']
            a = b * p
            nb = b + a + 50
            u[str(ctx.author.id)]['balance'] = round(nb)
        u[str(ctx.author.id)]['crates'][cratename] -= quantity
        dumpjson('users', u)
        e = self.bot.Embed()
        e.set_image(
            url='https://cdnb.artstation.com/p/assets/images/images/013/242/325/original/andre-evangelista-bau.gif?1538699058')
        m = await ctx.send(embed=e)
        await asyncio.sleep(3)
        await m.edit(embed=None,
                     content=f'Congrats! You got **{u[str(ctx.author.id)]["balance"] - be}** Stellics from **{quantity}** crates!')


def setup(bot):
    bot.add_cog(Crates(bot))
