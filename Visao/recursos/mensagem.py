from kivy.uix.label import Label

class Mensagem(Label):
    def __init__(self,error=False,sucesso=False,**kwargs):
        super().__init__(**kwargs)
        if error:
            self.color = 'red'

        if sucesso:
            self.color = 'green'

        self.size_hint = (.2, .05)
        self.active = False

    def addMensagem(self,mensagemError,pos_hint):
        self.text = mensagemError
        self.pos_hint = pos_hint
        self.active = True

    def setStatus(self,boolean):
        self.active = boolean

    def getStatus(self):
        return self.active