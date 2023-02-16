import socket
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox


def obterIP():
    return socket.gethostbyname(socket.gethostname())

def remvDofim(string):
    str = string.split()
    strOut = ''

    for i in range(len(str)):
        strOut += str[i]
        if i != len(str) - 1:
            strOut += ' '


    return strOut

def verificaIntegridadeSenha(senha):
    if len(senha) < 8:
        return 'tamanho'

    else:
        qtdLetrasMaiusculas = 0
        qtdLetras = 0
        qtdNumeros = 0
        for char in senha:
            if (char != "9" and char !="8" and char !="7" and char !="6" and
            char !="5" and char != "4" and char !="3" and char !="2" and char !="1" and char !="0"):
                if (char == char.upper()):
                    qtdLetrasMaiusculas +=1
                qtdLetras +=1
            else:
                qtdNumeros += 1

        if qtdLetrasMaiusculas == 0 and qtdLetras > 0:
            return 'maiuscula'

        elif qtdNumeros == 0:
            return 'numero'

        elif qtdLetras == 0:
            return 'letra'
        else:
            return True

class checkboxList(list):
    def __init__(self,pos_x,pos_y,listaNomes):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.ativados = list()
        for nome in listaNomes:
            self.inserir(nome)

    def inserir(self,string):
        pos = self.pos_y - len(self)/50
        self.append(Label(pos_hint={'center_x': self.pos_x-0.3, 'center_y': pos}, text=string))
        check = CheckBox(pos_hint={'center_x': self.pos_x, 'center_y': pos})
        check.bind(active=self.ativo)
        self.append(check)

    def ativo(self,checkbox,value):
        for i in range(len(self)):
            if checkbox == self[i] and value:
                self.ativados.append(self[i-1].text)

            elif checkbox == self[i] and value == False and self[i-1].text in self.ativados:
                j = 0
                for nome in self.ativados:
                    if nome == self[i-1].text:
                        del(self.ativados[j])
                    j+=1

    def getNomesAtivos(self):
        return self.ativados


class checkboxListUniqueMark(list): #Ao marcar um checkbox, os demais devem ser desmarcados
    def __init__(self,pos_x,pos_y,listaNomes):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.ativado = None
        self.checkboxActive = [None]
        for nome in listaNomes:
            self.inserir(nome)

    def inserir(self,string):
        pos = self.pos_y - len(self)/50
        self.append(Label(pos_hint={'center_x': self.pos_x-0.3, 'center_y': pos}, text=string))
        check = CheckBox(pos_hint={'center_x': self.pos_x, 'center_y': pos})
        check.bind(active=self.ativo)
        self.append(check)

    def ativo(self,checkbox,value):
        if value != False and checkbox != self.checkboxActive[0]:
            self.__desative()
            for i in range(len(self)):
                if checkbox == self[i] and value:
                    self.ativado = self[i-1].text
                    self.checkboxActive[0] = checkbox
                    break
        elif value == False and checkbox == self.checkboxActive[0]:
            self.ativado = None


    
    def __desative(self):
        if self.checkboxActive[0] != None:
            self.checkboxActive[0].state = 'normal'


    def getNomesAtivos(self):
        return self.ativado