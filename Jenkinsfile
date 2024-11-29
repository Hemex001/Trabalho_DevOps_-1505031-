pipeline {
    agent any

    stages {
        stage('Clone do Repositório') {
            steps {
                // Clonando o repositório do Git
                checkout scm
            }
        }

        stage('Configurar Ambiente Virtual') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Rodar Testes') {
            steps {
                sh '''
                source venv/bin/activate
                python -m unittest discover -s . -p "test_*.py"
                '''
            }
        }

        stage('Build de Imagens Docker') {
            steps {
                // Build das imagens Docker
                sh 'docker-compose -f docker-compose.yml build'
            }
        }

        stage('Deploy') {
            steps {
                // Subindo os serviços Docker
                sh 'docker-compose -f docker-compose.yml up -d'
            }
        }

        stage('Verificar Monitoramento') {
            steps {
                // Validando que o Prometheus está rodando corretamente
                script {
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:9090", returnStdout: true).trim()
                    if (response != "200") {
                        error "Prometheus não está acessível. Código HTTP: ${response}"
                    }
                }
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
