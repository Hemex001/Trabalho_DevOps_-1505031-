pipeline {
    agent any

    stages {
        stage('Clonar Repositório') {
            steps {
                echo 'Clonando o repositório...'
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[url: 'https://github.com/Hemex001/Trabalho_DevOps_-1505031-.git']]
                ])
            }
        }

        stage('Construir') {
            steps {
                echo 'Construindo o projeto...'
                sh 'echo "Simulação de build"'
            }
        }
    }
}
