from controllers.sql import Banco

from datetime import datetime


class Chat:
    def __init__(self, usuario_id=None, mensagem=None, data_hora=None):
        self.usuario_id = usuario_id  # ID do usuário que está enviando a mensagem
        self.mensagem = mensagem  # Conteúdo da mensagem
        self.data_hora = data_hora
        self.banco = Banco()
        
    def enviar_mensagem(self):
        """
        Envia uma mensagem para o chat
        Args:
            texto (str): Conteúdo da mensagem
        Returns:
            bool: True se enviou com sucesso, False se falhou
        """
        try:

            agora = datetime.now()
            data_formatada = agora.strftime("%Y-%m-%d %H:%M:%S")
            print(data_formatada)

            self.data_hora = data_formatada

            dados = {
                'usuario_id' : self.usuario_id,
                'mensagem': self.mensagem,
                'data_hora' : self.data_hora
				
            }
            self.banco.inserir('chat_usuario', dados)
            print("Usuario.py | Inserir Dados | Cadastrado com sucesso")
        except Exception as e:
            print(f"Erro: {e} ")
            print("Usuario.py | Inserir Dados | Erro ao cadastrar")

    def carregar_mensagens(self):
        """
        Carrega todas as mensagens do chat com informações dos usuários
        Returns:
            list: Lista de mensagens no formato (id, nome_usuario, texto, data_envio)
                  ou lista vazia em caso de erro
        """
        try:
            mensagens = self.banco.consultar_mensagens_com_join()

            print("===================================")

            print(mensagens)

            
            print("Chat | Mensagens carregadas com sucesso")
            return mensagens
        except Exception as e:
            print(f"Chat | Erro ao carregar mensagens: {e}")
            return []