from datetime import datetime


def getHora():
    data = datetime.now()
    return data.strftime('%H:%M')

def getData():
    data = datetime.now()
    return data.strftime('%d/%m/%Y')

def getMes():
    data = datetime.now()
    return data.month