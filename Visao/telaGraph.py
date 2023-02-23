from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from Data.graph import Graph
from kivy.uix.image import Image
from Visao.recursos.funcoes import Fundo
from kivy.uix.label import Label
from Data.diretorio import controlDiretorio
import numpy as np

class TelaGraph(Screen):
    def __init__(self,voltar:Button,x_values:list,y_values:list,tipo:str,**kw):
        super().__init__(**kw)
        self.rl = RelativeLayout()
        self.ctrDir = controlDiretorio("imagens")
        self.grp = Graph(x_values,y_values)
        telaFundo = Fundo(2000,1000,[1,1,1,1])
        self.title = f"Gŕafico dos dizimistas ({tipo})"
        self.tipo = tipo
        barra = Button(size_hint=(.15, .05),
                                    pos_hint={'center_x': .4, 'center_y': 0.96},
                                    text="Gráfico de barras", on_press=self.barra)

        pizza = Button(size_hint=(.15, .05),
                                    pos_hint={'center_x': .6, 'center_y': 0.96},
                                    text="Gráfico de pizza", on_press=self.pizza)

        total = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .18, 'center_y': .96}, text=f'Total de {tipo}: {np.sum(y_values)}')                                                                 
        self.img = None
        self.showed = False
        self.rl.add_widget(telaFundo)
        self.rl.add_widget(total)
        self.rl.add_widget(barra)
        self.rl.add_widget(pizza)
        self.add_widget(self.rl)
    
    def __refresh(self):
        self.img = Image(source=self.grp.get_filename(),pos_hint={'center_x': .5, 'center_y': .5})
        if self.showed:
            self.rl.remove_widget(self.img)
        self.rl.add_widget(self.img)
    
    def pizza(self,obj):
        self.grp.alterTitle(self.title + " - pizza")
        self.showed = True
        self.ctrDir.delet(self.grp.get_nameFig())
        self.grp.pizza()
        self.__refresh()
    
    def barra(self,obj):
        self.grp.alterTitle(self.title+ " - barra")
        self.showed = True
        self.ctrDir.delet(self.grp.get_nameFig())
        self.grp.barra(self.tipo)
        self.__refresh()
