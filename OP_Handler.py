from typing import Text as Text
import discord
import sqlite3
from Android import IUser
import Operation
 
class OPHandler:
    def __init__(self, user: discord.user.User) -> None:
        OPHandler.Initializers=['!T','!t','!task','!TASK']
        self.conn = sqlite3.connect("tasks.db")
        self.c = self.conn.cursor()
        self.user=discord.User
        self.user = user
        self.CurOp = Operation.OPBase(self.user, self.c)
        self.Interacted=True
        self.lang='jp'

        # self.Say(self.CurOp.Say())
        pass

    async def Onmessage(self, message:discord.Message):
        text = message.content.split(",")
        self.Interacted=True
        if len(text) > 1:
            
            for a in OPHandler.Initializers:
                if a in text:
                    text.remove(a)
                pass
            res = self.CurOp.Listen(text, self.c)
           
            if type(res) != type(None):
                if type(res)==Operation.LangPackage:
                    print(type(res.next))
                    self.CurOp=res.next
                    self.lang=res.lang
                    pass
                else:
                    self.CurOp = res
                    pass
                print(type(res))
                await self.Say(self.CurOp.Say(self.lang))
                pass
            else:
                await self.Say(self.CurOp.Say(self.lang))
        pass

    pass

    async def Say(self, txt):

        if len(txt)>0:
            print(txt)
            await self.user.send(txt)
        else:
            await self.user.send('nul')

        pass

    pass

