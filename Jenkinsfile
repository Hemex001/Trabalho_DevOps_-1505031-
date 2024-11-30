pipeline {
    agent any

    environment {
        DOCKER_IMAGE_FLASK = "flask_app_image"
        DOCKER_IMAGE_MARIADB = "mariadb_image"
    }

    stages {
        stage('Clone do Repositório') {
            steps {
                echo 'Clonando o repositório do Git...'
                checkout scm
            }
        }

        stage('Rodar Testes') {
            steps {
                echo 'Executando testes unitários...'
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                FLASK_ENV=testing python -m unittest discover -s . -p "test_*.py"
                '''
            }
        }

        stage('Build de Imagens Docker') {
            steps {
                echo 'Criando imagens Docker...'
                sh '''
                docker-compose down || true
                docker-compose build
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Fazendo deploy da aplicação...'
                sh '''
                docker-compose down || true
                docker-compose up -d
                '''
            }
        }

        stage('Verificar Monitoramento') {
            steps {
                echo 'Verificando o status do monitoramento...'
                sh '''
                echo "Verificando Prometheus..."
                status=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:9090/-/ready)
                if [ "$status" -ne 200 ]; then
                    echo "Prometheus não está acessível. Código HTTP: $status"
                    exit 1
                fi
                '''
                echo 'Prometheus está funcionando corretamente.'
            }
        }
    }

    post {
        always {
            echo 'Pipeline concluído. Verifique os resultados nos logs acima.'
        }
        success {
            echo 'Pipeline executado com sucesso! Aplicação e monitoramento estão operacionais.'
        }
        failure {
            echo 'Pipeline falhou. Verifique os erros nos logs.'
        }
    }
}
