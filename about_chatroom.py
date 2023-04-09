import random
from json import loads, dumps

CADD = "onlineAdd"
CREMOVE = "onlineRemove"
CCHAT = "chat"

def JOIN(nick, channel, password=""):
    return dumps({
        "cmd":"join",
        "nick":"%s#%s" % (nick, password),
        "channel":channel
    })
def CHAT(text):
    return dumps({
        "cmd":"chat",
        "text":text
    })
def COLOR2(code=random.randint(0, 0xffff)):
    return CHAT("/color %06x" % code)