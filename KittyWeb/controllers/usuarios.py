from controllers.sql import Banco

class Usuario:
    def __init__(self, nome_completo = None,  nome_usuario = None, senha = None ):
        self.nome_completo = nome_completo
        self.nome_usuario = nome_usuario
        self.senha = senha
      
        self.banco = Banco()

    def inserir_dados(self):
        try:
            dados = {
                'nome_completo' : self.nome_completo,
                'nome_usuario': self.nome_usuario,
                'senha' : self.senha
				
            }
            self.banco.inserir('tb_usuario', dados)
            print("Usuario.py | Inserir Dados | Cadastrado com sucesso")
        except Exception as e:
            print(f"Erro: {e} ")
            print("Usuario.py | Inserir Dados | Erro ao cadastrar")