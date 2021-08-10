


#YYYY-MM-DD HH:MM:SS.SSS
def ConverttoDate(m,d):
    txt=str()
    month=str()
    date=str()
    if(m<10):
        month+='0{}'.format(m)
    else:
        month+='{}'.format(m)

    if(d<10):
        date+='0{}'.format(d)
    else:
        date+='{}'.format(d)

    return '2021-{}-{} 12-00-00'.format(month,date)
    pass

