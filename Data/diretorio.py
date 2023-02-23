import os
class controlDiretorio:
    def __init__(self,diretorioName:str) -> None:
        self.dir = os.listdir(diretorioName)
        self.nome = diretorioName

    def delet(self,fileName:str):
        arquivo = f"{self.nome}/{fileName}"
        for file in self.dir:
            if file == fileName:
                os.remove(arquivo)
                break