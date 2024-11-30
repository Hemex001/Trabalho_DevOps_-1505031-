from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from prometheus_flask_exporter import PrometheusMetrics
import os
import time
import logging

# Inicializar o Flask
app = Flask(__name__)
metrics = PrometheusMetrics(app)  # Exponha métricas no endpoint /metrics
# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

# Configuração do Flask
app.config['SECRET_KEY'] = 'minha_chave_secreta_super_secreta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if os.getenv('FLASK_ENV') == 'testing':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mariadb/school_db'

# Inicializar o banco de dados e AppBuilder
db = SQLAlchemy(app)
appbuilder = AppBuilder(app, db.session)

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.route('/metrics')
def custom_metrics():
    return metrics.do_expose_metrics()

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
    logger.info(f"Aluno {data['nome']} {data['ra']} adicionado com sucesso!")
    return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
