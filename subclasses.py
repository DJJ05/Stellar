from discord.ext import commands
import discord
import colorsys

intents = discord.Intents().all()

class PinBoardContext(commands.Context):
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

class PinBoardColour(discord.Color):
    @classmethod
    def PinBoard(cls):
        """Returns the PinBoard logo colour"""
        return cls(0xDC0724)
