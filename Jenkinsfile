pipeline {
    agent any

    environment {
        COMPOSE_PROJECT_NAME = "pipeline2" // Prefixo único para evitar conflitos
    }

    stages {
        stage('Clone Repositório') {
            steps {
                echo 'Clonando o código do repositório...'
                checkout scm
            }
        }

        stage('Parar e Remover Containers Existentes') {
            steps {
                echo 'Removendo containers existentes...'
                sh '''
                    docker-compose down || true
                '''
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

        stage('Subir o Ambiente') {
            steps {
                echo 'Subindo o ambiente completo...'
                sh '''
                    docker-compose up -d
                '''
            }
        }

        stage('Rodar Testes') {
            steps {
                echo 'Executando testes da aplicação...'
                sh '''
                    docker-compose up flask-tests --abort-on-container-exit
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

        stage('Verificar Grafana') {
            steps {
                echo 'Verificando se Grafana está ativo...'
                sh '''
                    curl -f http://localhost:3000 || exit 1
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizada.'
            sh '''
                docker-compose down || true
            '''
        }
        success {
            echo 'Pipeline concluída com sucesso!'
        }
        failure {
            echo 'Pipeline falhou.'
        }
    }
}
