from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Visao.Interfaces import TelaLogin
from Data.user import User
import numpy as np

class GerenciadorTelas(ScreenManager):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(TelaLogin())


class Programa(App):

    def build(self):
        return GerenciadorTelas()

Programa().run()