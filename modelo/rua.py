class Rua:
    def __init__(self,nomeRua:str,zelador:str):
        self.nomeRua = nomeRua
        self.zelador = zelador
    
    def __str__(self) -> str:
        return self.nomeRua
    
    def getNomeRua(self)->str:
        return self.nomeRua

    def getZelador(self)->str:
        return self.zelador
