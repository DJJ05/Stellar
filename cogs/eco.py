import asyncio
import datetime
import random

import humanize
from discord.ext import commands, menus

from .utils.checks import check_account
from .utils.commons import loadjson, dumpjson
from .utils.paginator import ShipSource, PlanetSource, ShopSource, InvSource
from .utils.templates import NEW_ACC


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create(self, ctx):
        """Creates your Stellar account."""
        users = loadjson('users')
        if str(ctx.author.id) in users.keys():
            return await ctx.send(
                f'You already have an account. Close your existing account using `{ctx.prefix}close`.')
        users[str(ctx.author.id)] = NEW_ACC
        dumpjson('users', users)
        return await ctx.send('Account successfully created! Enjoy!')

    @commands.command()
    @check_account()
    async def close(self, ctx, confirm=None):
        """Closes your stellar account. Use close yes to auto confirm the closure."""
        users = loadjson('users')
        if confirm and confirm.lower() == 'yes':
            users.pop(str(ctx.author.id))
            dumpjson('users', users)
            return await ctx.send(
                f'Alright, I deleted your account for you, feel free to use `{ctx.prefix}create` at any time.')
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
                dumpjson('users', users)
                return await ctx.send(
                    f'Alright, I deleted your account for you, feel free to use `{ctx.prefix}create` at any time.')
            return await ctx.send(f'Cancelled.')

    @commands.command(aliases=['balance'])
    @check_account()
    async def bal(self, ctx):
        """Displays your balance in Stellics."""
        users = loadjson('users')
        user = users[str(ctx.author.id)]
        embed = self.bot.Embed(
            title=f'{ctx.author.display_name}\'s balance'
        )
        embed.add_field(name='Stellics', value=user['balance'])
        return await ctx.send(embed=embed)

    @commands.command()
    @check_account()
    async def ships(self, ctx):
        """Displays all your ships, and their stats"""
        users = loadjson('users')
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
            constructed = f'__**`{name}`**__\n**Level: **{level}\n**Description: **{desc}\n**Max Scavenge: **{peak}\n**Upgrade Cost: **{upgradecost}\n**Cooldown: **{cooldown} '
            ships.append(constructed)
        pages = menus.MenuPages(source=ShipSource(
            ships), delete_message_after=True, clear_reactions_after=True)
        await pages.start(ctx)

    @commands.command(aliases=['si'])
    @check_account()
    async def shipinfo(self, ctx, shipname: str):
        """Displays the stats of a provided ship"""
        shipname = shipname.lower()
        users = loadjson('users')
        user = users[str(ctx.author.id)]
        try:
            ship = user['ships'][shipname.capitalize()]
        except KeyError:
            return await ctx.send(
                f'I couldn\'t find that ship in your account, make sure you own it. Use `{ctx.prefix} shop ships` to view info about ships you may not own.')
        desc = ship['description']
        peak = str(ship['max']) + ' Stellics'
        upgradecost = str(ship['upgradecost']) + ' Stellics'
        cooldown = str(ship['cooldown']) + ' seconds'
        level = str(ship['level'])
        constructed = f'__**`{shipname.capitalize()}`**__\n**Level: **{level}\n**Description: **{desc}\n**Max Scavenge: **{peak}\n**Upgrade Cost: **{upgradecost}\n**Cooldown: **{cooldown} '
        pages = menus.MenuPages(source=ShipSource(
            [constructed]), delete_message_after=True, clear_reactions_after=True)
        await pages.start(ctx)

    @commands.command(aliases=['pi'])
    @check_account()
    async def planetinfo(self, ctx, planetname: str):
        """Displays the stats of a provided planet"""
        planetname = planetname.lower()
        users = loadjson('users')
        user = users[str(ctx.author.id)]
        try:
            planet = user['planets'][planetname.capitalize()]
        except KeyError:
            return await ctx.send(
                f'I couldn\'t find that planet in your account, make sure you own it. Use `{ctx.prefix}shop planets` to view info about planets you may not own.')
        desc = planet['description']
        chance = str(planet['chance']) + '%'
        upgradecost = str(planet['upgradecost']) + ' Stellics'
        cooldown = str(planet['cooldown']) + ' seconds'
        level = str(planet['level'])
        constructed = f'__**`{planetname.capitalize()}`**__\n**Level: **{level}\n**Description: **{desc}\n**Artifact Chance: **{chance}\n**Upgrade Cost: **{upgradecost}\n**Cooldown: **{cooldown} '
        pages = menus.MenuPages(source=PlanetSource(
            [constructed]), delete_message_after=True, clear_reactions_after=True)
        await pages.start(ctx)

    @commands.command()
    @check_account()
    async def planets(self, ctx):
        """Displays all your planets, and their stats"""
        users = loadjson('users')
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
            constructed = f'__**`{name}`**__\n**Level: **{level}\n**Description: **{desc}\n**Artifact Chance: **{chance}\n**Upgrade Cost: **{upgradecost}\n**Cooldown: **{cooldown} '
            planets.append(constructed)
        pages = menus.MenuPages(source=PlanetSource(
            planets), delete_message_after=True, clear_reactions_after=True)
        await pages.start(ctx)

    @commands.command(aliases=['scavange'])
    @check_account()
    async def scavenge(self, ctx, shipname: str):
        """Scavenge for Stellics with a specified ship. Keep in mind that the cooldown for whichever ship you use
        will apply across all ships until your next scavenge. """
        shipname = shipname.lower().capitalize()
        users = loadjson('users')
        user = users[str(ctx.author.id)]
        cooldowns = loadjson('cooldowns')
        current = str(ctx.message.created_at)
        try:
            past = cooldowns['scavenge'].get(str(ctx.author.id))
            if past:
                past = datetime.datetime.strptime(past, '%Y-%m-%d %H:%M:%S.%f')
                current = datetime.datetime.strptime(
                    current, '%Y-%m-%d %H:%M:%S.%f')
                if current < past:
                    return await ctx.send(
                        f'You are still on cooldown for another {humanize.precisedelta(past - current)}, due to your ship\'s cooldown settings.')
        except KeyError:
            pass
        ship = user['ships'].get(shipname)
        if not ship:
            return await ctx.send(f'Ship not found, make sure you own it with `{ctx.prefix}ships`.')
        cooldown = ship['cooldown']
        current = ctx.message.created_at
        current += datetime.timedelta(seconds=cooldown)
        cooldowns['scavenge'][str(ctx.author.id)] = str(current)
        dumpjson('cooldowns', cooldowns)
        to_add = random.randint(2, ship['max'])
        user['balance'] += to_add
        dumpjson('users', users)
        return await ctx.send(
            f'You managed to scavenge for {to_add} Stellics, and are now on cooldown due to your ship\'s cooldown settings.')

    @commands.command()
    @check_account()
    async def search(self, ctx, planetname: str):
        """Search for artifacts on a specified planet. Keep in mind that the cooldown for whichever planet you use
        will apply across all planets until your next search. """
        planetname = planetname.lower().capitalize()
        users = loadjson('users')
        user = users[str(ctx.author.id)]
        cooldowns = loadjson('cooldowns')
        current = str(ctx.message.created_at)
        try:
            past = cooldowns['search'].get(str(ctx.author.id))
            if past:
                past = datetime.datetime.strptime(past, '%Y-%m-%d %H:%M:%S.%f')
                current = datetime.datetime.strptime(
                    current, '%Y-%m-%d %H:%M:%S.%f')
                if current < past:
                    return await ctx.send(
                        f'You are still on cooldown for another {humanize.precisedelta(past - current)} due to your planet\'s cooldown settings.')
        except KeyError:
            pass
        planet = user['planets'].get(planetname)
        if not planet:
            return await ctx.send(f'Planet not found, make sure you own it with `{ctx.prefix}planets`.')
        cooldown = planet['cooldown']
        current = ctx.message.created_at
        current += datetime.timedelta(seconds=cooldown)
        cooldowns['search'][str(ctx.author.id)] = str(current)
        dumpjson('cooldowns', cooldowns)
        rng = random.randint(1, 100)
        if rng > planet['chance']:
            return await ctx.send(
                'Your search yielded no results and you are now on cooldown due to your planets\'s cooldown settings.')
        catalogue = loadjson('catalogue')
        artifacts = catalogue['Artifacts'][1]
        artifact = random.choice(list(artifacts))
        if not user['inventory'].get(artifact):
            user['inventory'][artifact] = 1
        else:
            user['inventory'][artifact] += 1
        dumpjson('users', users)
        return await ctx.send(
            f'Your search was successful, and you found one {artifact}! View your artifacts with `{ctx.prefix}inv` and sell your artifact(s) with `{ctx.prefix}sell`.')

    @commands.group(invoke_without_command=True, aliases=['store'])
    async def shop(self, ctx):
        """Shop commands, displaying buy costs, upgrade costs and other information on a specifiec category."""
        await ctx.send_help(ctx.command)

    @shop.command(aliases=['ship'], name='ships')
    async def shop_ships(self, ctx):
        """View information about the various ships available for purchase."""
        ca = loadjson('catalogue')
        s = ca['Ships']
        sd = s[0]
        s.remove(sd)
        sf = []
        for ss in s:
            for n, d in ss.items():
                de = d['description']
                p = str(d['max']) + ' Stellics'
                u = str(d['upgradecost']) + ' Stellics'
                c = str(d['cooldown']) + ' seconds'
                b = str(d['buycost']) + ' Stellics'
                co = f'__**`{n}`**__\n**Description: **{de}\n**Buy Cost: **{b}\n**Base Max Scavenge: **{p}\n**Base Upgrade Cost: **{u}\n**Base Cooldown: **{c}'
                sf.append(co)
        pages = menus.MenuPages(source=ShopSource(
            sf), delete_message_after=True, clear_reactions_after=True)
        await pages.start(ctx)

    @commands.command(aliases=['inventory'])
    @check_account()
    async def inv(self, ctx):
        """Check your inventory, including all of your artifacts! If you are looking for the invite link,
        use the invite command. """
        u = loadjson('users')
        c = loadjson('catalogue')
        a = []
        i = u[str(ctx.author.id)]['inventory']
        if not len(i):
            a.append(f'You do not own any artifacts! You can search for artifacts using `{ctx.prefix}search`.')
        for n in i:
            q = i.get(n)
            de = c['Artifacts'][1]
            d = de.get(n)
            f = f'__**`{n}`**__\n**Quantity: **{q}\n**Description: **{d}'
            a.append(f)
        pages = menus.MenuPages(source=InvSource(
            a), delete_message_after=True, clear_reactions_after=True)
        await pages.start(ctx)

    # TODO: Add leaderboard guild specific command
    # TODO: Add sell command
    # TODO: Trading command?
    # TODO: More artifacts ships planets etc
    # TODO: Pets
    # TODO: Bot listing
    # TODO: Market?
    # TODO: Pay and ask for? Maybe opt-in to getting DMed about payment requests
    # TODO: Rob? No idea how but guild specific for sure, passive?
    # TODO: Giveaways in support server
    # TODO: Voting crates once top.gg
    # TODO: Regular buy crates?
    # TODO: Global leaderboard? Might be resource intensive
    # TODO: DEV COG: manual removal, giving etc
    # TODO: Config cog for guild-specifics
    # TODO: Meta commands - about
    # TODO: On_guild_join


def setup(bot):
    bot.add_cog(Economy(bot))
