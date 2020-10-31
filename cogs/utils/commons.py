import json
import re

from discord.ext import commands

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k] * float(v)
            except KeyError:
                raise commands.BadArgument(f"{k} is an invalid time-key! h/m/s/d are valid!")
            except ValueError:
                raise commands.BadArgument(f"{v} is not a number!")
        return time


def getallcustoms(object) -> str:
    dicted = {}
    for i in dir(object):
        if not str(i).startswith('__') and not str(getattr(object, i)).startswith('<'):
            dicted[i] = str(getattr(object, i))
    dicted = json.dumps(dicted, indent=4)
    return dicted


def loadjson(filename: str) -> dict:
    with open(f'{filename}.json', 'r') as f:
        result = json.load(f)
    return result


def dumpjson(filename: str, data: dict) -> None:
    with open(f'{filename}.json', 'w') as f:
        json.dump(data, f, indent=4)
