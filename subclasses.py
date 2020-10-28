import discord
from discord.ext import commands

intents = discord.Intents().all()


class StellarContext(commands.Context):
    @property
    async def owner(self):
        owner = await self.bot.fetch_user(self.bot.owner_id)
        return owner

    @property
    def intents(self):
        final = ''
        for i in dict(intents):
            final += f'\n{i} = {dict(intents).get(i)}'
        return final


class StellarColour(discord.Color):
    @classmethod
    def Stellar(cls):
        return cls(0x7649fe)


class StellarEmbed(discord.Embed):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('colour', 0x7649fe)
        super().__init__(*args, **kwargs)
