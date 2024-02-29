from src.Data.data import getData,getHora
class User:
    def __init__(self,nome,nomeComunidade,email,login,senha):
        self.nome:str = nome
        self.comunidade:str = nomeComunidade
        self.email = email
        self.login = login
        self.senha = senha
    
    def __str__(self) -> str:
        return self.nome

    def __dict__(self)->dict:
        return {
            "nome":self.nome,
            "comunidade":self.comunidade,
            "email":self.email,
            "login":self.login,
            "senha":self.senha
        }