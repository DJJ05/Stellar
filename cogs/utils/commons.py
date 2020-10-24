import json


def getallcustoms(object) -> dict:
    dicted = {}
    for i in dir(object):
        if not str(i).startswith('__') and not str(getattr(object, i)).startswith('<'):
            dicted[i] = str(getattr(object, i))
    dicted = json.dumps(dicted, indent=4)
    return dicted
