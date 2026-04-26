<div align="center">
  <h1>⛅ Weather Data Engineering Pipeline</h1>
  <p><i>Um pipeline ETL automatizado de ponta a ponta para dados climáticos usando Apache Airflow e PostgreSQL.</i></p>
  
  <p>
    <img src="https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Apache_Airflow-017CEE?style=for-the-badge&logo=Apache-Airflow&logoColor=white" alt="Airflow" />
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
    <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white" alt="Jupyter" />
  </p>
</div>

---

## 📖 Sobre o Projeto

Este projeto consiste em uma arquitetura de dados completa para **extrair, transformar e carregar (ETL)** dados climáticos da cidade de Campinas/SP. Todo o fluxo de dados é orquestrado de forma automatizada pelo **Apache Airflow**, armazenado de forma estruturada e relacional em um banco de dados **PostgreSQL** e, posteriormente, consumido por **Jupyter Notebooks** para análises exploratórias e geração de insights visuais.

### 🎯 Objetivos Principais
- 🔄 **Automação:** Orquestrar rotinas de coleta de dados de APIs externas sem necessidade de intervenção humana.
- 🧹 **Qualidade de Dados:** Limpar, normalizar atributos e tratar dados de data/hora (timestamps) antes da persistência.
- 💾 **Armazenamento Seguro:** Salvar os dados processados garantindo integridade em um banco relacional robusto.
- 📊 **Análise Visual:** Facilitar o acesso aos dados para cientistas/analistas identificarem tendências climáticas, como picos de temperatura e sazonalidades.

---

## ⚙️ Arquitetura do Pipeline

O fluxo dos dados segue o padrão moderno de ETL, estruturado nas seguintes etapas:

1. **🌐 Extract (`extract_data.py`):** Consome informações do clima através de requisições HTTP para uma API externa.
2. **🛠️ Transform (`transform_data.py`):** Utiliza bibliotecas modernas como o `pandas` para normalizar colunas, lidar com valores nulos e estruturar tipos de dados corretamente.
3. **🗄️ Load (`load_data.py`):** Utiliza `SQLAlchemy` para carregar o DataFrame processado na nossa camada de armazenamento dentro do **PostgreSQL**.
4. **⏳ Orquestração (`weather_dag.py`):** O **Airflow** coordena todas essas etapas como tarefas em um Grafo Direcionado Acíclico (DAG), executando-as em horários programados.
5. **📈 Análise (`notebooks/`):** Consumo direto do banco de dados no Jupyter para exploração e visualização.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
| :--- | :--- |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="30" height="30"/> **Python 3** | Linguagem central para o desenvolvimento dos scripts ETL e exploração de dados. |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" width="30" height="30"/> **Pandas** | Processamento rápido, manipulação de tabelas e transformações avançadas. |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="30" height="30"/> **PostgreSQL** | SGBD Relacional escolhido para servir como Data Warehouse/Storage. |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apache/apache-original.svg" width="30" height="30"/> **Apache Airflow** | Ferramenta padrão de mercado para orquestração e monitoramento de DAGs. |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="30" height="30"/> **Docker** | Isolamento de ambiente com `docker-compose` gerindo Airflow e DB. |
| <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jupyter/jupyter-original.svg" width="30" height="30"/> **Jupyter** | Criação de relatórios e visualizações ricas a partir do DB. |

---

## 📁 Estrutura do Repositório

```text
engenharia_dados/
│
├── 📂 dags/                   # DAGs do Apache Airflow
│   └── weather_dag.py         # Arquivo de definição do fluxo e steps
│
├── 📂 src/                    # Código-fonte principal (Camada ETL)
│   ├── extract_data.py        # Regras de acesso a API e requests
│   ├── transform_data.py      # Transformações pesadas e limpezas (Pandas)
│   └── load_data.py           # Conexão e injeção massiva de dados no Postgres
│
├── 📂 notebooks/              # Área de Análise de Dados
│   ├── analise_campinas.ipynb # Notebook com insights de negócio e gráficos
│   └── analysis_data.ipynb    # Explorações preliminares locais
│
├── 📂 config/                 # Variáveis de ambiente sensíveis
│   └── .env                   # Senhas, credenciais e configurações
├── 📂 data/                   # Armazenamento temporário de dados parciais
│
├── docker-compose.yaml        # Manifesto Docker de toda a infraestrutura
├── pyproject.toml             # Configurações de projeto e dependências (uv/pip)
└── uv.lock                    # Arquivo de lock do gerenciador 'uv'
```

---

## 🚀 Como Executar o Projeto

### 1️⃣ Pré-requisitos
- **Docker** e **Docker Compose** devem estar rodando na sua máquina.
- (Recomendado) Gerenciador de pacotes **uv** ou um ambiente virtual ativo com Python 3.

### 2️⃣ Configuração do Ambiente
Crie um arquivo `.env` na raiz do projeto (ou verifique os da pasta `config/`) contendo suas variáveis:
```ini
# Configuração de Banco de Dados
DB_HOST=postgres
DB_USER=airflow
DB_PASSWORD=airflow
DB_NAME=weather_db

# Chave da API Climática
API_KEY=sua_chave_secreta_aqui
```

### 3️⃣ Subindo a Infraestrutura (Airflow + Banco)
Abra seu terminal na pasta do projeto e inicie os containers em background:
```bash
docker-compose up -d
```
*Dica: Na primeira vez, o Docker baixará as imagens necessárias. Isso pode levar alguns minutos.*

### 4️⃣ Acessando e Rodando o Airflow
Abra a interface administrativa web do Airflow no seu navegador:
- 🔗 **Acesso:** [http://localhost:8080](http://localhost:8080)
- 👤 **Usuário:** `airflow`
- 🔑 **Senha:** `airflow`

1. Na lista, localize a DAG chamada `weather_dag`.
2. Clique no botão de *Toggle* (Unpause) no canto esquerdo.
3. Clique no botão de *Play* (Trigger DAG) no lado direito para iniciar o processo de extração.

---

## 📊 Visualização de Dados

Depois que o pipeline rodar com sucesso e o banco PostgreSQL for alimentado, você pode investigar os resultados! 

Acesse a pasta `notebooks/` e abra o `analise_campinas.ipynb` em seu Jupyter/VSCode. Os dados gerarão gráficos que respondem:
- 📈 **Tendências de Temperatura:** Evolução do clima em Campinas (Máximas e Mínimas).
- 🌧️ **Outras Métricas:** Quaisquer cruzamentos de humidade ou pressão atmosférica relevantes.

---

<div align="center">
  <p>Feito com ☕, 🐍 Python e muita Engenharia de Dados!</p>
</div>