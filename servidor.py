import socket
from threading import Thread
from Comunication.mensagem import *
import queue
import sys
from src.controle.cadastro import Cadastro
from src.Data.send import envioEmail
from Log.Logger import LOGGER

class LogicalServer:
    def __init__(self) -> None:
        self.actions = {"cadastro":self.__cadastro,
                        "login":self.__login,
                        "senha":self.__password
                        }
    def get(self,key:str,msg:dict):
        return self.actions[key](msg)

    def __cadastro(self,msg:dict):
        controleCadastro = Cadastro()
        email = msg['email']
        nome = msg['nome']
        login = msg['login']
        senha = msg['senha']
        comunidade = msg['comunidade']
        try:
            return controleCadastro.cadastrar(email,nome,login,senha,comunidade)
        except Exception as e:
            LOGGER("servidor").inserirLOG("__cadastro",str(e),"ERROR")
            return False
    
    def __password(self,msg:dict):
        controleCadastro = Cadastro()
        email = msg['email']
        try:
            senha = controleCadastro.recuperaSenha(email)
            envioEmail(email,"Recuperação de Senha",senha,"senha")
            return True
        except Exception as e:
            LOGGER("servidor").inserirLOG("__password",str(e),"ERROR")
            return False

    def __login(self,msg:dict):
        controleCadastro = Cadastro()
        login = msg['login']
        senha = msg['senha']
        try:
            return controleCadastro.login(login,senha)
        except Exception as e:
            LOGGER("servidor").inserirLOG("__login",str(e),"ERROR")
            return None

class Server:
    def __init__(self) -> None:
        self.ip = "0.0.0.0"
        self.porta = 4045
        self.address = (self.ip, self.porta)
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind(self.address)
        self.conexoes = {}
        self.server_client = Thread(target=self.__server_to_client)
        self.mensagens = queue.Queue()
        self.ServerAction = LogicalServer()

    def start(self):
        print("[INFO] Servidor Iniciado")
        self.servidor.listen()
        self.server_client.start()
        while True:
            conn, addr = self.servidor.accept()
            thread = Thread(target=self.__clients_to_server, args=(conn, addr))
            thread.start()

    def __server_to_client(self):
        while True:
            retorno_servidor = None
            addr, msg = self.mensagens.get()
            try:
                path = msg['route']
                retorno_servidor = self.ServerAction.get(path,msg)
                retorno_servidor = {"msg":retorno_servidor}
                msg_serialized = serialize(retorno_servidor)
                self.conexoes[addr].send(msg_serialized)
            except KeyError:
                LOGGER("servidor").inserirLOG("__server_to_client","Erro de chave, mensagem mal interpretada no servidor","INFO")

    def __clients_to_server(self, conn, addr):
        print(f"Um novo usuário se conectou pelo endereço = {addr}")
        buffer = b""
        expected_size = sys.maxsize  # Inicialmente, não há um tamanho esperado
        while True:
            try:
                data = conn.recv(4096)
                if data:
                    if expected_size == sys.maxsize:
                        expected_size = deserialize(data)['size_buffer']
                    else:
                        buffer += data
                        if sys.getsizeof(buffer) >= expected_size:
                            msg = deserialize(buffer)
                            self.conexoes[addr] = conn
                            self.mensagens.put((addr, msg))
                            expected_size = sys.maxsize
                            buffer = b""
                
                else:
                    LOGGER("servidor").inserirLOG("__clients_to_server",f"[INFO] Cliente {addr} desconectou","INFO")
                    print(f"[INFO] Cliente {addr} desconectou")
                    break

            except Exception as e:
                LOGGER("servidor").inserirLOG("__clients_to_server",str(e),"ERROR")
                print(f"[ERRO] {e}")
                break


Server().start()