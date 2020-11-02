import asyncio
from bot import Bot

event_loop = asyncio.get_event_loop()
bot = Bot(event_loop=event_loop)
bot.run()
