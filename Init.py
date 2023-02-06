from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Visao.LoginCadastro import TelaLogin
from Visao.Main import TelaPrincipal
from Data.user import User

class GerenciadorTelas(ScreenManager):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        # self.add_widget(TelaLogin())
        self.add_widget(TelaPrincipal(User("Pedro")))


class Programa(App):

    def build(self):
        return GerenciadorTelas()

Programa().run()