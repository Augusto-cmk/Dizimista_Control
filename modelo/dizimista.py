class dizimista:
    def __init__(self,nome:str,rua:str,nCasa:str,aniversario:str=None):
        self.rua = rua
        self.nome = nome
        self.nCasa = nCasa
        self.aniversario = aniversario
    
    def __str__(self)->str:
        return self.nome
    
    def getNome(self)->str:
        return self.nome
    
    def getRua(self)->str:
        return self.rua
    
    def getNCasa(self)->str:
        return self.nCasa
    
    def getAniversario(self)->str:
        return self.aniversario
    


    
