from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from prometheus_flask_exporter import PrometheusMetrics
from sqlalchemy.exc import OperationalError
import os
import time
import logging

# Inicializar o Flask
app = Flask(__name__)

# Configurar o Prometheus Metrics
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Informações sobre o Flask App", version="1.0.0")

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

# Configuração do Banco de Dados
if os.getenv('FLASK_ENV') != 'testing':
    attempts = 5
    for i in range(attempts):
        try:
            with app.app_context():
                db.create_all()
                if not appbuilder.sm.find_user(username='admin'):
                    appbuilder.sm.add_user(
                        username='admin',
                        first_name='Admin',
                        last_name='User',
                        email='admin@admin.com',
                        role=appbuilder.sm.find_role(appbuilder.sm.auth_role_admin),
                        password='admin'
                    )
            logger.info("Banco de dados inicializado com sucesso.")
            break
        except OperationalError:
            if i < attempts - 1:
                logger.warning("Tentativa de conexão com o banco de dados falhou. Tentando novamente...")
                time.sleep(5)
            else:
                logger.error("Não foi possível conectar ao banco de dados após várias tentativas.")
                raise

# Definir modelo
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
    logger.info(f"Aluno {data['nome']} {data['ra']} adicionado com sucesso!")
    return jsonify({'message': 'Aluno adicionado com sucesso!'}), 201

# Rota inicial
@app.route("/")
def index():
    return "Aplicação Flask rodando com métricas no endpoint /metrics"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
