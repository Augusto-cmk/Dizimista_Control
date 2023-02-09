import sqlite3
import numpy as np
from Data.user import User
# consulta = http://pythonclub.com.br/gerenciando-banco-dados-sqlite3-python-parte1.html
# Dados = https://docs.google.com/spreadsheets/d/1_HBwd5AdT7gH_P5IoNFRyOkfJZmTLLPD/edit#gid=11936601

def transform(listWithTuple:list)->list:
    return [tupla[0] for tupla in listWithTuple]

def concat(listOfDizimist:list)->list:
    lista = list()
    for dizimista in listOfDizimist:
        lista.append(f"{dizimista[0]} - {dizimista[1]}")
    return lista

class BancodeDados:
    def __init__(self,nome:str):
        self.nome = nome
        self.conn = sqlite3.connect(f"{nome}.db")
        self.cmd = self.conn.cursor()
    
    def __obterIds(self,table:str,nomeId:str):
        return self.cmd.execute(
            f"""
              SELECT {nomeId} from {table};
            """
        )
    def __getIdDizimista(self,nome:str,nCasa:str,nomeRua:str)->int:
        try:
            return self.cmd.execute(
                """
                    SELECT idDizimista,nome,nCasa,nRua from dizimista
                    where nome = ? and nCasa = ? and nRua = ?;            
                """,(nome,nCasa,nomeRua,)
            ).fetchall()[0][0]
        except IndexError:
            return None

    def __getnewID(self,table:str,nomeId:str)->int:
        try:
            id = np.array(transform(self.__obterIds(table,nomeId).fetchall())).max()
            if id >=0:
                return int(id+1)
            else:
                return 0
        except Exception:
            return 0

    def criar(self):
        self.cmd.execute(
            """
            CREATE TABLE IF NOT EXISTS dizimista (
                    idDizimista int,
                    nome varchar(100) not null,
                    nCasa varchar(20) not null,
                    aniversario datetime,
                    nRua varchar(20) not null,
                    primary key(idDizimista)
                );
            """
        )
        self.cmd.execute(
            """
                CREATE TABLE IF NOT EXISTS rua(
                    idRua int,
                    nomeRua varchar(20),
                    zelador varchar(20),
                    primary key(idRua)
                );
                """
        )
        self.cmd.execute(
            """
                CREATE TABLE IF NOT EXISTS doacao(
                    idDoacao int,
                    idDizimista int not null,
                    mesContribuicao varchar(20),
                    anoContribuicao varchar(20),
                    primary key(idDoacao),
                    foreign key(idDizimista) references contribuinte(idDizimista)
                );
            """
        )
        self.conn.commit()
    def marcarContribuinte(self,nomeDizimista:str,nomeRua:str,nCasa:str,mesContribuido:str,anoContribuicao:str)->bool:
        try:
            idDizimista = self.__getIdDizimista(nomeDizimista,nCasa,nomeRua)
            self.cmd.execute(
                """
                    INSERT INTO doacao(idDoacao,idDizimista,mesContribuicao,anoContribuicao)
                    values(?,?,?,?);
                """,(self.__getnewID("doacao","idDoacao"),idDizimista,mesContribuido,anoContribuicao,)
            )
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def doacoesDizimista(self,nomeDizimista:str,nomeRua:str,nCasa:str,anoDoacao:str)->list:
        try:
            return transform(self.cmd.execute(
                """
                SELECT mesContribuicao from doacao natural join dizimista
                where dizimista.idDizimista = ? and doacao.anoContribuicao = ?;
                """,(self.__getIdDizimista(nomeDizimista,nCasa,nomeRua),anoDoacao,)
            ).fetchall())
        except Exception:
            return None

    def inserirDizimista(self,nome:str,nCasa:int,dataNiver:str,nomeRua:str):
        dizimista = transform(self.cmd.execute(
            """
            SELECT nome from dizimista where nome = ?;
            """,(nome,)
        ).fetchall())

        if nome not in dizimista:
            self.cmd.execute(
                f"""
                    INSERT INTO dizimista(idDizimista,nome,nCasa,aniversario,nRua)
                    values(?,?,?,?,?);
                """,(self.__getnewID("dizimista","idDizimista"),nome,nCasa,dataNiver,nomeRua,)
            )
            self.conn.commit()

    def removerDizimista(self,nome:str,nCasa:str,nomeRua:str)->int:
        try:
            id = self.__getIdDizimista(nome,nCasa,nomeRua)
            self.cmd.execute(
                """
                    delete from dizimista where idDizimista = ?;
                """,(id,)
            )
            self.conn.commit()
            return True
        except Exception:
            return False

    def removerRua(self,nomeRua:str)->int:
        try:
            self.cmd.execute(
                """
                    delete from rua where nomeRua = ?;
                """,(nomeRua,)
            )
            self.conn.commit()
            return True
        except Exception:
            return False

    def removerDoacao(self,nomeDizimista:str,nCasa:str,nomeRua:str,mesDoacao:str):
        try:
            id = self.__getIdDizimista(nomeDizimista,nCasa,nomeRua)
            self.cmd.execute(
                """
                    delete from doacao where idDizimista = ? and mesContribuicao = ?;
                """,(id,mesDoacao,)
            )
            self.conn.commit()
            return True
        except Exception:
            return False

    def obterZelador(self,nomeRua:str)->str:
        try:
            return self.cmd.execute(
                """
                    SELECT zelador from rua
                    where rua.nomeRua = ?;
                """,(nomeRua,)
            ).fetchall()[0][0]
        except IndexError:
            return None
    
    def inserirRua(self,nomeRua:str,zelador:str):
        ruas = transform(self.cmd.execute(
            """
                SELECT nomeRua from rua where nomeRua = ?;
            """,(nomeRua,)
        ).fetchall())

        if nomeRua not in ruas:
            self.cmd.execute(
                """
                    INSERT INTO rua(idRua,nomeRua,zelador)
                    values(?,?,?);
                """,(self.__getnewID("rua","idRua"),nomeRua,zelador,)
            )
            self.conn.commit()
    
    def buscarDizimista(self,nomeDizimista:str)->list:
        return self.cmd.execute(
            """
                SELECT * from dizimista where nome = ?;
            """,(nomeDizimista,)
        ).fetchall()
    
    def dizimistasRua(self,nomeRua:str)->list:
        infos = self.cmd.execute(
            """
                SELECT nome,nCasa from dizimista
                WHERE nRua = ?;
            """,(nomeRua,)
        ).fetchall()
        return concat(infos)

    def ruasDisponiveis(self)->list:
        return transform(self.cmd.execute(
            """
                SELECT nomeRua from rua;
            """
        ).fetchall())

    def getDizimista(self,nome:str,rua:str,nCasa:str)->tuple:
        try:
            return self.cmd.execute(
                """
                    SELECT * from dizimista
                    where nome = ? and nRua = ? and nCasa = ?
                """,(nome,rua,nCasa,)
            ).fetchall()[0]
        except IndexError:
            return None
    
    def __alterar(self,nomeTabela:str,nomeColuna:str,nomeIdentificador:str,identificador:str,novoAtributo:str):
        self.cmd.execute(
            f"""
                UPDATE {nomeTabela} set {nomeColuna} = ? where {nomeIdentificador} = ?;
            """,(novoAtributo,identificador,)
        )
        self.conn.commit()

    def alterarRua(self,colunas_alterar:list,novosAtributos:list,nomeRua:str):
        try:
            if len(colunas_alterar) == len(novosAtributos):
                for i,coluna in enumerate(colunas_alterar):
                    self.__alterar("rua",coluna,"nomeRua",nomeRua,novosAtributos[i])
                self.conn.commit()
                return True
            return False
        except Exception:
            return False
    
    def alterarMesDoacao(self,nomeDizimista:str,nomeRua:str,nCasa:str,novoMesDoacao:str,antigoMesDoacao:str,anoDoacao_alterar:str):
        try:
            id = self.__getIdDizimista(nomeDizimista,nCasa,nomeRua)
            self.cmd.execute(
                """
                    UPDATE doacao set mesContribuicao = ? where idDizimista = ? and anoContribuicao = ? and mesContribuicao = ?;
                """,(novoMesDoacao,id,anoDoacao_alterar,antigoMesDoacao,)
            )
            self.conn.commit()
            return True
        except Exception:
            return False
    
    def alterarAnoDoacao(self,nomeDizimista:str,nomeRua:str,nCasa:str,novoAnoDoacao:str,antigoAnoDoacao,mesDocao_alterar:str):
        try:
            id = self.__getIdDizimista(nomeDizimista,nCasa,nomeRua)
            self.cmd.execute(
                """
                    UPDATE doacao set anoContribuicao = ? where idDizimista = ? and mesContribuicao = ? and anoContribuicao = ?;
                """,(novoAnoDoacao,id,mesDocao_alterar,antigoAnoDoacao,)
            )
            self.conn.commit()
            return True
        except Exception:
            return False

    def alterarDizimista(self,colunas_alterar:list,novosAtributos:list,nomeDizimista:str,nCasa:str,nomeRua:str)->bool:
        try:
            if len(colunas_alterar) == len(novosAtributos):
                for i,coluna in enumerate(colunas_alterar):
                    self.__alterar("dizimista",coluna,"idDizimista",self.__getIdDizimista(nomeDizimista,nCasa,nomeRua),novosAtributos[i])
                self.conn.commit()
                return True
            return False
        except Exception:
            return False


class BancodeDados_cadastro:
    def __init__(self):
        self.conn = sqlite3.connect(f"{'info'}.db")
        self.cmd = self.conn.cursor()
    
    def criar(self):
        self.cmd.execute(
            """
            CREATE TABLE IF NOT EXISTS cadastro (
                    login varchar(100),
                    senha varchar(100),
                    nome varchar(100) not null,
                    nomeComunidade varchar(100)
                );
            """
        )
        self.conn.commit()

    def inserirCadastro(self,login:str,senha:str,nome:str,nomeComunidade:str)->bool:
        cadastros = transform(self.cmd.execute(
            """
                SELECT login from cadastro where login = ?;
            """,(login,)
        ).fetchall())
        if login not in cadastros:
            self.cmd.execute(
                """
                    INSERT INTO cadastro (login,senha,nome,nomeComunidade)
                    values(?,?,?,?);
                """,(login,senha,nome,nomeComunidade,)
            )
            self.conn.commit()
            return True
        return False

    def login(self,login:str,senha:str)->User:
        info =  self.cmd.execute(
            """
                SELECT nome,nomeComunidade from cadastro where
                login = ? and senha = ?;
            """,(login,senha,)
        ).fetchall()
        if len(info) == 0:
            return None
        info = info[0]
        return User(info[0],info[1])