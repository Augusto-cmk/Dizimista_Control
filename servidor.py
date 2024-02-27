import socket
from threading import Thread
from Comunication.mensagem import *
import queue
import sys
import time

class LogicalServer: # Serve para realizar a ação requisitada pelo usuário, ao acessar a posição ele realiza a operação
    def __init__(self) -> None:
        self.actions = {"cadastro":self.__cadastro,
                        "alterar dados usuário":self.__alterar_dados_usuario,
                        "login":self.__login,
                        "password":self.__password
                        }
    def get(self,key:str,msg:dict):
        return self.actions[key](msg)

    def __cadastro(self,msg:dict):
        try:
            # Realizar o cadasttro do cliente
            return True
        except Exception:
            return False
    
    def __password(self,msg:dict):
        email = msg['email']
        password = None # Obser senha do usuário
        return password

    def __login(self,msg:dict):
        email = msg['email']
        senha = msg['password']
        try:
            # Obter os dados a serem retornados para efetuar o login
            return {}
        except Exception:
            return None

    def __alterar_dados_usuario(self,msg:dict):
        perfil_atualizado = None
        return perfil_atualizado

class Server:
    def __init__(self) -> None:
        self.ip = "192.168.3.11"
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
            # Realizar o tratamento da mensagem
            try:
                path = msg['route']
                retorno_servidor = self.ServerAction.get(path,msg)
                # ------------------------------
                # Depois, mandar a mensagem para o cliente
                msg_serialized = serialize(retorno_servidor)
                self.conexoes[addr].send(serialize({"size_buffer": sys.getsizeof(msg_serialized)}))

                fragmentos = fragment_msg(msg_serialized, 4096)
                time.sleep(0.1)
                for fragmento in fragmentos:
                    self.conexoes[addr].send(fragmento)
            except KeyError:
                print("[INFO] Erro de chave, mensagem mal interpretada no servidor")

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
                            msg = deserialize(buffer)  # Recebe a classe enviada pelo cliente (Obs: O servidor deve conhecer a estrutura da classe)
                            self.conexoes[addr] = conn
                            self.mensagens.put((addr, msg))
                            expected_size = sys.maxsize
                            buffer = b""
                
                else:
                    print(f"[INFO] Cliente {addr} desconectou")
                    break

            except Exception:
                print(f"[INFO] Cliente {addr} desconectou")
                break


Server().start()