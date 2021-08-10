import discord
from Android.IUser import IUser
import sqlite3
from iDB import iDB
from ITask import ITask
import Operation

class OP_SeeTaskBoard(OPUnit):

    def __init__(self, user: IUser, c: sqlite3.Cursor) -> None:
        super().__init__(user, c)

        self.Itemlist=iDB.Get('tasks.db','_TASK',condition='WHERE username = "MarcieM"')
        self.ItemCount=len(self.Itemlist)
        self.CurrentSelection=0
        OP_SeeTaskBoard.PH_Left=['L','l','left','LEFT']
        OP_SeeTaskBoard.PH_Right=['R','r','right','RIGHT']
        OP_SeeTaskBoard.PH_Select=['select','s','SELECT','S','YES','y','Y','yes']
        pass

    def Listen(self, text: str, c):

        if text[0] in OP_SeeTaskBoard.PH_Left:
            self.CurrentSelection=max(self.CurrentSelection-1,0)
            pass
        if text[0] in OP_SeeTaskBoard.PH_Right:
            self.CurrentSelection=min(self.CurrentSelection+1,self.ItemCount-1)
            pass
        return super().Listen(text,c)
        pass

    def Say(self) -> str:


        return ITask(self.Itemlist[self.CurrentSelection]).__str__()
        pass
