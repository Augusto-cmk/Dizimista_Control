from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.checkbox import CheckBox
from Visao.recursos.mensagem import Mensagem
from kivy.uix.screenmanager import Screen
from Visao.recursos.funcoes import obterIP,checkboxList
from Visao.recursos.botoesAuxiliares import Menu
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Rectangle,Color
from kivy.uix.gridlayout import GridLayout
from Data.user import User
from Data.data import getMes
from Visao.LoginCadastro import TelaLogin
from Data.database import BancodeDados

class TelaPrincipal(Screen):
    def __init__(self,user:User,**kw):
        super().__init__(**kw)
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
        
        self.ruaSelecao = Menu('Selecione a rua do dizimista', {'center_x': .65, 'center_y': .76}, (.28, .05),
                               ['teste','teste1'])
        self.bloco.blocoRemoverDizimista(Button(size_hint=(.18, .05),
                                     pos_hint={'center_x': .65, 'center_y': .15},
                                     text="Remover",on_press=self.remove),None,self.ruaSelecao)
    
    def telaadd(self,obj):
        textInNome = None
        textInNumero = None
        textInRua = None
        textInZelador = None
        textInAniversario = None
        self.ruaSelecao = Menu('Selecione a rua do dizimista', {'center_x': .65, 'center_y': .42}, (.28, .05),
                               ['teste','teste1'])#self.Contribuintes.getNomeRuas())
        self.bloco.blocoAdicionarDizimista(Button(size_hint=(.18, .05),
                                     pos_hint={'center_x': .65, 'center_y': .15},
                                     text="Adicionar",on_press=self.add),self.ruaSelecao)
    
    def remove(self,obj):
        pass

    def add(self,obj):
        pass

    def selecMark(self,obj):
        self.ruaSelecao = Menu('Selecione uma rua', {'center_x': .55, 'center_y': .5}, (.28, .05),self.Contribuintes.getNomeRuas())
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
            bloco = blocoTela(self.Contribuintes,self.user,self.df,self.ruaSelecao.text)
            nomesDizimistas,dic = self.Contribuintes.dizimistasDaRua(self.ruaSelecao.text)
            bloco.telaMarcar(0.8, 0.65, nomesDizimistas,dic,getMes())
            self.rl.clear_widgets()
            self.add_widget(bloco)

    def sair(self,obj):
        self.df.apagarCredenciais(obterIP())
        self.clear_widgets()
        self.add_widget(TelaLogin(self.df))


class widgetsBloco(Widget):
    def __init__(self,rl:RelativeLayout, **kwargs):
        super().__init__(**kwargs)
        self.rl = rl
        self.listaWidget = list()
        self.erro = False

    def blocoAdicionarDizimista(self,buttonAdd:Button,menuRua:Menu):
        self.limparWidgets()

        labelNome = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .46, 'center_y': .65},
                      text='Nome do dizimista')

        textInNome = TextInput(size_hint=(.2, .05),
                                   pos_hint={'center_x': .7, 'center_y': .65}, multiline=False)

        labelNumero = Label(color='black', size_hint=(.2, .05),
                          pos_hint={'center_x': .467, 'center_y': .58},
                          text='Número da casa')

        textInNumero = TextInput(size_hint=(.2, .05),
                                   pos_hint={'center_x': .7, 'center_y': .58}, multiline=False)


        labelAniversario = Label(color='black',size_hint=(.2, .05),
                               pos_hint={'center_x': .46, 'center_y': .51},
                      text='Data de aniversário')

        textInAniversarioDia = TextInput(size_hint=(.04, .045),
                                   pos_hint={'center_x': .619, 'center_y': .51}, multiline=False)

        labelBarra = Label(color='black', size_hint=(.2, .05),
                                 pos_hint={'center_x': .649, 'center_y': .51},
                                 text='/')

        textInAniversarioMes = TextInput(size_hint=(.04, .045),
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

        self.rl.add_widget(textInNome)
        self.listaWidget.append(textInNome)
        self.rl.add_widget(textInNumero)
        self.listaWidget.append(textInNumero)
        self.rl.add_widget(menuRua)
        self.listaWidget.append(menuRua)
        self.rl.add_widget(textInAniversarioDia)
        self.listaWidget.append(textInAniversarioDia)
        self.rl.add_widget(textInAniversarioMes)
        self.listaWidget.append(textInAniversarioMes)
        self.rl.add_widget(labelBarra)
        self.listaWidget.append(labelBarra)
        self.rl.add_widget(buttonAdd)
        self.listaWidget.append(buttonAdd)
    
    def blocoRemoverDizimista(self,buttonRemove:Button,bd:BancodeDados,menuRua:Menu):
        self.limparWidgets()
        labelToRemove = Label(color='black', size_hint=(.2, .05),
                                 pos_hint={'center_x': .4, 'center_y': .76},
                                 text='Feito')
        box = CheckBox(color='black',size_hint=(.1, .1), pos_hint={'center_x': .47, 'center_y': .76})
        box.bind(active=self.selecionarNome)
        self.rl.add_widget(labelToRemove)
        self.listaWidget.append(labelToRemove)
        self.rl.add_widget(box)
        self.listaWidget.append(box)
        self.rl.add_widget(menuRua)
        self.listaWidget.append(menuRua)
        self.bd = bd
        self.menuRua = menuRua
        self.buttonRemove = buttonRemove
        self.widgetsNovo = [labelToRemove,box,menuRua]
    
    def selecionarNome(self,checkbox,value):
        nomeRua = self.menuRua.text
        self.removeWidgetsByList(self.widgetsNovo)
        if value and nomeRua != "Selecione a rua do dizimista":
            menuDizimistas = Menu('Selecione um dizimista', {'center_x': .65, 'center_y': .76}, (.28, .05),['Teste1','Teste2'])#self.bd.dizimistasRua(nomeRua))
            labelToRemove = Label(color='black', size_hint=(.2, .05),
                                 pos_hint={'center_x': .4, 'center_y': .76},
                                 text='Feito')
            box = CheckBox(color='black',size_hint=(.1, .1), pos_hint={'center_x': .47, 'center_y': .76})
            box.bind(active=self.removerDizimista)
            self.widgetsNovo.append(labelToRemove)
            self.widgetsNovo.append(box)
            self.widgetsNovo.append(menuDizimistas)
            self.rl.add_widget(menuDizimistas)
            self.rl.add_widget(labelToRemove)
            self.rl.add_widget(box)
        
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
        if value:
            # Colocar aqui a impressão das informações do dizimista e o botão de remover
            pass
        else:
            pass

    def removeWidgetsByList(self,widgets:list):
        for widget in widgets:
            self.rl.remove_widget(widget)
        
        widgets = list()

    def blocoMarcarContribuintes(self,menu,exec):
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
            self.rl.add_widget(self.labelNomeRua)
            self.listaWidget.append(self.labelNomeRua)
            self.rl.add_widget(self.textInNome)
            self.listaWidget.append(self.textInNome)
            self.rl.add_widget(self.labelZelador)
            self.listaWidget.append(self.labelZelador)
            self.rl.add_widget(self.textInZelador)
            self.listaWidget.append(self.textInZelador)

        else:
            self.removeWidgetsByList(self.widgetsNovo)


    def limparWidgets(self):
        self.removeWidgetsByList(self.listaWidget)



class blocoTela(Screen):
    def __init__(self,Contribuintes,user,df,nomeRua,**kwargs):
        super().__init__(**kwargs)
        self.Contribuintes = Contribuintes
        self.nomeRua = nomeRua
        self.user = user
        self.df = df
        self.checkBoxes = None
        self.dic = None
        self.mes = None

    def telaMarcar(self,pos_x,pos_y,listaNomes,dic,mes):
        self.dic = dic
        self.mes = mes
        self.feito = Button(text="Feito",on_press=self.marcados)
        self.checkBoxes = checkboxList(pos_x, pos_y, listaNomes)

        self.add_widget(caixaRolagem(self.feito,self.checkBoxes,self.Contribuintes,self.user,self.df))


    def marcados(self,obj):
        self.Contribuintes.dizimistasMes(self.checkBoxes.getNomesAtivos(),self.nomeRua,self.dic,self.mes)
        self.clear_widgets()
        self.add_widget(TelaPrincipal(self.Contribuintes,self.user,self.df))


class caixaRolagem(Screen):
    def __init__(self,buttonFeito,listaWidgets,Contribuintes,user,df,**kwargs):
        super().__init__(**kwargs)
        self.Contribuintes = Contribuintes
        self.user = user
        self.df = df

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
        self.add_widget(TelaPrincipal(self.Contribuintes,self.user,self.df))