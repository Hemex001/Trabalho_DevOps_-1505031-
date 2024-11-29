import os
import unittest
from app import app, db, Aluno

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Definir o ambiente como 'testing'
        os.environ['FLASK_ENV'] = 'testing'

    def setUp(self):
        # Configurar o banco de dados em memória
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Limpar o banco de dados após cada teste
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_cadastrar_aluno(self):
        with app.app_context():
            aluno = Aluno(nome="Teste", ra="12345")
            db.session.add(aluno)
            db.session.commit()

            aluno_salvo = Aluno.query.filter_by(ra="12345").first()
            self.assertIsNotNone(aluno_salvo)
            self.assertEqual(aluno_salvo.nome, "Teste")

if __name__ == '__main__':
    unittest.main()
