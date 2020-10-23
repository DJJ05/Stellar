import discord
from discord.ext import menus


class MySource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        a = ''.join(f'{v}' for i, v in enumerate(entries, start=offset))
        a = a.replace('`', '\`')
        a = discord.Embed(
            description=f'```\n{a}\n```'
        )
        return a

        '''
        pages = menus.MenuPages(source=paginator.MySource(cock), clear_reactions_after=True)
        await pages.start(ctx)
        '''
