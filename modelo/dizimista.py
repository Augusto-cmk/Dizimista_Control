from Data.database import BancodeDados
import datetime
class dizimista:
    def __init__(self,nome:str,rua:str,nCasa:str,data:BancodeDados)->bool:
        info = data.getDizimista(nome,rua,nCasa)
        if info:
            self.nome = info[1]
            self.nCasa = info[2]
            self.aniversario = datetime.strptime(info[3], '%d/%m/%Y').date()
            self.rua = info[4]
            self.database = data
            return True
        else:
            return False

    
    def __str__(self)->str:
        return self.nome
    


    
