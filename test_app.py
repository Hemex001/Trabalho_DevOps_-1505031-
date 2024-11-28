import unittest
import json
from app import app, db, Aluno

class TestAlunoMariaDB(unittest.TestCase):
    def setUp(self):
        # Configurar o banco de dados para o contêiner MariaDB
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mariadb/school_db'
        app.config['TESTING'] = True
        self.app = app.test_client()

        # Criar as tabelas no banco
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Limpar o banco de dados após cada teste
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_adicionar_aluno(self):
        aluno_data = {
            'nome': 'Teste',
            'sobrenome': 'Teste 2',
            'turma': '3B',
            'disciplinas': 'Teste'
        }
        response = self.app.post('/alunos', data=json.dumps(aluno_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Aluno adicionado com sucesso!', response.data)

        # Verificar no banco de dados
        with app.app_context():
            aluno = Aluno.query.filter_by(ra='654321').first()
            self.assertIsNotNone(aluno)
            self.assertEqual(aluno.nome, 'Teste')

if __name__ == '__main__':
    unittest.main()
