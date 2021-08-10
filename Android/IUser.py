import sqlite3
import Text
import discord


class IUser:
    def __init__(self):
        self.id = -1
        self.name = "undefined"
        IUser.key='USER_DESC'
        pass
    def __init__(self,usr:discord.User):
        self.id = usr.id
        self.name = usr.name
        IUser.key='USER_DESC'
        pass
    def __init__(self, Id, Name):
        self.id = Id
        self.name = Name
        IUser.key='USER_DESC'
        pass

    @staticmethod
    def GetUser(user, c):
        q = "SELECT id FROM _USERS WHERE id = '{}'".format(user.id)
        c.execute(q)
        usr = c.fetchall()
        if len(usr) > 0:
            return IUser(usr[0], usr[1])
        else:
            return IUser()
        pass

    @staticmethod
    def MakeList(val):
        l = list()

        for id, name in val:
            l.append(IUser(id, name))
            pass
        return l

        pass  # func end

    @staticmethod
    def AddUnique(user:discord.user.User):
        
        conn = sqlite3.connect("tasks.db")

        c = conn.cursor()

        q = "SELECT id FROM _USERS WHERE id = '{}'".format(user.id)
        c.execute(q)
        # print(c.fetchall())
        if len(c.fetchall()) < 1:
            c.execute(
                """
		INSERT INTO _USERS VALUES(?,?)
		""",
                (user.id, user.name),
            )
            conn.commit()
            return True
        else:
            return False
        pass

        pass

    pass  # class end

    @staticmethod
    def GetAllUserList():

        fmt=Text.GetText('USER_DESC','jp')

        conn =sqlite3.connect('tasks.db')

        c=conn.cursor()

        #get all users
        q='''
        SELECT name FROM _USERS
        '''
        c.execute(q)
        UserList=str()
        UserList=c.fetchall()

        #get all task
        q='''
        SELECT username FROM _TASK
        '''
        tasklist=str()
        tasklist=c.execute(q).fetchall()

        output=str()

        for names in UserList:
            output+=(fmt.format(names[0].replace(',',''),tasklist.count(names)))
            pass
        return output
        pass

    @staticmethod
    def GetAllUser()->list:
        conn = sqlite3.connect("tasks.db")

        c = conn.cursor()

        c.execute('''
        SELECT * FROM _USERS
        ''')
        l=list()
        ulist=c.fetchall()
        
        if len(ulist)>0:

            for users in ulist:

                print (users)
                l.append(IUser(int(users[0]),str(users[1])))
                pass
            return l
        else:
            return IUser()
        pass

    @staticmethod
    def GetUserByName(name:str):
        conn = sqlite3.connect("tasks.db")

        c = conn.cursor()
        q='''
        SELECT * FROM _USERS WHERE name = "{}"'''.format(name)
        c.execute(q)
        buf=c.fetchone()
        return IUser(buf[0],buf[1])
        

        pass
      
    @staticmethod
    def GetAllUserName()->list[str]:
        conn = sqlite3.connect("tasks.db")

        c = conn.cursor()

        c.execute('''
        SELECT name FROM _USERS
        ''')
        l=list[str]()
        ulist=c.fetchall()
        
        if len(ulist)>0:

            for name in ulist:
                buf=str(name)
                buf=buf.replace(',','')

                l.append(buf)
                pass

            return l
        else:
            return 'null'
        pass


    @staticmethod
    def isAdmin(user):
        conn = sqlite3.connect("tasks.db")

        c = conn.cursor()

        q='''
        SELECT admin FROM _USERS
        WHERE id = '{}'
        '''.format(user.id)

        c.execute(q)
      #  res=c.fetchone()
        return c.fetchone()

        pass

