from flask import Flask, Blueprint, request, jsonify, render_template, redirect, session
from flask_socketio import SocketIO, emit
from controllers.sql import Banco
from controllers.chat import Chat
import os

from controllers.usuarios import Usuario

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'
app.config['banco_de_dados'] = 'models/chatWeb.db'
UPLOAD_FOLDER = 'static/assets/avatar'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

socketio = SocketIO(app)  # Inicializa o Socket.IO

# -------------------- Funções Banco de Dados --------------------

# Função para obter a conexão com o banco
def get_db_connection():
    banco = Banco()  # Cria a instância da classe Banco
    banco.conectar()  # Conecta ao banco
    return banco

# Função para carregar todas as mensagens
def carregar_todas_mensagens():
    banco = get_db_connection()
    mensagens = banco.consultar_mensagens_com_join()
    print(mensagens)  # Aqui você consulta as mensagens da tabela 'chat_usuario'
    banco.desconectar()
    return mensagens

# -------------------- Rotas --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario')
        senha = request.form.get('senha')
        banco = get_db_connection()
        cursor = banco.cursor
        cursor.execute("SELECT * FROM tb_usuario WHERE nome_usuario = ? AND senha = ?", (nome_usuario, senha))
        usuario = cursor.fetchone()
        banco.desconectar()
        if usuario:
            session['usuario_id'] = usuario[0]  # Supondo que o ID do usuário seja o primeiro campo
            session['nome_usuario'] = usuario[1]  # Supondo que o nome do usuário seja o segundo campo
            return redirect('/chat')
        else:
            return "Usuário ou senha incorretos."
    return render_template('entrar.html')

@app.route('/chat')
def chat():    
    
    if 'usuario_id' not in session:
        return redirect('/login')
    
    chat_obj = Chat()
    mensagens = chat_obj.carregar_mensagens()
  
    print(f"Nome do usuário: {mensagens}")
    
    return render_template('chatzinho.html', mensagens=mensagens, usuario_id=session['usuario_id']) 

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':

        usuario = Usuario()

        usuario.nome_completo = request.form.get('nome_completo')
        usuario.nome_usuario = request.form.get('nome_usuario')
        usuario.senha = request.form.get('senha')

        try:
            usuario.inserir_dados()
            socketio.emit('novo_usuario')

            return redirect('/')  
        
        except Exception as e:
            return render_template('erro.html', erro="Impossível cadastrar o usuário")
      
        # avatar = request.files.get('avatar')

        # banco = get_db_connection()
        # cursor = banco.cursor
      
        # cursor.execute("SELECT * FROM tb_usuario WHERE nome_usuario = ?", (nome_usuario,))
       
        # if cursor.fetchone():
        #     banco.desconectar()
        #     return "Usuário já existe."

        
        # if avatar and avatar.filename:
        #     extensao = avatar.filename.split('.')[-1]
        #     nome_avatar = f"{nome_usuario.lower().replace(' ', '_')}.{extensao}"
        #     caminho_avatar = os.path.join(app.config['UPLOAD_FOLDER'], nome_avatar)
        #     avatar.save(caminho_avatar)

            

        # cursor.execute("INSERT INTO tb_usuario (nome_completo, nome_usuario, senha, avatar) VALUES (?, ?, ?, ?)",(nome_completo, nome_usuario, senha, nome_avatar))
        
        # banco.conectar()
        # banco.desconectar()
        
        return redirect('/login')

    return render_template('cadastro.html')

# -------------------- Socket.IO --------------------

@app.route('/mensagem', methods=['POST', 'GET'])
def enviar():
    chat_obj = Chat()

    if request.method == 'POST':
        mensagem = request.form.get('mensagem')
        
        usuario_id = request.form.get('usuario_id')
        chat_obj.mensagem = mensagem
        chat_obj.usuario_id = usuario_id
        
        chat_obj.enviar_mensagem()     
        
        socketio.emit('atualizar_lista')
    
     #   mensagens = chat_obj.carregar_mensagens()

    return redirect('/chat')

# -------------------- Execução --------------------

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=80, debug=True)