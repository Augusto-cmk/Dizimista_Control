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
from Data.data import getData,getHora,getMes,getAno
from Data.database import BancodeDados_cadastro
from Data.user import User
from Data.database import BancodeDados
from modelo.dizimista import dizimista
from modelo.rua import Rua
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
                        pos_hint={'center_x': .40, 'center_y': .3},
                        text="Entrar", on_press=self.entrar)

        criarNovoCadastro = Button(size_hint=(.15, .05),
                                    pos_hint={'center_x': .53, 'center_y': .3},
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
        user = self.db.login(self.login.text,self.senha.text)
        if  user == None:
                if self.mensagemError.getStatus() == False:
                    self.mensagemError.addMensagem("Login ou senha invalidos",
                                                   {'center_x': .5, 'center_y': .2})
                    self.rl.add_widget(self.mensagemError)
                else:
                    self.mensagemError.addMensagem("Login ou senha invalidos",
                                                   {'center_x': .5, 'center_y': .2})
        else:
            self.clear_widgets()
            self.add_widget(TelaPrincipal(user=user))



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
                    mess.addMensagem("Cadastro efetuado com sucesso!!",pos_hint={'center_x': .5, 'center_y': .3})
                    BancodeDados(self.textCriarComunidade.text).criar()
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


class TelaPrincipal(Screen):
    def __init__(self,user:User,**kw):
        super().__init__(**kw)


        ## Colocar por defaut a tela de buscar um dizimista pelo nome no banco de dados para ver se o mesmo já existe
        self.db = BancodeDados(user.getComunidade())
        self.rl = RelativeLayout(size=(300, 300))
        self.mensagemError = Mensagem(error=True)
        self.user = user
        self.ruaSelecao = None

        self.bloco = widgetsBloco(self.rl)

        imagem = Image(source='imagens/fundo-de-formas-abstratas-brancas_79603-1362.avif', pos_hint={'center_x': .5, 'center_y': .5})

        labelNomeUser = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .18, 'center_y': .96}, text=f'Usuário: {user.getName()}')

        labelNomeComunidade = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .48, 'center_y': .96}, text=f'Ministrando: {user.getComunidade()}')

        dataHoraLogin = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .9, 'center_y': .98}, text='Data e hora de login')

        labelHora = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .9, 'center_y': .95}, text=f'{user.getHoraLogin()}')

        labelData = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .9, 'center_y': .92}, text=f'{user.getDataLogin()}')

        sair = Button(size_hint=(.09, .05),
                        pos_hint={'center_x': .05, 'center_y': 0.96},
                        text="Sair", on_press=self.sair)

        limparTela = Button(size_hint = (.18,.05),pos_hint={'center_x': .105,'center_y':0.76},text='Limpar tela',on_press=self.limpartela)
        visualizarDizimistas = Menu('Opções de visualização',{'center_x': .105, 'center_y': 0.68},(.2,.05),
                                    ['Todos os dizimistas','Contribuintes','Não contribuintes'])
        # Utilizar gráficos demonstrativos para explicar de forma resumida como estão todos os dizimistas em relação a contribuição

        ver = Button(size_hint=(.18, .05),
                                      pos_hint={'center_x': .105, 'center_y': 0.6},
                                      text="Visualizar")

        adicionarDizimista = Button(size_hint=(.18, .05),
                                      pos_hint={'center_x': .105, 'center_y': 0.4},
                                      text="Adicionar dizimista",on_press = self.telaadd)

        removerDizimista = Button(size_hint=(.18, .05),
                                      pos_hint={'center_x': .105, 'center_y': 0.3},
                                      text="Remover dizimista",on_press=self.telaRemove)

        marcarContribuintes  = Button(size_hint=(.18, .05),
                                      pos_hint={'center_x': .105, 'center_y': 0.2},
                                      text="Marcar contribuites",on_press=self.selecMark)

        alterar = Button(size_hint=(.18, .05),
                                     pos_hint={'center_x': .105, 'center_y': 0.1},
                                     text="Alterar dados")


        self.rl.add_widget(imagem)
        self.rl.add_widget(limparTela)
        self.rl.add_widget(alterar)
        self.rl.add_widget(ver)
        self.rl.add_widget(marcarContribuintes)
        self.rl.add_widget(removerDizimista)
        self.rl.add_widget(adicionarDizimista)
        self.rl.add_widget(visualizarDizimistas)
        self.rl.add_widget(dataHoraLogin)
        self.rl.add_widget(labelData)
        self.rl.add_widget(labelHora)
        self.rl.add_widget(labelNomeUser)
        self.rl.add_widget(labelNomeComunidade)
        self.rl.add_widget(sair)


        self.add_widget(self.rl)

    def limpartela(self,obj):
        self.bloco.limparWidgets()

    def telaRemove(self,obj):
        if self.bloco.erro:
            self.bloco.limparWidgets()
        
        self.bloco.blocoRemoverDizimista(self.user)
    
    def telaadd(self,obj):
        self.bloco.blocoAdicionarDizimista(self.user)

    def selecMark(self,obj):
        self.ruaSelecao = Menu('Selecione uma rua', {'center_x': .55, 'center_y': .5}, (.28, .05),self.db.ruasDisponiveis())
        self.bloco.blocoMarcarContribuintes(self.ruaSelecao,Button(size_hint=(.2, .05),
                               pos_hint={'center_x': .82, 'center_y': .5},
                      text='Marcar contribuintes',on_press=self.execMark))

    def execMark(self,obj):
        if self.ruaSelecao.text == 'Selecione uma rua':
            if self.mensagemError.getStatus() == False:
                self.mensagemError.addMensagem(
                    "Você não selecionou uma rua",
                    {'center_x': .65, 'center_y': .2})
                self.rl.add_widget(self.mensagemError)
            else:
                self.mensagemError.addMensagem(
                    "Você não selecionou uma rua",
                    {'center_x': .65, 'center_y': .2})

        else:
            bloco = blocoTela(self.user,self.ruaSelecao.text)
            nomesDizimistas = self.db.naoContribuintesRua(getMes(),getAno(),self.ruaSelecao.text)
            bloco.telaMarcar(0.8, 0.65, nomesDizimistas,getMes())
            self.rl.clear_widgets()
            self.add_widget(bloco)

    def sair(self,obj):
        self.clear_widgets()
        self.add_widget(TelaLogin())


class widgetsBloco(Widget):
    def __init__(self,rl:RelativeLayout, **kwargs):
        super().__init__(**kwargs)
        self.rl = rl
        self.listaWidget = list()
        self.erro = False
        self.infodiz = infoDizimista(self.rl)
        self.mensagens = list()

    def blocoAdicionarDizimista(self,user:User):
        self.limparWidgets()
        self.db = BancodeDados(user.getComunidade())
        self.novaRuaInserida = False
        self.ruaSelecao = Menu('Selecione a rua do dizimista', {'center_x': .65, 'center_y': .42}, (.28, .05),self.db.ruasDisponiveis())
        buttonAdd = Button(size_hint=(.18, .05),
                                     pos_hint={'center_x': .65, 'center_y': .15},
                                     text="Adicionar",on_press=self.addDizimista)

        labelNome = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .46, 'center_y': .65},
                      text='Nome do dizimista')

        self.textNomeDizimista = TextInput(size_hint=(.2, .05),
                                   pos_hint={'center_x': .7, 'center_y': .65}, multiline=False)

        labelNumero = Label(color='black', size_hint=(.2, .05),
                          pos_hint={'center_x': .467, 'center_y': .58},
                          text='Número da casa')

        self.textNumeroDizimista = TextInput(size_hint=(.2, .05),
                                   pos_hint={'center_x': .7, 'center_y': .58}, multiline=False)


        labelAniversario = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .46, 'center_y': .51},
                      text='Data de aniversário')

        self.textAniversarioDia = TextInput(size_hint=(.04, .045),
                                   pos_hint={'center_x': .619, 'center_y': .51}, multiline=False)

        labelBarra = Label(color='black', size_hint=(.2, .05),
                                 pos_hint={'center_x': .649, 'center_y': .51},
                                 text='/')

        self.textAniversarioMes = TextInput(size_hint=(.04, .045),
                                         pos_hint={'center_x': .679, 'center_y': .51}, multiline=False)

        box = CheckBox(color='black',size_hint=(.1, .1), pos_hint={'center_x': .47, 'center_y': .42})
        box.bind(active=self.novaRua)

        nova = Label(color='black', size_hint=(.2, .05),
                                 pos_hint={'center_x': .4, 'center_y': .42},
                                 text='Nova rua')

        self.labelNomeRua = Label(color='black', size_hint=(.2, .05),
                                  pos_hint={'center_x': .46, 'center_y': .3},
                                  text='Nome da rua')

        self.textInNome = TextInput(size_hint=(.2, .05),
                                    pos_hint={'center_x': .7, 'center_y': .3}, multiline=False)

        self.labelZelador = Label(color='black', size_hint=(.2, .05),
                                  pos_hint={'center_x': .46, 'center_y': .23},
                                  text='Nome do zelador')

        self.textInZelador = TextInput(size_hint=(.2, .05),
                                       pos_hint={'center_x': .7, 'center_y': .23}, multiline=False)

        self.widgetsNovo = [self.labelNomeRua, self.textInNome, self.textInZelador, self.labelZelador]


        self.rl.add_widget(labelNome)
        self.listaWidget.append(labelNome)
        self.rl.add_widget(labelNumero)
        self.listaWidget.append(labelNumero)
        self.rl.add_widget(labelAniversario)
        self.listaWidget.append(labelAniversario)
        self.rl.add_widget(box)
        self.listaWidget.append(box)
        self.rl.add_widget(nova)
        self.listaWidget.append(nova)

        self.rl.add_widget(self.textNomeDizimista)
        self.listaWidget.append(self.textNomeDizimista)
        self.rl.add_widget(self.textNumeroDizimista)
        self.listaWidget.append(self.textNumeroDizimista)
        self.rl.add_widget(self.ruaSelecao)
        self.listaWidget.append(self.ruaSelecao)
        self.rl.add_widget(self.textAniversarioDia)
        self.listaWidget.append(self.textAniversarioDia)
        self.rl.add_widget(self.textAniversarioMes)
        self.listaWidget.append(self.textAniversarioMes)
        self.rl.add_widget(labelBarra)
        self.listaWidget.append(labelBarra)
        self.rl.add_widget(buttonAdd)
        self.listaWidget.append(buttonAdd)
    
    def addDizimista(self,obj):
        self.removeWidgetsByList(self.mensagens)
        nomeDizimista = remvDofim(self.textNomeDizimista.text)
        numeroDizimista = remvDofim(self.textNumeroDizimista.text)
        diaAniversario = remvDofim(self.textAniversarioDia.text)
        mesAniversario = remvDofim(self.textAniversarioMes.text)
        if self.novaRuaInserida:
            nomeRua = remvDofim(self.textInNome.text)
            nomeZelador = remvDofim(self.textInZelador.text)
            nomeDizimista = remvDofim(self.textNomeDizimista.text)

            if nomeRua == '' or nomeZelador == '':
                error = Mensagem(error=True)
                error.addMensagem("Todos os campos da nova rua precisam ser preenchidos",{'center_x': .65, 'center_y': .1})
                self.rl.add_widget(error)
                self.widgetsNovo.append(error)
                self.listaWidget.append(error)
            else:
                if nomeDizimista == '' or numeroDizimista == '' or diaAniversario == '' or mesAniversario == '':
                    error = Mensagem(error=True)
                    error.addMensagem("Todos os campos do novo dizimista precisam ser preenchidos",{'center_x': .65, 'center_y': .1})
                    self.rl.add_widget(error)
                    self.widgetsNovo.append(error)
                    self.listaWidget.append(error)
                else:
                    self.db.inserirRua(nomeRua,nomeZelador)
                    self.db.inserirDizimista(nomeDizimista,numeroDizimista,f"{diaAniversario}/{mesAniversario}",nomeRua)
                    sucesso = Mensagem(sucesso=True)
                    sucesso.addMensagem("Dizimista inserido com sucesso!",{'center_x': .65, 'center_y': .1})
                    self.rl.add_widget(sucesso)
                    self.widgetsNovo.append(sucesso)
                    self.listaWidget.append(sucesso)
        else:
            self.removeWidgetsByList(self.widgetsNovo)
            if self.ruaSelecao.text == 'Selecione a rua do dizimista':
                error = Mensagem(error=True)
                error.addMensagem("É necessário que selecione uma rua ou crie uma nova rua para adicionar o dizimista",{'center_x': .6, 'center_y': .1})
                self.rl.add_widget(error)
                self.widgetsNovo.append(error)
                self.listaWidget.append(error)
            else:
                if nomeDizimista == '' or numeroDizimista == '' or diaAniversario == '' or mesAniversario == '':
                    error = Mensagem(error=True)
                    error.addMensagem("Todos os campos do novo dizimista precisam ser preenchidos",{'center_x': .65, 'center_y': .1})
                    self.rl.add_widget(error)
                    self.widgetsNovo.append(error)
                    self.listaWidget.append(error)
                else:
                    resposta = self.db.inserirDizimista(nomeDizimista,numeroDizimista,f"{diaAniversario}/{mesAniversario}",self.ruaSelecao.text)
                    if resposta:
                        sucesso = Mensagem(sucesso=True)
                        sucesso.addMensagem("Dizimista inserido com sucesso!",{'center_x': .65, 'center_y': .1})
                        self.rl.add_widget(sucesso)
                        self.mensagens.append(sucesso)
                        self.listaWidget.append(sucesso)
                    else:
                        erro = Mensagem(error=True)
                        erro.addMensagem("Dizimista não foi inserido por que já existe!",{'center_x': .65, 'center_y': .1})
                        self.rl.add_widget(erro)
                        self.mensagens.append(erro)
                        self.listaWidget.append(erro)


    
    def blocoRemoverDizimista(self,user:User):
        self.limparWidgets()
        self.db = BancodeDados(user.getComunidade())
        buttonRemove = Button(size_hint=(.18, .05),
                                     pos_hint={'center_x': .65, 'center_y': .55},
                                     text="Remover",on_press=self.remover)
        labelToRemove = Label(color='black', size_hint=(.2, .05),
                                 pos_hint={'center_x': .4, 'center_y': .76},
                                 text='Feito')
        box = CheckBox(color='black',size_hint=(.1, .1), pos_hint={'center_x': .47, 'center_y': .76})
        self.menuRua = Menu('Selecione a rua do dizimista', {'center_x': .65, 'center_y': .76}, (.28, .05),
                               self.db.ruasDisponiveis())

        box.bind(active=self.selecionarNome)
        self.rl.add_widget(labelToRemove)
        self.listaWidget.append(labelToRemove)
        self.rl.add_widget(box)
        self.listaWidget.append(box)
        self.rl.add_widget(self.menuRua)
        self.listaWidget.append(self.menuRua)
        self.buttonRemove = buttonRemove
        self.widgetsNovo = [labelToRemove,box,self.menuRua]
    
    def selecionarNome(self,checkbox,value):
        nomeRua = self.menuRua.text
        self.removeWidgetsByList(self.widgetsNovo)
        if value and nomeRua != "Selecione a rua do dizimista":
            self.menuDizimistas = Menu('Selecione um dizimista', {'center_x': .65, 'center_y': .76}, (.28, .05),self.db.dizimistasRua(nomeRua))
            labelToRemove = Label(color='black', size_hint=(.2, .05),
                                 pos_hint={'center_x': .4, 'center_y': .76},
                                 text='Feito')
            box = CheckBox(color='black',size_hint=(.1, .1), pos_hint={'center_x': .47, 'center_y': .76})
            box.bind(active=self.removerDizimista)
            self.widgetsNovo.append(labelToRemove)
            self.widgetsNovo.append(box)
            self.widgetsNovo.append(self.menuDizimistas)
            self.rl.add_widget(self.menuDizimistas)
            self.rl.add_widget(labelToRemove)
            self.rl.add_widget(box)
            self.listaWidget.append(self.menuDizimistas)
            self.listaWidget.append(labelToRemove)
            self.listaWidget.append(box)
        
        elif nomeRua == "Selecione a rua do dizimista":
            self.erro = True
            self.removeWidgetsByList(self.widgetsNovo)
            mensagem = Mensagem(error=True)
            mensagem.addMensagem("Não foi selecionada uma rua, favor tentar novamente !!",pos_hint={'center_x': .65, 'center_y': .76})
            self.rl.add_widget(mensagem)
            self.listaWidget.append(mensagem)
        
        else:
            self.removeWidgetsByList(self.widgetsNovo)
    
    def removerDizimista(self,checkbox,value):
        self.removeWidgetsByList(self.widgetsNovo)
        self.infodiz.limparInfo()
        if value:
            dadosDizimista = self.menuDizimistas.text.split("-")
            if self.menuDizimistas.text == "Selecione um dizimista":
                error = Mensagem(error=True)
                error.addMensagem("Não foi selecionado um dizimista",{'center_x': .65, 'center_y': .76})
                self.rl.add_widget(error)
                self.widgetsNovo.append(error)
                self.listaWidget.append(error)
            else:
                self.nome = remvDofim(dadosDizimista[0])
                self.numero = remvDofim(dadosDizimista[1])
                infodizimista = self.db.getDizimista(self.nome,self.menuRua.text,self.numero)
                self.infodiz.showInfo({'center_x': .65, 'center_y': .76},infodizimista[1],infodizimista[2],infodizimista[3],infodizimista[4]) 
                self.removeWidgetsByList(self.widgetsNovo)
                self.rl.add_widget(self.buttonRemove)
                self.listaWidget.append(self.buttonRemove)
                
        else:
            self.removeWidgetsByList(self.widgetsNovo)
    
    def remover(self,obj):
        self.db.removerDizimista(self.nome,self.numero,self.menuRua.text)
        sucesso = Mensagem(sucesso=True)
        sucesso.addMensagem("Dizimista removido com sucesso!",{'center_x': .65, 'center_y': .45})
        self.rl.add_widget(sucesso)
        self.widgetsNovo.append(sucesso)
        self.listaWidget.append(sucesso)
        for widget in self.infodiz.listaWidget:
            self.listaWidget.append(widget)

    def removeWidgetsByList(self,widgets:list):
        for widget in widgets:
            self.rl.remove_widget(widget)
        
        widgets = list()

    def blocoMarcarContribuintes(self,menu:Menu,exec:Button):
        self.limparWidgets()
        label = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .67, 'center_y': .7},
                      text='Escolha uma rua para a qual deseja marcar os contribuintes do mês')

        self.rl.add_widget(exec)
        self.rl.add_widget(menu)
        self.rl.add_widget(label)
        self.listaWidget.append(label)
        self.listaWidget.append(menu)
        self.listaWidget.append(exec)

    def novaRua(self,checkbox,value):
        if value:
            self.novaRuaInserida = True
            self.rl.add_widget(self.labelNomeRua)
            self.listaWidget.append(self.labelNomeRua)
            self.rl.add_widget(self.textInNome)
            self.listaWidget.append(self.textInNome)
            self.rl.add_widget(self.labelZelador)
            self.listaWidget.append(self.labelZelador)
            self.rl.add_widget(self.textInZelador)
            self.listaWidget.append(self.textInZelador)

        else:
            self.novaRuaInserida = False
            self.removeWidgetsByList(self.widgetsNovo)


    def limparWidgets(self):
        self.removeWidgetsByList(self.listaWidget)


class infoDizimista(Widget):
    def __init__(self,rl:RelativeLayout, **kwargs):
        super().__init__(**kwargs)
        self.rl = rl
        self.listaWidget = list()
        self.erro = False
    
    def showInfo(self,pos,nomeDizimista:str,numeroCasa:str,dataAniver:str,nomeRua:str):
        labelInit = Label(color='black',size_hint=(.2, .05),
                               pos_hint=pos,
                      text='_____________ informações _____________')
        
        labelNome = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': pos['center_x'], 'center_y':pos['center_y']-0.04},
                      text=f'Nome: {nomeDizimista}')
        
        labelNomeRua = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': pos['center_x'], 'center_y':pos['center_y']-0.08},
                      text=f'Rua: {nomeRua}')
        
        labelNumero = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': pos['center_x'], 'center_y':pos['center_y']-0.12},
                      text=f'Número da casa: {numeroCasa}')
        
        labelAniversario = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': pos['center_x'], 'center_y':pos['center_y']-0.16},
                      text=f'Data de Aniversário: {dataAniver}')

        self.rl.add_widget(labelInit)
        self.rl.add_widget(labelNome)
        self.rl.add_widget(labelNomeRua)
        self.rl.add_widget(labelNumero)
        self.rl.add_widget(labelAniversario)
        self.listaWidget.append(labelInit)
        self.listaWidget.append(labelNome)
        self.listaWidget.append(labelNomeRua)
        self.listaWidget.append(labelNumero)
        self.listaWidget.append(labelAniversario)
    
    def limparInfo(self):
        for widget in self.listaWidget:
            self.rl.remove_widget(widget)
        
        self.listaWidget = list()

class blocoTela(Screen):
    def __init__(self,user:User,nomeRua:str,**kwargs):
        super().__init__(**kwargs)
        self.nomeRua = nomeRua
        self.user = user
        self.db = BancodeDados(self.user.getComunidade())
        self.checkBoxes = None
        self.dic = None
        self.mes = None

    def telaMarcar(self,pos_x,pos_y,listaNomes,mes):
        self.mes = mes
        self.feito = Button(text="Feito",on_press=self.marcados)
        self.checkBoxes = checkboxList(pos_x, pos_y, listaNomes)

        self.add_widget(caixaRolagem(self.feito,self.checkBoxes,self.user))


    def marcados(self,obj):
        nomesConstribuintes = self.checkBoxes.getNomesAtivos()
        for contribuinte in nomesConstribuintes:
            diz = contribuinte.split('-')
            nome = remvDofim(diz[0])
            nCasa = remvDofim(diz[1])
            self.db.marcarContribuinte(nome,self.nomeRua,nCasa,getMes(),getAno())

        self.clear_widgets()
        self.add_widget(TelaPrincipal(self.user))


class caixaRolagem(Screen):
    def __init__(self,buttonFeito:Button,listaWidgets:list,user,**kwargs):
        super().__init__(**kwargs)
        self.user = user

        rl = RelativeLayout()

        scroll = ScrollView()
        buttonFeito.pos_hint = {'center_x': 0.1, 'center_y': 0.1}
        buttonFeito.size_hint = (0.07, 0.05)

        buttonVoltar = Button(size_hint = (.08, .05),pos_hint={'center_x': 0.2, 'center_y': 0.1},text='Voltar',on_press=self.voltar,height=40)

        layout = GridLayout(cols=2,spacing=10,size_hint_y=None,row_force_default=True,row_default_height=60,padding=100)
        layout.bind(minimum_height = layout.setter('height'))



        for widget in listaWidgets:
            layout.add_widget(widget)

        scroll.bar_width = 10
        scroll.add_widget(layout)
        rl.add_widget(scroll)
        rl.add_widget(buttonVoltar)
        rl.add_widget(buttonFeito)
        self.add_widget(rl)

    def voltar(self,obj):
        self.clear_widgets()
        self.add_widget(TelaPrincipal(self.user))