import sqlite3




def GetText(key,lang)->str:
    conn=sqlite3.connect('Texts.db')
    c=conn.cursor()
    q='''
    SELECT * FROM _TEXTS 
    WHERE key = ('{}') AND lang = ('{}')
    '''.format(key,lang[0].replace("'",""))

    c.execute(q)

    buf=c.fetchone()
    if buf==None:

        q='''
        SELECT * FROM _TEXTS 
        WHERE key = ('{}') AND lang = ('{}')
            '''.format(key,'jp')

        c.execute(q)
        buf=c.fetchone()

        pass

    text=str(buf[2])

    text=text.replace('\r\n','\n')
    text=text.replace('\t','')
    return text

    pass


def add():
    conn=sqlite3.connect('Texts.db')
    c=conn.cursor()

    q="""
    INSERT INTO _TEXTS VALUES ('{}','{}','{}')
    """.format('LIST','jp','CREATE')
    c.execute(q)

    conn.commit()
    pass
