pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "trabalho_devops_app"
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Clonando o repositório...'
                git 'https://github.com/Hemex001/Trabalho_DevOps_-1505031-.git'  // URL do repositório
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Executando testes...'
                sh 'python3 -m unittest discover -s . -p "test_*.py"'
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Construindo imagens Docker...'
                sh 'docker-compose build'
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Subindo os serviços Docker...'
                sh 'docker-compose up -d'
            }
        }

        stage('Verify Monitoring') {
            steps {
                echo 'Verificando monitoramento...'
                sh 'curl -s http://localhost:9090 | grep Prometheus || exit 1'
            }
        }
    }

    post {
        success {
            echo 'Pipeline executada com sucesso!'
        }
        failure {
            echo 'A pipeline falhou!'
        }
    }
}
