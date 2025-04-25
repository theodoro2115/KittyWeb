import sqlite3

class Banco:
    def __init__(self):
        self.conexao = None
        self.cursor = None

    def conectar(self):
        self.conexao = sqlite3.connect("models/chatWeb.db")
        self.cursor = self.conexao.cursor()

    def desconectar(self):
        if self.conexao:
            self.conexao.close()

    def inserir(self, tabela, dados: dict):
        self.conectar()
        colunas = ", ".join(dados.keys())
        valores = ", ".join(['?'] * len(dados))
        lista = list(dados.values())

        sql = f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})"
        self.cursor.execute(sql, lista)
        self.conexao.commit()
        self.desconectar()

    def consultar(self, tabela):
        self.conectar()
        sql = f"SELECT * FROM {tabela}"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.desconectar()
        return resultado
    
    def consultar_mensagens_com_join(self):
        self.conectar()
        sql = f"select chat.chat_id, usuario.nome_completo, chat.mensagem, strftime('%d/%m/%Y - %Hh:%M', chat.data_hora) AS data_formatada from chat_usuario as chat join tb_usuario as usuario on (chat.usuario_id = usuario.usuario_id)"
        #sql= "SELECT * FROM chat_usuario"
        self.cursor.execute(sql)
        resultado = self.cursor.fetchall()
        self.desconectar()
        print("=======================")
        print(resultado)
        return resultado