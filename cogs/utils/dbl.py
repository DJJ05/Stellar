import aiohttp

from .commons import loadjson

SECRETS = loadjson('config')
TOKEN = SECRETS['dbl_token']

HEADERS = dict(Authorization=TOKEN)

SESSION = aiohttp.ClientSession()

CHECKURL = 'https://top.gg/api/bots/758065684218380350/check'
CHECKALLURL = 'https://top.gg/api/bots/758065684218380350/votes'


async def checkvoter(uid: int) -> bool:
    p = {'userId': uid}
    resp = await SESSION.get(CHECKURL, headers=HEADERS, params=p)
    data: dict = await resp.json()
    if bool(data['voted']):
        return True
    return False


async def getvotes() -> list:
    resp = await SESSION.get(CHECKALLURL, headers=HEADERS)
    data: dict = await resp.json()
    return data
