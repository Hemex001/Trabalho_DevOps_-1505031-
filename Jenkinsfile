pipeline {
    agent any

    stages {
        stage('Clone do Repositório') {
            steps {
                // Clonando o repositório do Git
                checkout scm
            }
        }

        stage('Instalação de Dependências') {
            steps {
                // Instalando as dependências do Python
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Rodar Testes') {
            steps {
                // Rodando os testes com unittest
                sh 'python -m unittest discover -s . -p "test_*.py"'
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
            // Limpando containers após execução (opcional)
            sh 'docker-compose -f docker-compose.yml down || true'
        }
        success {
            echo 'Pipeline executada com sucesso!'
        }
        failure {
            echo 'Falha na pipeline. Verifique os logs.'
        }
    }
}
