import asyncio
import time

import discord
from discord.ext import commands


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=0x7649fe)
            await destination.send(embed=emby)


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    @commands.command(aliases=['latency'])
    async def ping(self, ctx):
        """Displays shard latency and command response time"""
        begin = time.perf_counter()
        shard = self.bot.get_shard(ctx.guild.shard_id)
        if not shard:
            return
        embed = self.bot.Embed(
            description=f'```prolog\nShard Heartbeat: {round(shard.latency * 1000)}ms\n```')
        pong = await ctx.send(embed=embed)
        end = time.perf_counter()
        response = round((end - begin) * 1000)
        embed = self.bot.Embed(
            description=f'```prolog\nShard Heartbeat: {round(shard.latency * 1000)}ms\nCommand Response: {response}ms'
                        f'\n```')
        await asyncio.sleep(0.5)
        await pong.edit(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        """Bot invite and server link, with multiple permission stages"""
        admin = 'https://discord.com/oauth2/authorize?client_id=758065684218380350&scope=bot&permissions=8'
        required = 'https://discord.com/oauth2/authorize?client_id=758065684218380350&scope=bot&permissions=67456065'
        none = 'https://discord.com/oauth2/authorize?client_id=758065684218380350&scope=bot&permissions=0'
        embed = self.bot.Embed(
            title='Invite Links:',
            description=f'__**Bot Invite Links**__\n[__Admin__]({admin})\n[__Required__]({required})\n'
                        f'[__None__]({none})\n\n__**Join The Bot Server!**__\n'
                        f'[__Click Me__](https://discord.gg/ybZ9ZYg) '
        )
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
