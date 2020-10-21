from discord.ext import commands
import discord

intents = discord.Intents().all()

class StellarContext(commands.Context):
    @property
    async def owner(self):
        owner = await self.bot.fetch_user(self.bot.owner_id)
        return owner

    @property
    def intents(self):
        final=''
        for i in dict(intents):
            final += f'\n{i} = {dict(intents).get(i)}'
        return final

class StellarColour(discord.Color):
    @classmethod
    def Steller(cls):
        """Returns the Stellar logo colour"""
        return cls(0x7649fe)
