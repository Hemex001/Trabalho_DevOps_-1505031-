import unittest
from app import app, db, Aluno

class TestApp(unittest.TestCase):
    def setUp(self):
        # Configuração inicial para o banco de dados em memória (para testes)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Limpar o banco de dados após os testes
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_cadastrar_aluno(self):
        # Dados do aluno a serem cadastrados
        aluno_data = {
            "nome": "João",
            "ra": "1775235"
        }
        # Fazendo o POST para cadastrar o aluno
        response = self.app.post('/alunos', json=aluno_data)
        self.assertEqual(response.status_code, 201)

        # Verificando se o aluno foi salvo no banco de dados
        with app.app_context():
            aluno = Aluno.query.filter_by(ra="1775235").first()
            self.assertIsNotNone(aluno)
            self.assertEqual(aluno.nome, "João")

if __name__ == '__main__':
    unittest.main()
