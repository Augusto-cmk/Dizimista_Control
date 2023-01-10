from Data.data import getData,getHora
class User:
    def __init__(self,nome=None,pagina=None,email=None):
        self.nome = nome
        self.comunidade = pagina
        self.email = email
        self.horaLogin = getHora()
        self.dataLogin = getData()

    def setUser(self,nome,pagina,email):
        self.nome = nome
        self.comunidade = pagina
        self.email = email

    def getHoraLogin(self):
        return self.horaLogin

    def getDataLogin(self):
        return self.dataLogin

    def getName(self):
        return self.nome

    def getComunidade(self):
        return self.comunidade

    def getEmail(self):
        return self.email