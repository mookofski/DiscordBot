import sqlite3

def Translate_OpId(Name,C):
    n=Name.upper()
    C.execute('SELECT id FROM _OPERATION_LIST WHERE name = (?)',(n,))
    l =C.fetchall()
    if(len(l)==0):
        return 0
    return l[0]

