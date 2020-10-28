import collections

from discord.ext import commands, tasks

from .utils.commons import loadjson
from .utils.dbl import getvotes


class Crates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voters = None
        '''self.check_voters.start()'''

    '''@tasks.loop(minutes=1.5)
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
'''

def setup(bot):
    bot.add_cog(Crates(bot))
