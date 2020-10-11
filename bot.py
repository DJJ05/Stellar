import discord
from discord.ext import commands
from subclasses import PinBoardColour, PinBoardContext, intents

import json
import os
import asyncio
import sys
# import jishaku

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

def parsetoken():
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data['token']

'''class PinBoardJishaku(jishaku.Jishaku, metaclass=jishaku.metacog.GroupCogMeta, command_parent=jishaku.cog.jsk):
    async def cog_check(self, ctx):
        return ctx.author.id == 670564722218762240'''

class Bot(commands.AutoShardedBot):
    def __init__(self, event_loop):
        super().__init__(command_prefix=self.get_prefix, intents=intents, case_insensitive=True, loop=event_loop, description="The modern day alternative to the StarBoard!")
        self.colour = PinBoardColour
        self.color = PinBoardColour

        for filename in os.listdir('cogs'):
            if filename.endswith('.py') and filename != 'secrets.py':
                self.load_extension('cogs.{}'.format(filename[:-3]))
        self.load_extension('jishaku')

    async def get_prefix(self, message: discord.Message) -> str:
        with open('guildconfig.json', 'r') as f:
            prefixes = json.load(f)
        guild_prefix = 	prefixes[str(message.guild.id)]["prefix"]
        return commands.when_mentioned_or(guild_prefix)(self, message)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or PinBoardContext)

    async def on_ready(self) -> None:
        print('\n')
        print(f'Logged in as: {self.user.name}#{self.user.discriminator}')
        print(f'With ID: {self.user.id}\n——————————————————————————————')
        await self.change_presence(activity=discord.Activity(type=5, name="the olympics"))
        print(f'Status changed successfully\n——————————————————————————————')

    def run(self):
        super().run(parsetoken())

def main():
    event_loop = asyncio.get_event_loop()
    bot = Bot(event_loop=event_loop)
    bot.run()
    # bot.add_cog(PinBoardJishaku(bot=bot))

if __name__ == '__main__':
    main()
