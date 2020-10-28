import collections

import discord
from discord.ext import commands, tasks

from .utils.commons import loadjson, dumpjson
from .utils.dbl import getvotes


class Crates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voters = None
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
        return dumpjson('users', us)


def setup(bot):
    bot.add_cog(Crates(bot))
