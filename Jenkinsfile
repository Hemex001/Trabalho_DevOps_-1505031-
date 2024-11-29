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

        stage('Parar Containers Existentes') {
            steps {
                echo 'Parando containers existentes...'
                sh '''
                    docker-compose down || true
                '''
            }
        }

        stage('Build Imagens Docker') {
            steps {
                echo 'Construindo imagens Docker...'
                sh '''
                    docker-compose build
                '''
            }
        }

        stage('Subir Containers') {
            steps {
                echo 'Iniciando containers...'
                sh '''
                    docker-compose up -d
                '''
            }
        }

        stage('Verificar Serviços') {
            steps {
                echo 'Verificando se todos os serviços estão ativos...'
                sh '''
                    docker ps
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finalizado.'
        }
        success {
            echo 'Pipeline concluído com sucesso!'
        }
        failure {
            echo 'Pipeline falhou. Verifique os logs.'
        }
    }
}
