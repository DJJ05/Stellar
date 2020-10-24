import discord
from discord.ext import commands
import json
import asyncio

from discord.ext.commands.core import check
from .utils.templates import NEW_ACC
from .utils.checks import check_account
from discord.ext import menus
from .utils.paginator import ShipSource
from .utils.paginator import PlanetSource


class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        """Creates your Stellar account."""
        with open('users.json', 'r') as f:
            users = json.load(f)
        if str(ctx.author.id) in users.keys():
            return await ctx.send(f'You already have an account. Close your existing account using `{ctx.prefix}close`.')
        users[str(ctx.author.id)] = NEW_ACC
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
        return await ctx.send('Account successfully created! Enjoy!')

    @commands.command()
    @check_account()
    async def close(self, ctx, confirm=None):
        """Closes your stellar account. Use close yes to auto confirm the closure."""
        with open('users.json', 'r') as f:
            users = json.load(f)
        if confirm and confirm.lower() == 'yes':
            users.pop(str(ctx.author.id))
            with open('users.json', 'w') as f:
                json.dump(users, f, indent=4)
            return await ctx.send(f'Alright, I deleted your account for you, feel free to use `{ctx.prefix}create` at any time.')
        await ctx.send('Are you certain you wish to close your account? Type "yes" to confirm.')

        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id
        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("You took too long, and so the request timed out.")
        else:
            if msg.content.lower() == 'yes':
                users.pop(str(ctx.author.id))
                with open('users.json', 'w') as f:
                    json.dump(users, f, indent=4)
                return await ctx.send(f'Alright, I deleted your account for you, feel free to use `{ctx.prefix}create` at any time.')
            return await ctx.send(f'Cancelled.')

    @commands.command(aliases=['balance'])
    @check_account()
    async def bal(self, ctx):
        """Displays your balance in Stellics."""
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = users[str(ctx.author.id)]
        embed = discord.Embed(
            title=f'{ctx.author.display_name}\'s balance',
            colour=self.bot.colour.Stellar()
        )
        embed.add_field(name='Stellics', value=user['balance'])
        return await ctx.send(embed=embed)

    @commands.command()
    @check_account()
    async def ships(self, ctx):
        """Displays all your ships, and their stats"""
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = users[str(ctx.author.id)]
        ships = []
        for i in user['ships']:
            name = i
            i = user['ships'].get(i)
            desc = i['description']
            peak = str(i['max']) + ' Stellics'
            upgradecost = str(i['upgradecost']) + ' Stellics'
            cooldown = str(i['cooldown']) + ' seconds'
            level = str(i['level'])
            constructed = f'__**`{name}`**__\n**Level: **{level}\n**Description: **{desc}\n**Max Scavage: **{peak}\n**Upgrade Cost: **{upgradecost}\n**Cooldown: **{cooldown}'
            ships.append(constructed)
        pages = menus.MenuPages(source=ShipSource(
            ships), delete_message_after=True)
        await pages.start(ctx)

    @commands.command(aliases=['si'])
    @check_account()
    async def shipinfo(self, ctx, shipname: str):
        """Displays the stats of a provided ship"""
        shipname = shipname.lower()
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = users[str(ctx.author.id)]
        try:
            ship = user['ships'][shipname.capitalize()]
        except KeyError:
            return await ctx.send(f'I couldn\'t find that ship in your account, make sure you own it. Use `{ctx.prefix}shop ships` to view info about ships you may not own.')
        desc = ship['description']
        peak = str(ship['max']) + ' Stellics'
        upgradecost = str(ship['upgradecost']) + ' Stellics'
        cooldown = str(ship['cooldown']) + ' seconds'
        level = str(ship['level'])
        constructed = f'__**`{shipname.capitalize()}`**__\n**Level: **{level}\n**Description: **{desc}\n**Max Scavage: **{peak}\n**Upgrade Cost: **{upgradecost}\n**Cooldown: **{cooldown}'
        pages = menus.MenuPages(source=ShipSource(
            [constructed]), delete_message_after=True)
        await pages.start(ctx)

    @commands.command(aliases=['pi'])
    @check_account()
    async def planetinfo(self, ctx, planetname: str):
        """Displays the stats of a provided planet"""
        planetname = planetname.lower()
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = users[str(ctx.author.id)]
        try:
            planet = user['planets'][planetname.capitalize()]
        except KeyError:
            return await ctx.send(f'I couldn\'t find that planet in your account, make sure you own it. Use `{ctx.prefix}shop planets` to view info about planets you may not own.')
        desc = planet['description']
        chance = str(planet['chance']) + '%'
        upgradecost = str(planet['upgradecost']) + ' Stellics'
        cooldown = str(planet['cooldown']) + ' seconds'
        level = str(planet['level'])
        constructed = f'__**`{planetname.capitalize()}`**__\n**Level: **{level}\n**Description: **{desc}\n**Artifact Chance: **{chance}\n**Upgrade Cost: **{upgradecost}\n**Cooldown: **{cooldown}'
        pages = menus.MenuPages(source=PlanetSource(
            [constructed]), delete_message_after=True)
        await pages.start(ctx)

    @commands.command()
    @check_account()
    async def planets(self, ctx):
        """Displays all your planets, and their stats"""
        with open('users.json', 'r') as f:
            users = json.load(f)
        user = users[str(ctx.author.id)]
        planets = []
        for i in user['planets']:
            name = i
            i = user['planets'].get(i)
            desc = i['description']
            chance = str(i['chance']) + '%'
            upgradecost = str(i['upgradecost']) + ' Stellics'
            cooldown = str(i['cooldown']) + ' seconds'
            level = str(i['level'])
            constructed = f'__**`{name}`**__\n**Level: **{level}\n**Description: **{desc}\n**Artifact Chance: **{chance}\n**Upgrade Cost: **{upgradecost}\n**Cooldown: **{cooldown}'
            planets.append(constructed)
        pages = menus.MenuPages(source=PlanetSource(
            planets), delete_message_after=True)
        await pages.start(ctx)


def setup(bot):
    bot.add_cog(economy(bot))
