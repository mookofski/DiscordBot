from Android.IUser import IUser
import enum
from typing import Text
import discord
from discord import message
from enum import Enum
import sqlite3
from ITask import ITask
import Text
from iDB import iDB



# say -listen- move
class OPUnit:
    def __init__(self, user:IUser, c:sqlite3.Cursor) -> None:
        self.user = user
        self.c = c
        OPUnit.PH_Exit = ["END", "EXIT"]
        OPUnit.PH_Lang=['lang','LANG']
        self.key='Unit'
        self.result=None
        pass

    def Listen(self, text:str, c):
        print(text)
        if text[0] in OPUnit.PH_Exit:
            self.result= OPBase(self.user,self.c)
        pass
        if text[0] == 'LANG':
            self.result=OP_SetLang(self.user,self.c,self)
            pass
        return self.result
    pass

    def Say(self,lang) -> str:
        return "null"
        pass

    pass


class OPBase(OPUnit):
    def __init__(self, user:discord.user, c:sqlite3.Cursor) -> None:
        self.c = c
        OPUnit.PH_Exit = ["END", "EXIT"]
        OPBase.PH_LIST = ["LIST"]
        OPBase.PH_CHANGE = ["LIST"]
        self.user=user
        self.key='BASE'
        OPBase.PH_CREATE=['CREATE','C']
        OPBase.PH_AGILESELECT=['TAKE','T']

    pass

    def Listen(self, text, c:sqlite3.Cursor):

        self.result= OPBase(self.user, self.c)

        if text[0] == "ADD":
            self.result= OPUpdateTaskInit(self.user, self.c)
            pass
        if text[0] in OPBase.PH_AGILESELECT:
            self.result= OP_SeeTaskBoard(self.user, self.c)
            pass
        if IUser.isAdmin(self.user):
            if text[0] in OPBase.PH_CREATE:
                self.result= OP_CreateTask(self.user, self.c)
                pass
        
        return super().Listen(text,c)
        pass

    def Say(self,lang) -> str:
        return Text.GetText(self.key,lang)


'''
conn=sqlite3.connect('Texts.db')
c=conn.cursor()

q='''
#INSERT INTO _TEXTS VALUES ('{}','{}','{}')
'''.format('CREATE','jp','CREATE')
c.execute(q)

conn.commit()
'''
# Get UpdateCommand, goto Choosing Section
class OPUpdateTaskInit(OPUnit):
    def __init__(self, user:IUser, c:sqlite3.Cursor):
        super().__init__(user, c)

        OPUpdateTaskInit.PH_Confirm = ["YES", "Y"]
        OPUpdateTaskInit.PH_Unconfirm = ["NO", "N"]
        self.key='TASKINIT'
        pass

    def Listen(self, text, c):


        if text[0] in OPUpdateTaskInit.PH_Confirm:
            self.result= OPUpdate_Choose(self.user, self.c)

        if text[0] in OPUpdateTaskInit.PH_Unconfirm:
            self.result= OPBase(self.user, self.c)

        return super().Listen(text, c)


        pass

    def Say(self,lang) -> str:
        return Text.GetText(self.key,lang)

    pass

class OPUpdate_Choose(OPBase):
    def __init__(self, user:IUser, c:sqlite3.Cursor):
        super().__init__(user, c)
        self.PH_UPDATE = ["UPDATE", "up",'U','u']
        self.Task_list = ITask.FindByName(self.user.name)
        self.key='UPDATE_CHOOSE'
        pass

    def Listen(self, text, c):
        
        text = text[0].split(':')
        if text[0] in self.PH_UPDATE:
            res = ITask.FindByName(self.user.name)

            if len(res) > 0:
                self.result= OPUpdateTask(self.user, c, res)
                pass
            pass
        return super().Listen(text, c)

    pass

    def Say(self,lang) -> str:
        # text=str()
        # for i in self.Task_list:
        #    text+=i.__str__()
        #    pass

        # return text
        return "CHOOSE"
        pass

    pass

class OPUpdateTask(OPUnit):
    # list detail on task
    # need interpter
    def __init__(self, user, c, d) -> None:
        super().__init__(user, c)
        self.task = ITask(d)
        OPUpdateTask.PH_EditDesc = ["DESC", "D"]
        OPUpdateTask.PH_EditStete = ["STATE", "S"]
        OPUpdateTask.PH_Commit = ["COMMIT", "C"]
        self.key='UPDATETASK'
        pass

    def Listen(self, text, c):
        if text[0] in OPUpdateTask.PH_EditDesc:
            self.Write("description", text[1])
            pass
        elif text[0] in OPUpdateTask.PH_EditStete:
            self.Write("state", text[1])
            pass
        elif text[0] in OPUnit.PH_Exit:
            self.result= OPBase(self.user, self.c)
            pass

        return super().Listen(text, c)
        pass

    def Write(self, tgt, contents):
        q = """
            UPDATE _TASK
            SET {0} = {1}
            WHERE taskname = {2}
            """.format(
            tgt, contents, self.task.taskname
        )
        self.c.execute(q)
        self.conn.commit()
        pass

    def Say(self,lang) -> str:
        text = self.task.__str__()
        text += "<DESC> <STATE> <EXIT>\n"
        text += "example:!TASK,DESC:Put Description Here\n"

        return self.task.__str__()
        pass

    pass


class OP_CreateTask(OPUnit):
    def __init__(self, user:IUser, c:sqlite3.Cursor) -> None:
        super().__init__(user, c)
        OP_CreateTask.Selection=['SELECT']
        self.userlist=IUser.GetAllUserName()
    pass

    def Listen(self, text, c):
        t=text[0].split(':')
        if t[0] in self.Selection:
            for names in self.userlist:
                if t[1] in names:
                    self.result= OP_CreateTaskToUser(self.user,self.c,IUser.GetUserByName(t[1]))
                pass

            pass
        return super().Listen(text, c)
        pass

    def Say(self,lang):
        text=IUser.GetAllUserList()
        text+='<SELECT>\n'
        text+='exmaple :!TASK,SELECT:molfov'
        
        return text
        pass

class OP_CreateTaskToUser(OPUnit):
    def __init__(self, user: IUser, c: sqlite3.Cursor,tgt:IUser) -> None:
        super().__init__(user, c)

        self.targetuser=IUser
        self.targetuser=tgt
        self.key='CREATE'
        OP_CreateTaskToUser.PH_TASKNAME=['TASKNAME','N','n']
        OP_CreateTaskToUser.PH_TASKSTATE=['TASKSTATE','S','s']
        OP_CreateTaskToUser.PH_TASKDESC=['DESCRIPTION','D','d']
        OP_CreateTaskToUser.PH_TASKST=['START','ST','st']
        OP_CreateTaskToUser.PH_TASKDL=['DEADLINE','DL','dl']
        OP_CreateTaskToUser.PH_TASKSAVE=['SAVE','save']
        

        self.task=ITask()
        self.task.taskname='undefined'
        self.task.username=self.targetuser.name
        self.task.desc='undefined'
        self.task.state='undefined'
        self.task.message='undefined'
        self.task.start=sqlite3.Date(2000,1,1)
        self.task.end=sqlite3.Date(2000,1,1)

        self.elemcount=5
        self.elemfilled=0
    pass

    def Listen(self, text, c):

        t=text[0].split(':')

        if t[0] in OP_CreateTaskToUser.PH_TASKNAME:
            if self.task.taskname=='undefined':
                self.elemfilled+=1

            self.task.taskname=t[1]
            pass
        if t[0] in OP_CreateTaskToUser.PH_TASKDESC:
            if self.task.desc=='undefined':
                self.elemfilled+=1
                
            self.task.desc=t[1]
            pass
        
        if t[0] in OP_CreateTaskToUser.PH_TASKSTATE:
            if self.task.state=='undefined':
                self.elemfilled+=1
                
            self.task.state=t[1]
            pass
        if t[0] in OP_CreateTaskToUser.PH_TASKDL:
            if self.task.end==sqlite3.Date(2000,1,1):
                self.elemfilled+=1
                pass
            d=t[1].split('-')
            self.task.end=sqlite3.Date(int(d[0]),int(d[1]),int(d[2]))
            pass

        if t[0] in OP_CreateTaskToUser.PH_TASKST:
            if self.task.start==sqlite3.Date(2000,1,1):
                self.elemfilled+=1
                pass
            d=t[1].split('-')
            self.task.start=sqlite3.Date(int(d[0]),int(d[1]),int(d[2]))
            pass
        if t[0] in OP_CreateTaskToUser.PH_TASKSAVE:
            if self.elemcount<=self.elemfilled:
                    ITask.AddTask(self.task)
                    self.result= OPBase(self.user,self.c)
                    pass                    
            pass
        return super().Listen(text, c)

        pass

    def Say(self,lang) -> str:
        text = Text.GetText(self.key,lang).format(self.task.username,self.task.taskname,self.task.desc,self.task.state,self.task.start,self.task.end,self.elemfilled,self.elemcount)
        if self.elemcount==self.elemfilled:
            text+='<SAVE>'
            pass
        return text
        pass        

    pass
'''
conn=sqlite3.connect('Texts.db')
c=conn.cursor()
c.execute('''#SELECT * FROM _TEXTS WHERE key = ('CREATE')''')
'''
a=str(c.fetchone()[2])
for i in range(0,4):
    b=a.format(i,'a','a','a','1','3','1','3')
    print(b)
    pass
print(a)
'''
#print(b)

# region obsolete

"""

class OpState(Enum):
    Initial = 0
    Listen = 1
    Confirmation = 2


class Operation:
    def __init__(self):

        self.StateMessage = {0: "Initial", 1: "Listen", 2: "Confirmation"}

        self.Operations = {
            OpState.Listen: self.Listen,
            OpState.Confirmation: self.Confirmation,
        }

        self.ID = -1
        self.InternalStage = OpState.Initial
        self.CurrentText = self.InitialText

        self.Activators = {"Item1": 0, "Item2": 1}
        self.ItemCount = 0
        self.ItemMax = 3
        pass

    async def Send(self):
        await message.channel.send(self.CurrentText)

        pass

    def NullOp(self, Message):
        pass

    def Commit(self):
        pass

    def CheckItem(self, Message):
        text = str()
        text += "Undefined Operation"
        return text
        pass  # func end

    def Listen(self, Texts):

        for i in Texts:
            Item = i.split("|")
            self.Activators.get(Item[0])
            pass
        pass

    async def GetState(self, Message):
        await Message.channel.send(
            self.StateMessage.get(self.InternalStage, "Undefined State")
        )
        pass


class Operation_DM_Update(Operation):
    def __init__(self):

        self.StateMessage = {0: "Initial", 1: "Listen", 2: "Confirmation"}

        self.Operations = {
            OpState.Listen: self.Listen,
            OpState.Confirmation: self.Confirmation,
        }

        self.ID = -1
        self.InternalStage = OpState.Initial
        self.CurrentText = self.InitialText

        self.Activators = {"Item1": 0, "Item2": 1}
        self.ItemCount = 0
        self.ItemMax = 3

    pass

    pass


class Operation_Add(Operation):
    def __init__(self):

        self.StateMessage = {0: "Initial", 1: "Listen", 2: "Confirmation"}
        self.Operations = {
            OpState.Listen: self.Listen,
            OpState.Confirmation: self.Confirmation,
        }

        self.OpState = OpState.Listen

        self.ID = -1
        self.InternalStage = OpState.Initial
        self.CurrentText = str()

        self.Task = "Undefined"
        self.Date = -1
        self.Description = "Undefined"

        self.Activators = {
            "TASK": self.Task,
            "DATE": self.Date,
            "DESC": self.Description,
        }
        self.ItemCount = 0
        self.ItemMax = 3

        pass

    def CheckItem(self, Message):
        text = str()

        text += "AddOp"
        #        text+=type(self).__name__
        text += "\n"

        text += "Task:"
        text += self.Task
        text += "\n"

        text += "Date:"
        text += str(self.Date)
        text += "\n"

        text += "Desc:"
        text += self.Description
        text += "\n"

        text += "\n"

        if self.ItemCount != 0:
            text += "{}/{}: {}%Done".format(
                self.ItemCount, self.ItemMax, int((self.ItemCount / self.ItemMax) * 100)
            )
        else:
            text += "0/{}: 0%Done".format(self.ItemCount)

        text += "\n\n"
        text += "Syntax (!TASK,Name:Contents)"

        text += "\n"
        text += "<RESET>"

        if self.ItemCount == self.ItemMax:
            text += "   <CONFIRM>"
            pass  # add Confirmation end

        return text
        pass  # func end

    def Listen(self, Message, c):  # take Item and store it inside
        Texts = Message.content.split(",")
        for i in Texts:
            Item = i.split(":")

            op = Item[0].upper()

            # set if else
            # ==============================
            if op in "TASK":
                if self.Task == "Undefined":
                    self.ItemCount += 1
                    pass
                self.Task = Item[1]
            pass
            if op in "DESC":
                if self.Description == "Undefined":
                    self.ItemCount += 1
                    pass
                self.Description = Item[1]
            pass
            if op in "DATE":
                if self.Date <= 0:
                    self.ItemCount += 1
                    pass
                self.Date = Item[1]
            if (op in "CONFIRM") | self.ItemCount == self.ItemMax:

                pass
            pass
        # ================================
        pass  # text Loop
        return self.CheckItem(Message)

    pass  # Main Func

    def Commit(self, Message, c):
        c.execute(
            "INSERT INTO _TASK_INST VALUES(?,?,?)",
            (
                self.Task,
                self.Date,
                self.Description,
            ),
        )

        pass

    async def Operation(self, Message, c):

        # op=self.Operation(self.OpState,self.NullOp)

        await Message.channel.send(self.Listen(Message, c))

        pass  # Main Func
"""



class OP_SetLang(OPUnit):
    def __init__(self, user: IUser, c: sqlite3.Cursor,prev:OPUnit) -> None:
        super().__init__(user, c)
        OP_SetLang.key='LANG'
        self.prev=prev
        
        pass
    
    def Listen(self, text: str, c):
        if text[0] in ['jp']:
            self.result=LangPackage(self.user,self.c,'jp',self.prev)
        if text[0] in ['en']:
            self.result=LangPackage(self.user,self.c,'en',self.prev)


        return super().Listen(text, c)
        pass
    def Say(self, lang) -> str:
        return Text.GetText(OP_SetLang.key,lang)

    pass

class LangPackage(OPUnit):
    def __init__(self, user: IUser, c: sqlite3.Cursor,lang:str,prev:OPUnit) -> None:
        super().__init__(user, c)
        self.lang=lang
        self.next=prev
        pass

    pass


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

    def Say(self,lang) -> str:


        return ITask(self.Itemlist[self.CurrentSelection]).__str__(lang)
        pass
