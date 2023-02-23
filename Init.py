from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Visao.Interfaces import TelaLogin
from Data.user import User
import numpy as np
from Visao.telaGraph import TelaGraph

class GerenciadorTelas(ScreenManager):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(TelaGraph(None,['carros','Motos','ônibus','Caminhões'],[40,30,15,20],"Contribuintes"))


class Programa(App):

    def build(self):
        return GerenciadorTelas()

Programa().run()