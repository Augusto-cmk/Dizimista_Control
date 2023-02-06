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
        self.user = None

        self.rl = RelativeLayout(size=(300, 300))


        self.flagSalvarCredenciais = True

        self.mensagemError = Mensagem(error=True)

        labelLembrar = Label(color='black',size_hint=(.2, .05),
                                pos_hint={'center_x': .50, 'center_y': .36}, text='Salvar credenciais')

        lembrarCadastro = CheckBox(color='black',size_hint=(.1, .1), pos_hint={'center_x': .59, 'center_y': .36},active=True)

        lembrarCadastro.bind(active=self.lembrarCadastro)

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

        esqueceuSenha = Button(size_hint=(.19, .05),
                        pos_hint={'center_x': .66, 'center_y': .3},
                        text="Esqueci minha senha", on_press=self.enviarEmailComSenha)

        self.mensagemSucesso = mensagem

        if mensagem != None:
            self.rl.add_widget(self.mensagemSucesso)

        self.rl.add_widget(imagem)
        self.rl.add_widget(esqueceuSenha)
        self.rl.add_widget(labelExibirSenha)
        self.rl.add_widget(exibirsenha)
        self.rl.add_widget(labelLembrar)
        self.rl.add_widget(lembrarCadastro)
        self.rl.add_widget(criarNovoCadastro)
        self.rl.add_widget(labelSenha)
        self.rl.add_widget(labelLogin)
        self.rl.add_widget(self.login)
        self.rl.add_widget(self.senha)
        self.rl.add_widget(entrar)
        self.add_widget(self.rl)

    def enviarEmailComSenha(self,obj):
        self.login.text = remvDofim(self.login.text)
        if self.login.text == '':
            if self.mensagemError.getStatus() == False:
                self.mensagemError.addMensagem(
                    "Você não preencheu o campo de login",
                    {'center_x': .5, 'center_y': .2})
                self.rl.add_widget(self.mensagemError)
            else:
                self.mensagemError.addMensagem(
                    "Você não preencheu o campo de login",
                    {'center_x': .5, 'center_y': .2})

        else:
            pass


    def exibirSenha(self,checkbox,value):
        if value:
            self.senha.password = False
        else:
            self.senha.password = True


    def lembrarCadastro(self,checkbox,value):
        self.flagSalvarCredenciais = value

    def criarCadastro(self,obj):
        self.clear_widgets()
        self.add_widget(TelaCadastro())

    def entrar(self,obj):
        self.login.text = remvDofim(self.login.text)
        self.senha.text = remvDofim(self.senha.text)

        if self.mensagemSucesso != None and self.mensagemSucesso.getStatus() != False:
            self.rl.remove_widget(self.mensagemSucesso)
        # Realizar as operações para entrar no sistema



class TelaCadastro(Screen):
    def __init__(self,erro = None,login=None,**kw):
        super().__init__(**kw)

        self.mensagemError = Mensagem(error=True)

        self.erro = erro

        self.addComunidade = False

        self.rl = RelativeLayout(size=(300, 300))

        telaFundo = Fundo(2000,1000,[0.98,0.98,0.98,0.98])
        
        self.newComunidade = CheckBox(color='black',size_hint=(.1, .1), pos_hint={'center_x': .385, 'center_y': .34})
        self.newComunidade.bind(active = self.criarComunidade)
        self.textCriarComunidade = TextInput(size_hint=(.2, .05),
                           pos_hint={'center_x': .5, 'center_y': .34}, multiline=False,text='Nome da comunidade')
        labelCriarComunidade = Label(color='black',size_hint=(.2, .05),
                           pos_hint={'center_x': .298, 'center_y': .34}, text='Nova comunidade')

        exibirsenhas = CheckBox(color='black',size_hint=(.1, .1), pos_hint={'center_x': .62, 'center_y': .41})
        exibirsenhas.bind(active=self.exibirSenhas)

        labelExibirSenha = Label(color='black',size_hint=(.2, .05),
                                 pos_hint={'center_x': .7, 'center_y': .41}, text='Exibir senhas')

        self.novoLogin = TextInput(size_hint=(.2, .05),
                  pos_hint={'center_x': .5, 'center_y': .62}, multiline=False)

        self.nome = TextInput(size_hint=(.2, .05),
                  pos_hint={'center_x': .5, 'center_y': .69}, multiline=False)

        labelNome = Label(color='black',size_hint=(.2, .05),
                                 pos_hint={'center_x': .35, 'center_y': .69}, text='Nome')

        self.email = TextInput(size_hint=(.2, .05),
                                   pos_hint={'center_x': .5, 'center_y': .55}, multiline=False)

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
                           pos_hint={'center_x': .35, 'center_y': .62}, text='Login')

        labelEmail = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .35, 'center_y': .55}, text='e-mail')

        Cadastrar = Button(size_hint=(.1, .05),
                        pos_hint={'center_x': .54, 'center_y': .27},
                        text="Cadastrar", on_press=self.cadastrar)

        Voltar = Button(size_hint=(.09, .05),
                        pos_hint={'center_x': .65, 'center_y': .27},
                        text="Voltar", on_press=self.voltar)

        if erro != None:
            self.rl.add_widget(erro)

        self.rl.add_widget(telaFundo)
        self.rl.add_widget(imagem)
        self.rl.add_widget(self.nome)
        self.rl.add_widget(labelNome)
        self.rl.add_widget(self.email)
        self.rl.add_widget(labelEmail)
        self.rl.add_widget(labelCriarComunidade)
        self.rl.add_widget(self.newComunidade)
        self.rl.add_widget(exibirsenhas)
        self.rl.add_widget(labelExibirSenha)
        self.rl.add_widget(labelSenha2)
        self.rl.add_widget(self.senha2)
        self.rl.add_widget(labelSenha1)
        self.rl.add_widget(self.senha1)
        self.rl.add_widget(self.novoLogin)
        self.rl.add_widget(labelNovoLogin)
        self.rl.add_widget(Voltar)
        self.rl.add_widget(Cadastrar)
        self.add_widget(self.rl)

    def criarComunidade(self,checkbox,value):
        if value:
            self.rl.add_widget(self.textCriarComunidade)
            self.addComunidade = True
        else:
            self.rl.remove_widget(self.textCriarComunidade)
            self.textCriarComunidade.text = "Nome da comunidade"
            self.addComunidade = False
            if self.mensagemError.getStatus():
                self.rl.remove_widget(self.mensagemError)
                self.mensagemError.setStatus(False)


    def cadastrar(self,obj):
        if self.erro != None:
            self.rl.remove_widget(self.erro)
        if test_conexao() != False:
            self.senha1.text = remvDofim(self.senha1.text)
            self.senha2.text = remvDofim(self.senha2.text)
            self.novoLogin.text = remvDofim(self.novoLogin.text)
            self.email.text = remvDofim(self.email.text)
            self.nome.text = remvDofim(self.nome.text)

            


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


class TelaConfirmacaoEmail(Screen):
    def __init__(self,codigo,destino,login, **kw):
        super().__init__(**kw)
        self.login = login
        self.error = Mensagem(error=True)
        if envioEmail(destino,'Confirmação',codigo,'confirmar'):
            self.codigo = codigo
            self.rl = RelativeLayout(size=(300, 300))
            self.codigoConfirmacao = TextInput(size_hint=(.2, .05),
                                               pos_hint={'center_x': .5, 'center_y': .5}, multiline=False)

            labelCodigo = Label(size_hint=(.2, .05),
                                pos_hint={'center_x': .27, 'center_y': .5}, text='Código de confirmação')

            confirmar = Button(size_hint=(.09, .05),
                            pos_hint={'center_x': .4, 'center_y': .4},
                            text="Confirmar", on_press=self.confirmar)

            mensagem = Mensagem(sucesso=True)
            mensagem.addMensagem("Um código foi enviado ao seu e-mail, favor inserir o código no campo abaixo",{'center_x': .5, 'center_y': .6})


            pular = Button(size_hint=(.18, .05),
                            pos_hint={'center_x': .6, 'center_y': .4},
                            text="Pular confirmação", on_press=self.pular)

            self.rl.add_widget(pular)
            self.rl.add_widget(mensagem)
            self.rl.add_widget(confirmar)
            self.rl.add_widget(self.codigoConfirmacao)
            self.rl.add_widget(labelCodigo)
            self.add_widget(self.rl)

        else:
            self.clear_widgets()
            erro = Mensagem(error=True)
            erro.addMensagem("O email inserido é inválido!",{'center_x': .5, 'center_y': .2})
            self.add_widget(TelaCadastro(erro=erro,login=self.login))

    def confirmar(self,obj):
        self.codigoConfirmacao.text = remvDofim(self.codigoConfirmacao.text)
        if int(self.codigoConfirmacao.text) == self.codigo:
            self.clear_widgets()
            cadastroSucesso = Mensagem(sucesso=True)
            cadastroSucesso.addMensagem("Cadastro efetuado com sucesso",
                                        {'center_x': .5, 'center_y': .2})
            self.add_widget(TelaLogin(mensagem=cadastroSucesso))
        else:
            if self.error.getStatus() == False:
                self.error.addMensagem("O código inserido está incorreto, favor inserir novamente!",{'center_x': .5, 'center_y': .2})
                self.rl.add_widget(self.error)
            else:
                self.error.addMensagem("O código inserido está incorreto, favor inserir novamente!",{'center_x': .5, 'center_y': .2})

    def pular(self,obj):
        self.clear_widgets()
        cadastroSucesso = Mensagem(sucesso=True)
        cadastroSucesso.addMensagem("Cadastro efetuado com sucesso",
                                    {'center_x': .5, 'center_y': .2})
        self.add_widget(TelaLogin(mensagem=cadastroSucesso))