import discord
from discord.ext import commands

import json
from .utils import embedder

embedder = embedder.client()

class eventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        with open('guildconfig.json', 'r') as f:
            guildconfig = json.load(f)

        guildconfig[str(guild.id)] = {
            "emotes": [':pushpin:'],
            "threshold": 10,
            "redirects": [],
            "pinalerts": True,
            "prefix": "pb+"
        }

        with open('guildconfig.json', 'w') as f:
            json.dump(guildconfig, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        with open('guildconfig.json', 'w') as f:
            guildconfig = json.load(f)

        guildconfig.pop(str(guild.id))
        
        with open('guildconfig.json', 'r') as f:
            json.dump(guildconfig, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not len(message.mentions):
            return
        if message.content in ('<@758065684218380350>', '<@!758065684218380350>') and not message.author.bot:
            with open('guildconfig.json', 'r') as f:
                prefixes = json.load(f)
            await message.channel.send(embed=embedder.thumbembedder(title=f'{message.guild.me.name} » {message.guild.me.id}', colour=self.bot.colour.PinBoard(), desc=f'`My prefix for {message.guild.name} is {prefixes[str(message.guild.id)]["prefix"]}.`\n`Use {prefixes[str(message.guild.id)]["prefix"]}help to view my command list.`', thumb=message.guild.me.avatar_url))

def setup(bot):
    bot.add_cog(eventsCog(bot))
