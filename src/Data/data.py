from datetime import datetime


def getHora():
    data = datetime.now()
    return data.strftime('%H:%M')

def getData():
    data = datetime.now()
    return data.strftime('%d/%m/%Y')

def getMes():
    meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
    data = datetime.now()
    return meses[data.month-1]

def getAno():
    data = datetime.now()
    return str(data.year)