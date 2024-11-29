pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "pipeline2"
    }

    stages {
        stage('Clone Repositório') {
            steps {
                echo 'Clonando o código do repositório...'
                checkout scm
            }
        }

        stage('Build Imagens Docker') {
            steps {
                echo 'Criando imagens Docker...'
                sh '''
                    docker-compose build
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Subindo o ambiente...'
                sh '''
                    docker-compose up -d --no-recreate
                '''
            }
        }

    stage('Rodar Testes') {
        steps {
            echo 'Executando testes da aplicação...'
            sh '''
                docker-compose up flask-tests --build --abort-on-container-exit
                docker-compose rm -f flask-tests || true
            '''
        }
    }

        stage('Verificar Monitoramento') {
            steps {
                echo 'Verificando se Prometheus está ativo...'
                sh '''
                    curl -f http://localhost:9090 || exit 1
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizada.'
        }
        success {
            echo 'Pipeline concluída com sucesso!'
        }
        failure {
            echo 'Pipeline falhou.'
        }
    }
}
