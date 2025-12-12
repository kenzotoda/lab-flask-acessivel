# Ferramentas: Flask (web framework), SQLAlchemy (ORM), os (gerenciar ambiente)
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

# Inicialização do Flask
app = Flask(__name__)

# Configuração do Banco de Dados (PostgreSQL)
# Entrada: URL de conexão (Requisito de Confiabilidade)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:29062003@localhost:5432/todolist_db'
)

# Configuração de Segurança (OWASP A05: Security Misconfiguration)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'chave_super_secreta_para_flash_msgs')

# Inicializa o ORM SQLAlchemy
db = SQLAlchemy(app)

# Modelo de Dados (ORM)
class Tarefa(db.Model):
    # LGPD: Minimização de Dados (apenas o necessário)
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    concluida = db.Column(db.Boolean, default=False)
    
    # Saída: Representação do objeto para debug
    def __repr__(self):
        return f'<Tarefa {self.id}: {self.titulo}>'

# Rota Principal (Entrada: GET /; Saída: render_template com dados)
@app.route('/')
def index():
    # Consulta ao DB: Obtém todas as tarefas (Saída do ORM)
    todas_tarefas = Tarefa.query.all()
    # Saída para a web: Renderiza o HTML, passando a lista de objetos Tarefa
    return render_template('index.html', tarefas=todas_tarefas)

if __name__ == '__main__':
    # Bloco para criar as tabelas no PostgreSQL (Executar uma vez)
    # python -> from app import app, db -> with app.app_context(): db.create_all()
    app.run(debug=True)
