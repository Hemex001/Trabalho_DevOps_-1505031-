from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from prometheus_client import generate_latest, CollectorRegistry, multiprocess
from prometheus_client import Counter, Histogram
import os
import time
import logging

# Inicializar o Flask
app = Flask(__name__)

# Configuração do Flask
app.config['SECRET_KEY'] = 'minha_chave_secreta_super_secreta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if os.getenv('FLASK_ENV') == 'testing':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mariadb/school_db'

# Inicializar banco de dados e AppBuilder
db = SQLAlchemy(app)
appbuilder = AppBuilder(app, db.session)

# Configuração do Monitoramento Prometheus
registry = CollectorRegistry()
multiprocess.MultiProcessCollector(registry)

# Métricas customizadas
REQUEST_COUNT = Counter(
    "flask_app_requests_total", "Total de requisições recebidas", ["method", "endpoint"]
)
REQUEST_LATENCY = Histogram(
    "flask_app_request_latency_seconds", "Latência das requisições", ["method", "endpoint"]
)

# Middleware para medir métricas
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    REQUEST_COUNT.labels(request.method, request.path).inc()
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.method, request.path).observe(latency)
    return response

# Endpoint `/metrics`
@app.route('/metrics')
def metrics():
    return Response(generate_latest(registry), mimetype="text/plain")

# Modelo Aluno
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    ra = db.Column(db.String(50), nullable=False)

# Configurar views do AppBuilder
class AlunoModelView(ModelView):
    datamodel = SQLAInterface(Aluno)
    list_columns = ['id', 'nome', 'ra']

appbuilder.add_view(
    AlunoModelView,
    "Lista de Alunos",
    icon="fa-folder-open-o",
    category="Alunos"
)

# Rotas para Alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    output = [{'id': aluno.id, 'nome': aluno.nome, 'ra': aluno.ra} for aluno in alunos]
    return jsonify(output)

@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    data = request.get_json()
    novo_aluno = Aluno(nome=data['nome'], ra=data['ra'])
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201

# Rota inicial
@app.route("/")
def index():
    return "Aplicação Flask rodando com métricas no endpoint /metrics"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
