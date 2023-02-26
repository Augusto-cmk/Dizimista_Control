import matplotlib.pyplot as plt
import numpy as np
from random import randint

def absolut(percent:float,y_values:list):
    absoluto = int(percent/100.*np.sum(y_values))
    return "{:.1f}%\n({:d})".format(percent,absoluto)

def nomeAleatorio():
    return str(randint(1,10000000))


class Graph:
    def __init__(self,x_values:list,y_values:list,title:str = None) -> None:
        self.x = x_values
        self.y = y_values
        self.nameFig = None
        self.filename = None
        self.title = title

    def alterTitle(self,newTitle:str):
        self.title = newTitle
    
    def __alterFilename(self):
        self.filename = f'imagens/{self.nameFig}'

    def pizza(self):
        plt.close()
        self.nameFig = f"{nomeAleatorio()}.png"
        self.__alterFilename()
        plt.subplots(subplot_kw=dict(aspect='equal'))
        wedgets,_,_ = plt.pie(self.y,autopct=lambda x: absolut(x,self.y),textprops=dict(color='w'))
        plt.legend(wedgets,self.x,loc='center left',bbox_to_anchor=(0.9,0,0.5,1),fontsize=10)
        if self.title:
            plt.title(self.title)
        plt.gcf().savefig(self.filename,format='png')
        plt.close()
    
    def barra(self,tipo:str):
        plt.close()
        self.nameFig = f"{nomeAleatorio()}.png"
        self.__alterFilename()
        plt.bar(self.x,self.y,color='blue')
        plt.xticks(self.x)
        plt.ylabel("Quantidade")
        plt.xlabel(tipo)
        if self.title:
            plt.title(self.title)
        plt.gcf().savefig(self.filename,format='png')
        plt.close()

    def get_filename(self):
        return self.filename
    
    def get_nameFig(self):
        return self.nameFig