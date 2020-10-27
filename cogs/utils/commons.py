import json


def getallcustoms(object) -> dict:
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
