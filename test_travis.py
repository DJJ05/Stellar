from bot import Bot
import asyncio

def test():
    event_loop = asyncio.get_event_loop()
    assert event_loop, 'Failed to fetch event loop'
    bot = Bot(event_loop=event_loop)
    assert bot, 'Failed to created bot instance'
    colour = bot.color
    assert colour, 'Failed to fetch bot variable(s)'