from kivy.uix.screenmanager import Screen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from Data.graph import Graph
from kivy.uix.image import Image
from Visao.recursos.funcoes import Fundo
from kivy.uix.label import Label
from Data.diretorio import controlDiretorio
import numpy as np
from Data.user import User
from Data.database import BancodeDados
from Data.data import *
from Visao.recursos.botoesAuxiliares import Menu
import time

class TelaGraph(Screen): ## Selecionar a rua, clicar em visualizar e depois mostrar uma comparação entre contribuintes e não contribuintes
                         ## O label com o total vai mostrar o total de todos os dizimistas
    def __init__(self,voltar:Button,user:User,**kw):
        super().__init__(**kw)
        self.rl = RelativeLayout()
        self.x_values = ["Contribuiu","Não contribuiu"]
        self.db = BancodeDados(user.getComunidade())
        self.ctrDir = controlDiretorio("imagens")
        self.grp = None
        telaFundo = Fundo(2000,1000,[1,1,1,1])
        self.title = None
        self.rua = None
        barra = Button(size_hint=(.15, .05),
                                    pos_hint={'center_x': .47, 'center_y': 0.96},
                                    text="Gráfico de barras", on_press=self.barra)

        pizza = Button(size_hint=(.15, .05),
                                    pos_hint={'center_x': .62, 'center_y': 0.96},
                                    text="Gráfico de pizza", on_press=self.pizza)

        self.menuMes = Menu(getMes(), {'center_x': .77, 'center_y': 0.96}, (.15, .05),
                            ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"],order=False)

        self.menuAno = Menu(getAno(), {'center_x': .92, 'center_y': 0.96}, (.15, .05),self.db.anosDisponiveis())

        self.namesFig = list()
        self.img = None
        self.showed = False
        self.rl.add_widget(telaFundo)
        self.rl.add_widget(voltar)
        self.rl.add_widget(barra)
        self.rl.add_widget(pizza)
        self.rl.add_widget(self.menuMes)
        self.rl.add_widget(self.menuAno)
        self.add_widget(self.rl)

    
    def __refresh(self):
        self.showed = True
        self.rl.add_widget(self.img)
    
    def insertData(self,rua:str):
        self.rua = rua
        self.namesFig = list()
        self.totalDizimistas = len(self.db.dizimistasRua(rua))

        self.title = f"Contribuintes X Não contribuintes ({rua})"
        total = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .25, 'center_y': .96}, text=f'Total de dizimistas: {self.totalDizimistas}')
        self.rl.add_widget(total)

    def pizza(self,obj):
        contribuintes = len(self.db.ContribuintesRua(self.menuMes.text,self.menuAno.text,self.rua))
        y_values = [contribuintes,abs(self.totalDizimistas - contribuintes)]

        self.grp = Graph(self.x_values,y_values)

        if np.sum(self.grp.y) != 0:
            self.grp.alterTitle(self.title + " - pizza")
            self.grp.pizza()
            self.namesFig.append(self.grp.get_nameFig())
            if self.showed:
                self.rl.remove_widget(self.img)
            self.img = Image(source=self.grp.get_filename(),pos_hint={'center_x': .5, 'center_y': .5})
            self.__refresh()
    
    def barra(self,obj):
        contribuintes = len(self.db.ContribuintesRua(self.menuMes.text,self.menuAno.text,self.rua))
        y_values = [contribuintes,abs(self.totalDizimistas - contribuintes)]

        self.grp = Graph(self.x_values,y_values)

        self.grp.alterTitle(self.title+ " - barra")
        self.grp.barra(self.rua)
        self.namesFig.append(self.grp.get_nameFig())
        if self.showed:
            self.rl.remove_widget(self.img)
        self.img = Image(source=self.grp.get_filename(),pos_hint={'center_x': .5, 'center_y': .5})
        self.__refresh()
    
    def get_namesFig(self):
        return self.namesFig
