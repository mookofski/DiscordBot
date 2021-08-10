from Operation import OPUnit
from Android.IUser import *
import sqlite3



class OP_Select_Base(OPUnit):
    def __init__(self, user: IUser, c: sqlite3.Cursor) -> None:
        super().__init__(user, c)
        self.Itemlist=list()
        self.CurrentSelection=0
        OP_Select_Base.PH_Left=['L','l','left','LEFT']
        OP_Select_Base.PH_Right=['R','r','right','RIGHT']
        OP_Select_Base.PH_Select=['select','s','SELECT','S','YES','y','Y','yes']
        self.ItemCount=len(self.Itemlist)
        pass
    
    def Listen(self, text: str, c):

        if text in OP_Select_Base.PH_Left:
            self.CurrentSelection=max(self.CurrentSelection-1,0)
            pass
        if text in OP_Select_Base.PH_Right:
            self.CurrentSelection=min(self.CurrentSelection+1,self.ItemCount-1)
            pass
        

        pass
    def Say(self) -> str:
        if self.ItemCount>0:
            return self.Itemlist[self.CurrentSelection].__str__()
        else:
            return 'No Item Found'
        pass
    
    pass