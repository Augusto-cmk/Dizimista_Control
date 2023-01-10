from Data.database import BancodeDados
class Rua:
    def __init__(self,nomeRua:str,data:BancodeDados):
        self.nome = nomeRua
        self.database = data
    
    def __str__(self) -> str:
        return self.nome