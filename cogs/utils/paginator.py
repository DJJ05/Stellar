import discord
from discord.ext import menus


class ShipSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        a = ''.join(f'{v}' for i, v in enumerate(entries, start=offset))
        a = discord.Embed(
            title='Ship Info',
            description=f'{a}',
            colour=0x7649fe
        )
        return a

        '''
        pages = menus.MenuPages(source=MySource(cock), clear_reactions_after=True)
        await pages.start(ctx)
        '''
