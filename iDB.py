import sqlite3


class iDB:

    @staticmethod
    def Get(db:str,table:str,items:list[str]=None,condition:list[str]=None):
        conn=sqlite3.connect(db)
        c=sqlite3.Cursor
        c=conn.cursor()

        q_item=str()
        
        if type(items)!=type(None):
            itemlength=len(items)
            

            if itemlength==1:#if only one, dont add ,
                q_item=items[0]
                pass
            else:
                for i in range(0,itemlength):#loop and append , except for last one
                    q_item+=items[i]
                    if i<itemlength-1:
                        q_item+=','
                        pass#last one check
                    pass#loop
                pass#if nest ned
            #endregion
        else:
            q_item='*'
            pass
        q_condition=' '
        if type(condition) != type(None):
            for a in condition:
                q_condition+=a
                pass
            pass
        q='''SELECT {0} FROM {1} {2}
        '''.format(q_item,table,q_condition)
        q=q.replace('\n','')
        c.execute(q)
        return c.fetchall()
        pass
    pass

