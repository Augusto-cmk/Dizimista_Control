from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class ButtonMenu(DropDown):
    def __init__(self,listaNomesBotoes,order=True, **kwargs):
        super().__init__(**kwargs)
        if order:
            listaNomesBotoes = sorted(listaNomesBotoes)
        for nome in listaNomesBotoes:
            btn = Button(text=f'{nome}',size_hint_y = None,height=35)
            btn.bind(on_press= self.Selecao)
            self.add_widget(btn)


    def Selecao(self,obj):
        self.select(obj.text)


class Menu(Button):
    def __init__(self,nomeBotao,dic_posicao,size_hint,listaNomesBotoes,order=True, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = size_hint
        self.listaPaginas = ButtonMenu(listaNomesBotoes,order=order)
        self.pos_hint = dic_posicao
        self.text = nomeBotao
        self.bind(on_release=self.listaPaginas.open)
        self.listaPaginas.bind(on_select=lambda instance,x : setattr(self,'text',x))