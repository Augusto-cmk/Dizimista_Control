from src.Data.database import BancodeDados_cadastro

class Cadastro:
    def __init__(self) -> None:
        self.db = BancodeDados_cadastro()
        self.db.criar()
    
    def cadastrar(self,email:str,nome:str,login:str,senha:str,nomeComunidade:str)->bool:
        return self.db.inserirCadastro(email,login,senha,nome,nomeComunidade)
    
    def login(self,login:str,senha:str):
        user = self.db.login(login,senha)
        if user:
            return user.__dict__()
        else:
            return False
    
    def recuperaSenha(self,email:str):
        return self.db.recuperar_senha(email)

