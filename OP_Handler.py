from typing import Text as Text
import discord
import sqlite3
from Android import IUser
import Operation
 
class OPHandler:
    def __init__(self, user: discord.user.User) -> None:
        OPHandler.Initializers=['!T','!t','!task','!TASK']
        self.conn = sqlite3.connect("tasks.db")
        self.user=discord.User
        self.user = user
        self.CurOp = Operation.OPBase(self.user)
        self.Interacted=True

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
            res = self.CurOp.Listen(text)
           
            if type(res) != type(None):
                if type(res)==Operation.LangPackage:
                    print(type(res.next))
                    self.CurOp=res.next
                    pass
                else:
                    self.CurOp = res
                    pass
                print(type(res))
                await self.Say(self.CurOp.Say(IUser.GetLang(self.user.name)))
                pass
            else:
                await self.Say(self.CurOp.Say(IUser.GetLang(self.user.name)))
        pass

    pass

    async def Say(self, txt:str):

        if len(txt)>0:
            print(txt)
            await self.user.send(txt)
        else:
            await self.user.send('nul')

        pass

    pass

