from os import name
from Android.IUser import IUser
import sqlite3
import Text

def DBDef():
    conn = sqlite3.connect("tasks.db")

    c = conn.cursor()
    c.execute('''
    CREATE TABLE _TASK
    (
        taskname text PRIMARY KEY,
        username integer,
        description text,
        state text,
        message text,
        start date,
        end date
    )
    ''')
    pass


class ITask:


    def __init__(self,d=None) -> None:
        ITask.key='TASKUNIT'


        if d==None:
            self.taskname='null'
            self.username='null'
            self.desc='null'
            self.state='null'
            self.message='null'
            self.start=sqlite3.Date(1,1,1)
            self.end=sqlite3.Date(1,1,1)
            pass
        else:            
            self.taskname=str(d[0])
            self.username=str(d[1])
            self.desc=str(d[2])
            self.state=str(d[3])
            self.message=str(d[4])

            convert=lambda c:sqlite3.Date(year=int(c[0]),month=int(c[1]),day=int(c[2]))

            buf=str(d[5]).split('-')
            self.start=convert(buf)
            
            buf=str(d[6]).split('-')
            self.end=convert(buf)
                
        pass
    
    
    def __str__(self,lang:str=None) -> str:


     
        #taskname 
        #username 
        #state
        #deadline
        #days until deadline

        #desc
        if lang==None:
            fmt=str(Text.GetText(ITask.key,'en'))
            daystil=self.end-sqlite3.Date.today()
            buf= fmt.format(self.taskname,self.username,self.state,self.end,daystil.days,self.desc)
            buf+='\n, No Language specified'
            return buf
            pass
        else:
            fmt=str(Text.GetText(ITask.key,lang))
            daystil=self.end-sqlite3.Date.today()
            buf= fmt.format(self.taskname,self.username,self.state,self.end,daystil.days,self.desc)
            return buf
            pass
        pass

    @staticmethod
    def UpdateTask(taskname,username=None,desc=None,state=None,message=None,start:sqlite3.Date=None,end:sqlite3.Date=None):
        conn = sqlite3.connect("tasks.db")

        c = conn.cursor()
        items=list[str]()
        if username!=None:
            items.append('''username="{}"'''.format(username))
            pass
        if desc!=None:
            items.append('''description="{}"'''.format(desc))
            pass
        if state!=None:
            items.append('''state="{}"'''.format(state))
            pass
        if message!=None:
            items.append('''message="{}"'''.format(message))
            pass
        if start!=None:
            items.append('''start="{}"'''.format(start))
            pass
        if end!=None:
            items.append('''state="{}"'''.format(end))
            pass
        condition=str()
        if len(items)==1:
            condition=items[0]
            pass
        else:
            for a in range(0,len(items)):
                condition+=items[a]
                if (a<len(items)-1):
                    condition+=','
                    pass
                pass    

        q='''
        UPDATE _TASK
        SET {0}
        WHERE taskname = "{1}"
        '''.format(items,taskname)
        q=q.replace('\n',' ')
        q=q.replace('[',' ')
        q=q.replace(']',' ')
        q=q.replace("'",' ')

        c.execute(q)
        conn.commit()
        pass


    @staticmethod
    def FindByName(username):
        conn = sqlite3.connect("tasks.db")

        c = conn.cursor()
        
        q='''
        SELECT * FROM _TASK WHERE username = '{}'
        '''.format(username.replace(' ',''))

        c.execute(q)

        return c.fetchall()

        pass

    pass


    @staticmethod
    def AddTask(t)->list:
        conn = sqlite3.connect("tasks.db")

        c = conn.cursor()

        q='''
       INSERT INTO _TASK VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
        '''.format(t.taskname,t.username,t.desc,t.state,t.message,t.start,t.end)
        c.execute(q)
        conn.commit()

        pass
    
    @staticmethod
    def GetActiveTask(name):
        conn=sqlite3.connect('tasks.db')
        c=conn.cursor()

        q='''
        SELECT * FROM _TASK
        WHERE state != 'DONE' and username = '{0}' and start < '{1}' 
        '''.format(name,sqlite3.Date.today())
        c.execute(q)
        res=list[ITask]()
        tasks=c.fetchall()
        if len(tasks)>0:
            for t in tasks:
                res.append(ITask(t))
                pass
            pass

        return res

def IsCompleted(taskname:str=None,task:ITask=None):

    complete=['DONE','done','完','完了']

    conn = sqlite3.connect("tasks.db")

    c = conn.cursor()
    
    if taskname!=None:
        name=taskname
        pass
    else:
        name=task.taskname
        pass

    q='''
    SELECT * FROM _TASK WHERE taskname = '{}'
    '''.format(name.replace(' ',''))

    c.execute(q)
    t:ITask=ITask(c.fetchone())
    
    return t.state in complete 
    pass

def FindTaskByTaskName(taskname)->ITask:
    conn = sqlite3.connect("tasks.db")

    c = conn.cursor()
        
    q='''
    SELECT * FROM _TASK WHERE taskname = '{}'
    '''.format(taskname.replace(' ',''))

    c.execute(q)

    return ITask(c.fetchone())

    pass
pass


