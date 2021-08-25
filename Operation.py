from Android.IUser import IUser
from typing import Text
import discord
import sqlite3
from ITask import FindTaskByTaskName, ITask, IsCompleted
import Text
from iDB import iDB

#region Base

# say -listen- move
class OPUnit:
    def __init__(self, user: IUser) -> None:
        self.user = user
        OPUnit.PH_Exit = ["EXIT"]
        OPUnit.PH_Lang = ["lang", "LANG"]
        self.key = "Unit"
        self.result = None
        pass

    def Listen(self, text: str):
        print(text)
        arg=text[0].upper()
        if type(self.result)==OP_SetLang:
            self.result=None
            pass
        if arg in OPUnit.PH_Exit:
            self.result = OPBase(self.user)
        pass
        if arg in ["lang", "LANG"]:
            self.result = OP_SetLang(self.user, self)
            pass
        return self.result

    pass

    def Say(self, lang) -> str:
        return "null"
        pass

    pass


class OPBase(OPUnit):
    def __init__(self, user: discord.user) -> None:
        OPUnit.PH_Exit = ["END", "EXIT"]
        OPBase.PH_LIST = ["LIST","L"]
        OPBase.PH_CHANGE = ["LIST"]
        OPBase.PH_UPDATE = ["UPDATE","U"]

        self.user:discord.User
        self.user = user
        self.key = "BASE"
        OPBase.PH_CREATE = ["CREATE", "C"]
        OPBase.PH_AGILESELECT = ["TAKE", "T"]

    pass

    def Listen(self, text: sqlite3.Cursor):

        self.result = OPBase(self.user)
        arg:str
        arg=text[0].upper()
        if arg in OPBase.PH_UPDATE:
            self.result = OPUpdate_Choose(self.user)
            pass
        if arg in OPBase.PH_LIST:
            self.result = OP_List(self.user)
            pass

        if IUser.isAdmin(self.user):
            if arg in OPBase.PH_CREATE:
                self.result = OP_CreateTask(self.user)
                pass
            if arg in OPBase.PH_AGILESELECT:
                self.result = OP_SeeTaskBoard(self.user)
            pass

        return super().Listen(text)
        pass

    def Say(self, lang) -> str:
        text=Text.GetText(self.key, lang).format(self.user.name)

        return text
#endregion Base

#region Update

# Get UpdateCommand, goto Choosing Section
class OPUpdateTaskInit(OPUnit):
    def __init__(self, user: IUser):
        super().__init__(user)

        OPUpdateTaskInit.PH_Confirm = ["YES", "Y"]
        OPUpdateTaskInit.PH_Unconfirm = ["NO", "N"]
        self.key = "TASKINIT"
        pass

    def Listen(self, text):

        if text[0] in OPUpdateTaskInit.PH_Confirm:
            self.result = OPUpdate_Choose(self.user)

        if text[0] in OPUpdateTaskInit.PH_Unconfirm:
            self.result = OPBase(self.user)

        return super().Listen(text)

        pass

    def Say(self, lang) -> str:
        return Text.GetText(self.key, lang)

    pass


class OPUpdate_Choose(OPUnit):
    def __init__(self, user: IUser):
        super().__init__(user)
        self.PH_UPDATE = ["UPDATE", "up", "U", "u"]
        self.Task_list=list[ITask]()
        l=ITask.FindByName(self.user.name)
        
        for a in l:
            self.Task_list.append(ITask(a))
            pass
        
        OPUpdate_Choose.key = "UPDATE_CHOOSE"
        
        pass

    def Listen(self, text):

        res = FindTaskByTaskName(text[0])

        if res!=None:
            self.result = OPUpdateTask(self.user,res)
            pass
        pass
        
        return super().Listen(text)

    pass

    def Say(self, lang) -> str:
        fmt = Text.GetText(OPUpdate_Choose.key, lang)
        st = str()
        ct=1
        for a in self.Task_list:
            if a.state not in "DONE":
                st+='no:'+ct.__str__()+'\n'
                st += a.__str__(lang=lang)
                st += "\n"
                ct+=1
                pass
            pass

        st += fmt

        return st
        pass

    pass


class OPUpdateTask(OPUnit):
    # list detail on task
    # need interpter
    def __init__(self, user, d:ITask) -> None:
        super().__init__(user)
        self.task:ITask = d
        OPUpdateTask.PH_EditDesc = ["DESC", "D"]
        OPUpdateTask.PH_EditStete = ["STATE", "S"]
        OPUpdateTask.PH_Commit = ["End", "E"]
        self.key = "UPDATETASK"
        pass

    def Listen(self, text):
        
        t=text[0].split(':')

        arg:str=t[0].upper()
        if arg in OPUpdateTask.PH_EditDesc:
            self.Write("description", t[1])
            pass
        elif arg in OPUpdateTask.PH_EditStete:
            self.Write("state", t[1])
            pass
        elif arg in OPUnit.PH_Exit:
            self.result = OPBase(self.user)
            pass

        return super().Listen(text)
        pass

    def Write(self, tgt, contents):
        if tgt=='state':
            ITask.UpdateTask(taskname=self.task.taskname,state=contents)
            pass
        if tgt=='description':
            ITask.UpdateTask(taskname=self.task.taskname,desc=contents)
            pass 
        pass

    def Say(self, lang) -> str:
        
        t:ITask=FindTaskByTaskName(self.task.taskname)
        text = t.__str__(lang=lang)
        text += Text.GetText(self.key,lang)

        return text
        pass

    pass
#endregion Update

#region Create


class OP_CreateTask(OPUnit):
    def __init__(self, user: IUser) -> None:
        super().__init__(user)
        OP_CreateTask.Selection = ["SELECT"]
        self.userlist = IUser.GetAllUserName()

    pass

    def Listen(self, text):
        t = text[0].split(":")
        if t[0] in self.Selection:
            for names in self.userlist:
                if t[1] in names:
                    self.result = OP_CreateTaskToUser(
                        self.user, IUser.GetUserByName(t[1])
                    )
                pass

            pass
        return super().Listen(text)
        pass

    def Say(self, lang):
        text = IUser.GetAllUserList()
        text += "<SELECT>\n"
        text += "exmaple :!TASK,SELECT:molfov"

        return text
        pass


class OP_CreateTaskToUser(OPUnit):
    def __init__(self, user: IUser, tgt: IUser) -> None:
        super().__init__(user)

        self.targetuser = IUser
        self.targetuser = tgt
        self.key = "CREATE"
        OP_CreateTaskToUser.PH_TASKNAME = ["TASKNAME", "N", "n"]
        OP_CreateTaskToUser.PH_TASKSTATE = ["TASKSTATE", "S", "s"]
        OP_CreateTaskToUser.PH_TASKDESC = ["DESCRIPTION", "D", "d"]
        OP_CreateTaskToUser.PH_TASKST = ["START", "ST", "st"]
        OP_CreateTaskToUser.PH_TASKDL = ["DEADLINE", "DL", "dl"]
        OP_CreateTaskToUser.PH_TASKSAVE = ["SAVE", "save"]

        self.task = ITask()
        self.task.taskname = "undefined"
        self.task.username = self.targetuser.name
        self.task.desc = "undefined"
        self.task.state = "undefined"
        self.task.message = "undefined"
        self.task.start = sqlite3.Date(2000, 1, 1)
        self.task.end = sqlite3.Date(2000, 1, 1)

        self.elemcount = 5
        self.elemfilled = 0

    pass

    def Listen(self, text):

        t = text[0].split(":")

        if t[0] in OP_CreateTaskToUser.PH_TASKNAME:
            if self.task.taskname == "undefined":
                self.elemfilled += 1

            self.task.taskname = t[1]
            pass
        if t[0] in OP_CreateTaskToUser.PH_TASKDESC:
            if self.task.desc == "undefined":
                self.elemfilled += 1

            self.task.desc = t[1]
            pass

        if t[0] in OP_CreateTaskToUser.PH_TASKSTATE:
            if self.task.state == "undefined":
                self.elemfilled += 1

            self.task.state = t[1]
            pass
        if t[0] in OP_CreateTaskToUser.PH_TASKDL:
            if self.task.end == sqlite3.Date(2000, 1, 1):
                self.elemfilled += 1
                pass
            d = t[1].split("-")
            self.task.end = sqlite3.Date(int(d[0]), int(d[1]), int(d[2]))
            pass

        if t[0] in OP_CreateTaskToUser.PH_TASKST:
            if self.task.start == sqlite3.Date(2000, 1, 1):
                self.elemfilled += 1
                pass
            d = t[1].split("-")
            self.task.start = sqlite3.Date(int(d[0]), int(d[1]), int(d[2]))
            pass
        if t[0] in OP_CreateTaskToUser.PH_TASKSAVE:
            if self.elemcount <= self.elemfilled:
                ITask.AddTask(self.task)
                self.result = OPBase(self.user)
                pass
            pass
        return super().Listen(text)

        pass

    def Say(self, lang) -> str:
        text = Text.GetText(self.key, lang).format(
            self.task.username,
            self.task.taskname,
            self.task.desc,
            self.task.state,
            self.task.start,
            self.task.end,
            self.elemfilled,
            self.elemcount,
        )
        if self.elemcount == self.elemfilled:
            text += "<SAVE>"
            pass
        return text
        pass

    pass
#endregion Create

#region Util
class OP_SetLang(OPUnit):
    def __init__(self, user: IUser, prev: OPUnit) -> None:
        super().__init__(user)
        OP_SetLang.key = "LANG"
        self.prev = prev

        pass

    def Listen(self, text: str):
        if text[0] in ["jp"]:
            self.result = LangPackage(self.user, "jp", self.prev)
            IUser(self.user).SetLang(lang='jp')
        if text[0] in ["en"]:
            self.result = LangPackage(self.user, "en", self.prev)
            IUser(self.user).SetLang(lang='en')
        return super().Listen(text)
        pass

    def Say(self, lang) -> str:
        return Text.GetText(OP_SetLang.key, lang)

    pass


class LangPackage(OPUnit):
    def __init__(self, user: IUser, lang: str, prev: OPUnit) -> None:
        super().__init__(user)
        self.lang = lang
        self.next = prev
        pass

    pass
#endregion Util

#region Agile
class OP_SeeTaskBoard(OPUnit):
    def __init__(self, user: IUser) -> None:
        super().__init__(user)

        self.Itemlist = iDB.Get(
            "tasks.db", "_TASK", condition='WHERE username = "MarcieM"'
        )
        self.ItemCount = len(self.Itemlist)
        self.CurrentSelection = 0
        OP_SeeTaskBoard.PH_Left = ["L", "l", "left", "LEFT"]
        OP_SeeTaskBoard.PH_Right = ["R", "r", "right", "RIGHT"]
        OP_SeeTaskBoard.PH_Select = [
            "select",
            "s",
            "SELECT",
            "S",
            "YES",
            "y",
            "Y",
            "yes",
        ]
        pass

    def Listen(self, text: str):

        if text[0] in OP_SeeTaskBoard.PH_Left:
            self.CurrentSelection = max(self.CurrentSelection - 1, 0)
            pass
        if text[0] in OP_SeeTaskBoard.PH_Right:
            self.CurrentSelection = min(self.CurrentSelection + 1, self.ItemCount - 1)
            pass
        return super().Listen(text)
        pass

    def Say(self, lang) -> str:

        return ITask(self.Itemlist[self.CurrentSelection]).__str__(lang)
        pass

#endregion Agile

#region List
class OP_List(OPUnit):
    def __init__(self, user: IUser) -> None:
        super().__init__(user)
        OP_List.key='LIST'

        self.TaskList=list[ITask]()
        t=ITask.FindByName(self.user.name)
        for task in t:
            self.TaskList.append(ITask(task))
            pass

        self.AllCompleted=True
        self.UncompletedList=list[ITask]()
        for task in self.TaskList:
            if IsCompleted(task=task):
                self.AllCompleted=False
                self.UncompletedList.append(task)
                pass
            pass
        

        self.alltask=False
        OP_List.PH_ALL=['YES','Y']
        OP_List.PH_NOTDONE=['NO','N']
        OP_List.PH_RIGHT=['RIGHT','R']
        OP_List.PH_LEFT=['LEFT','L']
        self.selection=0
        self.GetListSize()
        pass

    def Listen(self, text: str):

        arg=text[0].upper()
        if arg in OP_List.PH_ALL:
            self.alltask=True
            self.GetListSize()
            self.selection=0
            pass
        if arg in OP_List.PH_NOTDONE:
            self.alltask=False
            self.GetListSize()
            self.selection=0
            pass

        if arg in OP_List.PH_RIGHT:
            self.selection=min(self.selection+1,self.listsize)
            pass
        if arg in OP_List.PH_RIGHT:
            self.selection=max(self.selection-1,0)
            pass



        return super().Listen(text)

    def GetListSize(self):
        k=0
        for t in self.TaskList:
            if self.alltask:
                k+=1
                pass
            elif not IsCompleted(task=t):
                k+=1
                pass
            pass
        self.listsize=k
        pass

    def Say(self, lang) -> str:
        fmt=Text.GetText(OP_List.key,lang)
        
        text=str()

        if self.alltask:
            buf=self.TaskList
            pass 
        else:
            buf=self.UncompletedList
            pass
        
        text+=buf[self.selection].__str__(lang)

        text+=fmt
        return text

    pass


#endregion List
