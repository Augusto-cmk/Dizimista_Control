from Data.data import getData,getHora
class User:
    def __init__(self,nome=None,nomeComunidade=None):
        self.nome = nome
        self.comunidade = nomeComunidade
        self.horaLogin = getHora()
        self.dataLogin = getData()
    
    def __str__(self) -> str:
        return self.getName()

    def setUser(self,nome,nomeComunidade,email):
        self.nome = nome
        self.comunidade = nomeComunidade
        self.email = email

    def getHoraLogin(self):
        return self.horaLogin

    def getDataLogin(self):
        return self.dataLogin

    def getName(self):
        return self.nome

    def getComunidade(self):
        return self.comunidade