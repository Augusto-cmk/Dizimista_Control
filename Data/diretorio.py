import os
class controlDiretorio:
    def __init__(self,diretorioName:str) -> None:
        self.dir = os.listdir(diretorioName)
        self.nome = diretorioName

    def __refresh(self):
        self.dir = os.listdir(self.nome)

    def delet(self,fileName:str):
        self.__refresh()
        arquivo = f"{self.nome}/{fileName}"
        for file in self.dir:
            if file == fileName:
                os.remove(arquivo)
                break