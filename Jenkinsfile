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
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Rodar Testes') {
            steps {
                sh '''
                echo "Criando ambiente virtual..."
                python3 -m venv venv
                echo "Ativando ambiente virtual..."
                . venv/bin/activate
                echo "Instalando dependências..."
                pip install -r requirements.txt
                echo "Executando testes..."
                FLASK_ENV=testing python -m unittest discover -s . -p "test_*.py"
                echo "Testes concluídos!"
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
                sh '''
                echo "Parando e removendo containers existentes..."
                docker-compose -f docker-compose.yml down || true
                echo "Subindo novos containers..."
                docker-compose -f docker-compose.yml up -d
                '''
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
