import re
import ssl
import json
import random
import socket
import struct
import requests
from threading import Thread
from multiprocessing import Lock
from websocket_client import create_connection
# local packages
from message import *
from analyse_nick import *
from about_chatroom import *
from poker import *

Brand.reprfmt = r"***[%s]()***"

'''
`***[%s]()***`
`**%s**` 
`### **%s**`
`### ==**%s**==`
'''

class Main(Scene):
    def __init__(self):
        self.pipe, self.pipelock = [], Lock()
        self.in_game = []
        try:
            self.bot = create_connection(url="wss://hack.chat/chat-ws")
        except Exception as error:
            print("report error when connecting, exit...")
            exit()
        else:
            self.bot.send(JOIN("Ea8a", "poker", "ep8"))
            t = Thread(target=self._listen)
            t.setDaemon(True)
            t.start()

        # join game
        while True: # not stop
            while True:
                m = self._getpipemsg()
                if m[1].strip() == "p0ker":
                    if m[0] not in self.in_game:
                        self.prompt("*POKER MASTER*")
                        self.in_game.append(m[0])
                    else:
                        self.prompt("You have been in")
                if len(self.in_game) == 3:
                    break
            Scene.__init__(self, *self.in_game)
            self.in_game.clear()
            self.bot.close()

    def _getpipemsg(self):
        while True:
            if self.pipe:
                p = self.pipe[0]
                self.pipelock.acquire()
                self.pipe.pop(0)
                self.pipelock.release()
                return p

    def _listen(self):
        while True:
            # receive data
            try:
                data = json.loads(self.bot.recv())
            except Exception as error:
                print("error: ", error)
                continue
            else:
                if data["cmd"] == CCHAT:
                    data_nick = data["nick"]
                    data_text = data["text"]
                    self.pipelock.acquire()
                    self.pipe.append((data_nick, data_text))
                    self.pipelock.release()
        self.bot.close()

    def prompt(self, *args):
        self.bot.send(json.dumps({
            "cmd":"chat",
            "text":"**%s**" % "".join([str(i) for i in args])}))

    def promptquietly(self, playername, *args):
        self.bot.send(json.dumps({
            "cmd":"chat",
            "text":"/w %s %s" % (playername, ''.join([str(i) for i in args]))}))

    def getinput(self, player):
        while True:
            m = self._getpipemsg()
            if m[0] == player:
                return m[1]

if __name__ == "__main__":
    main = Main()
    run()
