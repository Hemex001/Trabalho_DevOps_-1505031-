pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "flask_app"
    }

    stages {
        stage('Clone Repositório') {
            steps {
                echo 'Clonando o código do repositório...'
                checkout scm
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
