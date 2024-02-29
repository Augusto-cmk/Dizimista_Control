import sqlite3
from datetime import datetime

class LOGGER:
    def __init__(self,lado:str):
        self.conn = sqlite3.connect("logs.db")
        self.cmd = self.conn.cursor()
        self.lado = lado
        self.criar()
    
    def criar(self):
        self.cmd.execute(
            """
            CREATE TABLE IF NOT EXISTS LOG (
                    data DATETIME,
                    log varchar(100),
                    tipo varchar(100),
                    metodo varchar(100),
                    lado varchar(100)
                );
            """
        )
        self.conn.commit()
    
    def inserirLOG(self,metodo:str,log:str,tipo:str)->bool:
        data = datetime.now()
        self.cmd.execute(
            """
                INSERT INTO LOG (lado,metodo,data,log,tipo)
                values(?,?,?,?,?);
            """,(self.lado,metodo,data,log,tipo,)
        )
        self.conn.commit()
        return True