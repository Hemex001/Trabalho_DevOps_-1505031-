# **Projeto DevOps - Trabalho**

**Aluno**: Hemerson da Costa Lacovic
**RA**: 1505031

---

## **Descrição**

Este projeto é uma aplicação web construída com Flask, Docker, Prometheus, Grafana e Jenkins. Ele utiliza Jenkins para automatizar o fluxo de CI/CD, incluindo testes, build, deploy e monitoramento.


---

## **Pré-requisitos**

1. **Jenkins** instalado e em execução.
2. **Docker** e **Docker Compose** configurados no ambiente do Jenkins.
3. Acesso ao navegador para visualizar o Grafana no endereço `http://localhost:3000`.

---

## **Passos para Configurar e Executar o Projeto**

### **1. Iniciar o Jenkins**
   - Certifique-se de que o Jenkins está em execução. Normalmente, ele estará disponível em `http://localhost:8080`.

---

### **2. Criar uma Nova Pipeline no Jenkins**

1. **Acessar o Jenkins**
   - Vá até o Jenkins em `http://localhost:8080` e faça login.

2. **Criar uma nova Pipeline**
   - Clique em **"Nova Tarefa"**.
   - Digite um nome para o pipeline, como `Pipeline-Grafana`.
   - Selecione a opção **"Pipeline"** e clique em **"OK"**.

3. **Configurar o Pipeline**
   - Na página de configuração do pipeline:
     - Role até a seção **Pipeline** e selecione a opção **Pipeline Script from SCM**.

4. **Configurar Repositório SCM**
   - Em **SCM**, selecione **Git**.
   - Insira o repositório Git onde o projeto está hospedado: `https://github.com/Hemex001/Trabalho_DevOps_-1505031-.git`.
   - Configure as credenciais, se necessário.
   - Clique em **Salvar**.

---

### **3. Executar o Pipeline**

1. Volte para a página inicial do Jenkins e clique na pipeline recém-criada.
2. Clique em **"Construir Agora"** para iniciar o pipeline.
3. Monitore a execução:
   - Acompanhe os logs para verificar se os containers Docker (Prometheus, Grafana) foram provisionados corretamente.

---

### **4. Acessar o Grafana**

1. Abra o navegador e vá para `http://localhost:3000`.
2. Faça login no Grafana:
   - **Usuário**: `admin`  
   - **Senha**: `admin` (ou a configurada no ambiente).
3. Verifique o dashboard provisionado automaticamente e visualize as métricas de requisições.

---

## **Resumo dos Passos**

1. Certifique-se de que o Jenkins está rodando.
2. Crie uma nova pipeline no Jenkins seguindo as instruções acima.
3. Execute a pipeline.
4. Acesse o Grafana em `http://localhost:3000` e explore o dashboard.

---
