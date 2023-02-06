from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.checkbox import CheckBox
from Visao.recursos.mensagem import Mensagem
from kivy.uix.screenmanager import Screen
from Data.conexao import test_conexao
from Visao.recursos.funcoes import remvDofim,verificaIntegridadeSenha,obterIP,checkboxList
from Visao.recursos.botoesAuxiliares import Menu
from Data.send import envioEmail,gerarNumero
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle,Color
from kivy.uix.gridlayout import GridLayout
from Data.data import getData,getHora,getMes
from Data.database import BancodeDados_cadastro


class Fundo(Widget):
    def __init__(self,tam_x,tam_y,cor,pos_x=None,pos_y=None, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(cor[0],cor[1],cor[2],cor[3])
            if pos_x == None and pos_y == None:
                self.rect = Rectangle(size=[tam_x,tam_y])
            else:
                self.rect = Rectangle(size=[tam_x, tam_y],pos=(pos_x,pos_y))


class TelaLogin(Screen):
    def __init__(self,mensagem=None, **kw):
        super().__init__(**kw)

        self.db = BancodeDados_cadastro()
        self.db.criar()

        self.user = None

        self.rl = RelativeLayout(size=(300, 300))


        self.mensagemError = Mensagem(error=True)

        exibirsenha = CheckBox(color='black',size_hint=(.01, .01), pos_hint={'center_x': .62, 'center_y': .42})

        labelExibirSenha = Label(color='black',size_hint=(.2, .05),
                                    pos_hint={'center_x': .7, 'center_y': .42}, text='Exibir senha')

        exibirsenha.bind(active=self.exibirSenha)

        labelLogin = Label(color='black',size_hint=(.2, .05),
                            pos_hint={'center_x': .36, 'center_y': .5}, text='Login')

        labelSenha = Label(color='black',size_hint=(.2, .05),
                            pos_hint={'center_x': .36, 'center_y': .42}, text='Senha')

        self.login = TextInput(size_hint=(.2, .05),
                                pos_hint={'center_x': .5, 'center_y': .5}, multiline=False)

        self.senha = TextInput(size_hint=(.2, .05),
                                pos_hint={'center_x': .5, 'center_y': .42}, multiline=False, password=True)

        imagem = Image(source='imagens/dizimo2.jpg',pos_hint={'center_x': .5, 'center_y': .5})

        entrar = Button(size_hint=(.09, .05),
                        pos_hint={'center_x': .35, 'center_y': .3},
                        text="Entrar", on_press=self.entrar)

        criarNovoCadastro = Button(size_hint=(.15, .05),
                                    pos_hint={'center_x': .48, 'center_y': .3},
                                    text="Novo Cadastro", on_press=self.criarCadastro)

        self.mensagemSucesso = mensagem

        if mensagem != None:
            self.rl.add_widget(self.mensagemSucesso)

        self.rl.add_widget(imagem)
        self.rl.add_widget(labelExibirSenha)
        self.rl.add_widget(exibirsenha)
        self.rl.add_widget(criarNovoCadastro)
        self.rl.add_widget(labelSenha)
        self.rl.add_widget(labelLogin)
        self.rl.add_widget(self.login)
        self.rl.add_widget(self.senha)
        self.rl.add_widget(entrar)
        self.add_widget(self.rl)


    def exibirSenha(self,checkbox,value):
        if value:
            self.senha.password = False
        else:
            self.senha.password = True

    def criarCadastro(self,obj):
        self.clear_widgets()
        self.add_widget(TelaCadastro())

    def entrar(self,obj):
        self.login.text = remvDofim(self.login.text)
        self.senha.text = remvDofim(self.senha.text)

        if self.mensagemSucesso != None and self.mensagemSucesso.getStatus() != False:
            self.rl.remove_widget(self.mensagemSucesso)
        
        if self.db.login(self.login.text,self.senha.text) == None:
                if self.mensagemError.getStatus() == False:
                    self.mensagemError.addMensagem("Login ou senha invalidos",
                                                   {'center_x': .5, 'center_y': .2})
                    self.rl.add_widget(self.mensagemError)
                else:
                    self.mensagemError.addMensagem("Login ou senha invalidos",
                                                   {'center_x': .5, 'center_y': .2})
        else:
            self.clear_widgets()
            self.add_widget()



class TelaCadastro(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        self.db = BancodeDados_cadastro()
        self.db.criar()

        self.mensagemError = Mensagem(error=True)

        self.rl = RelativeLayout(size=(300, 300))

        telaFundo = Fundo(2000,1000,[0.98,0.98,0.98,0.98])
        
        self.textCriarComunidade = TextInput(size_hint=(.2, .05),
                           pos_hint={'center_x': .5, 'center_y': .34}, multiline=False,text='Nome da comunidade')
        labelCriarComunidade = Label(color='black',size_hint=(.2, .05),
                           pos_hint={'center_x': .32, 'center_y': .34}, text='Nova comunidade')

        exibirsenhas = CheckBox(color='black',size_hint=(.1, .1), pos_hint={'center_x': .62, 'center_y': .41})
        exibirsenhas.bind(active=self.exibirSenhas)

        labelExibirSenha = Label(color='black',size_hint=(.2, .05),
                                 pos_hint={'center_x': .7, 'center_y': .41}, text='Exibir senhas')

        self.novoLogin = TextInput(size_hint=(.2, .05),
                  pos_hint={'center_x': .5, 'center_y': .56}, multiline=False)

        self.nome = TextInput(size_hint=(.2, .05),
                  pos_hint={'center_x': .5, 'center_y': .64}, multiline=False)

        labelNome = Label(color='black',size_hint=(.2, .05),
                                 pos_hint={'center_x': .35, 'center_y': .64}, text='Nome')

        imagem = Image(source='imagens/imagemTelaCadastro.jpg', pos_hint={'center_x': .5, 'center_y': .5})

        self.senha1 = TextInput(size_hint=(.2, .05),
                  pos_hint={'center_x': .5, 'center_y': .48}, multiline=False,password = True)

        self.senha2 = TextInput(size_hint=(.2, .05),
                           pos_hint={'center_x': .5, 'center_y': .41}, multiline=False,password = True)

        labelSenha1 = Label(color='black',size_hint=(.2, .05),
                           pos_hint={'center_x': .35, 'center_y': .48}, text='Senha')

        labelSenha2 = Label(color='black',size_hint=(.2, .05),
                           pos_hint={'center_x': .325, 'center_y': .41}, text='Confirmar senha')

        labelNovoLogin = Label(color='black',size_hint=(.2, .05),
                           pos_hint={'center_x': .35, 'center_y': .56}, text='Login')

        Cadastrar = Button(size_hint=(.1, .05),
                        pos_hint={'center_x': .44, 'center_y': .27},
                        text="Cadastrar", on_press=self.cadastrar)

        Voltar = Button(size_hint=(.09, .05),
                        pos_hint={'center_x': .55, 'center_y': .27},
                        text="Voltar", on_press=self.voltar)

        self.rl.add_widget(telaFundo)
        self.rl.add_widget(imagem)
        self.rl.add_widget(self.nome)
        self.rl.add_widget(labelNome)
        self.rl.add_widget(labelCriarComunidade)
        self.rl.add_widget(exibirsenhas)
        self.rl.add_widget(labelExibirSenha)
        self.rl.add_widget(labelSenha2)
        self.rl.add_widget(self.senha2)
        self.rl.add_widget(labelSenha1)
        self.rl.add_widget(self.senha1)
        self.rl.add_widget(self.novoLogin)
        self.rl.add_widget(labelNovoLogin)
        self.rl.add_widget(self.textCriarComunidade)
        self.rl.add_widget(Voltar)
        self.rl.add_widget(Cadastrar)
        self.add_widget(self.rl)


    def cadastrar(self,obj):
    
        self.senha1.text = remvDofim(self.senha1.text)
        self.senha2.text = remvDofim(self.senha2.text)
        self.novoLogin.text = remvDofim(self.novoLogin.text)
        self.nome.text = remvDofim(self.nome.text)
        if self.novoLogin.text == '':
            if self.mensagemError.getStatus() == False:
                self.mensagemError.addMensagem("O campo de login precisa ser preenchido",
                                                {'center_x': .5, 'center_y': .2})
                self.rl.add_widget(self.mensagemError)
            else:
                self.mensagemError.addMensagem("O campo de login precisa ser preenchido",
                                                {'center_x': .5, 'center_y': .2})
            return

        elif self.senha1.text == '':
            if self.mensagemError.getStatus() == False:
                self.mensagemError.addMensagem("O campo de senha precisa ser preenchido",
                                                {'center_x': .5, 'center_y': .2})
                self.rl.add_widget(self.mensagemError)
            else:
                self.mensagemError.addMensagem("O campo de senha precisa ser preenchido",
                                                {'center_x': .5, 'center_y': .2})
            return
        elif self.senha2.text == '':
            if self.mensagemError.getStatus() == False:
                self.mensagemError.addMensagem("É necessario confirmar a senha",
                                                {'center_x': .5, 'center_y': .2})
                self.rl.add_widget(self.mensagemError)
            else:
                self.mensagemError.addMensagem("É necessario confirmar a senha",
                                                {'center_x': .5, 'center_y': .2})
            return

        elif self.nome.text == '':
            if self.mensagemError.getStatus() == False:
                self.mensagemError.addMensagem("É necessario adicionar um nome",
                                                {'center_x': .5, 'center_y': .2})
                self.rl.add_widget(self.mensagemError)
            else:
                self.mensagemError.addMensagem("É necessario adicionar um nome",
                                                {'center_x': .5, 'center_y': .2})
            return
        elif self.senha1.text != self.senha2.text:
            if self.mensagemError.getStatus() == False:
                self.mensagemError.addMensagem("As senhas não são iguais",
                                                {'center_x': .5, 'center_y': .2})
                self.rl.add_widget(self.mensagemError)
            else:
                self.mensagemError.addMensagem("As senhas não são iguais",
                                                {'center_x': .5, 'center_y': .2})
            return
        if test_conexao() == False:    
            if self.mensagemError.getStatus() == False:
                self.mensagemError.addMensagem("Você não possui conexão com a internet! Reinicie o programa e tente novamente",
                                                {'center_x': .5, 'center_y': .2})
                self.rl.add_widget(self.mensagemError)
            else:
                self.mensagemError.addMensagem("Você não possui conexão com a internet! Reinicie o programa e tente novamente",
                                                {'center_x': .5, 'center_y': .2})
            return
    
        if self.textCriarComunidade.text == "Nome da comunidade" or self.textCriarComunidade.text == '':
                if self.mensagemError.getStatus() == False:
                    self.mensagemError.addMensagem("Não adicionou um nome à comunidade",
                                                           {'center_x': .5, 'center_y': .2})
                    self.rl.add_widget(self.mensagemError)
                else:
                    self.mensagemError.addMensagem("Não adicionou um nome à comunidade",
                                                           {'center_x': .5, 'center_y': .2})
                return 
        elif self.senha1.text == self.senha2.text:
            teste = verificaIntegridadeSenha(self.senha1.text)
            if teste == True:
                if self.db.inserirCadastro(self.novoLogin.text,self.senha1.text,self.nome.text,self.textCriarComunidade.text) == False:
                    if self.mensagemError.getStatus() == False:
                        self.mensagemError.addMensagem("Login já existente no banco de dados",
                                                        {'center_x': .5, 'center_y': .2})
                        self.rl.add_widget(self.mensagemError)
                    else:
                        self.mensagemError.addMensagem("Login já existente no banco de dados",
                                                        {'center_x': .5, 'center_y': .2})
                    return
                else:
                    self.clear_widgets()
                    mess = Mensagem(sucesso=True)
                    mess.addMensagem("Cadastro efetuado com sucesso!!",pos_hint={'center_x': .5, 'center_y': .2})
                    self.add_widget(TelaLogin(mensagem=mess))

            else:
                codigosErro = {'tamanho':'A senha deve possuir pelo menos 8 digitos',
                                'numero': 'A senha deve possuir pelo menos um número',
                                'maiuscula': 'A senha deve possuir pelo menos uma letra maiúscula',
                                'letra': 'A senha deve possuir pelo menos uma letra'}

                if self.mensagemError.getStatus() == False:
                    self.mensagemError.addMensagem(codigosErro[teste],
                                                    {'center_x': .5, 'center_y': .2})
                    self.rl.add_widget(self.mensagemError)
                else:
                    self.mensagemError.addMensagem(codigosErro[teste],
                                                    {'center_x': .5, 'center_y': .2})
                return 

            


    def exibirSenhas(self,checkbox,value):
        if value:
            self.senha1.password = False
            self.senha2.password = False
        else:
            self.senha1.password = True
            self.senha2.password = True

    def voltar(self,obj):
        self.clear_widgets()
        self.add_widget(TelaLogin())