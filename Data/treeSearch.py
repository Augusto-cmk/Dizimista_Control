from unidecode import unidecode

class word:
    def __init__(self,palavra:str):
        self.palavra = palavra
    
    def __str__(self):
        return self.palavra

    def menorQue(self,palavra):
        lettersA = unidecode(self.palavra).lower()
        lettersB = unidecode(palavra).lower()
        if len(lettersA) < len(lettersB):
            for i,letter in enumerate(lettersA):
                if letter < lettersB[i]:
                    return True
                elif letter > lettersB[i]:
                    return False
        else:
            for i,letter in enumerate(lettersB):
                if letter < lettersA[i]:
                    return False
                elif letter > lettersA[i]:
                    return True
    def casa(self,key:str):
        lettersK = unidecode(key).lower()
        letters = unidecode(self.palavra).lower()
        if len(lettersK) <= len(letters):
            casamentos = 0
            for i,letter in enumerate(lettersK):
                if letter == letters[i]:
                    casamentos+=1
            return casamentos == len(lettersK)
        else:
            return False
              
class node:
    def __init__(self,input:str):
        self.atributo = word(input)
        self.left = None
        self.right = None
    def __str__(self):
        return str(self.atributo)
    def get(self):
        return self.atributo

class S_tree:
    def __init__(self):
        self.root = None
        self.qtdElements = 0
    
    def addList(self,lista:list):
        for palavra in lista:
            self.add(palavra)

    def add(self,letter):
        self.qtdElements+=1
        self.root = self.insert(self.root,letter)
    
    def insert(self,no:node,letter:str):
        if(not no):
            return node(letter)
        else:
            if no.get().menorQue(letter):
                no.right = self.insert(no.right,letter)
            else:
                no.left = self.insert(no.left,letter)
            return no
        
    def obterCorrespondencias(self,key):
        lista = list()
        self.get(self.root,key,lista)
        return lista

    def get(self,no:node,key,lista:list):
        if no:
            self.get(no.left,key,lista)
            if no.atributo.casa(key):
                lista.append(str(no))
            self.get(no.right,key,lista)

    def imprimir(self):
        self.print(self.root)

    def print(self,no):
        if no:
            self.print(no.left)
            print(f"{no} ")
            self.print(no.right)

    def size(self):
        return self.qtdElements
