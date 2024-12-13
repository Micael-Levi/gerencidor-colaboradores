# Sistema de Gestão de Colaboradores

Este é um sistema de gestão de colaboradores e cargos desenvolvido utilizando **Python**, **FastAPI** e **SQLAlchemy**, com persistência de dados em um banco de dados **PostgreSQL**. O projeto foi configurado para rodar em containers utilizando **Docker** e **Docker Compose**.

## Funcionalidades

- **Cadastro de Cargos**
  - Criar, listar, atualizar e excluir cargos.
  - Validações para nome e código do cargo.

- **Cadastro de Colaboradores**
  - Criar, listar, atualizar e excluir colaboradores.
  - Relacionamento com cargos.
  - Vinculação de líder e subordinados.

- **Tratamento de Erros**
  - Tratamento de exceções a nível de banco.

## Padrões de Projeto

Este sistema foi projetado utilizando princípios de organização modular e reutilização de código. Os principais padrões de projeto e boas práticas adotados incluem:

- **Repository Pattern**: A camada de repositórios abstrai a lógica de acesso ao banco de dados, promovendo um design mais limpo e facilitando a manutenção e testes.
- **Separation of Concerns**: Divisão clara entre as responsabilidades de API, modelos, esquemas, e lógica de banco de dados.
- **Dependency Injection**: Uso do `Depends` do FastAPI para gerenciar injeções de dependências, como sessões do banco de dados.
- **Validation Layer**: Validações robustas são implementadas na camada de esquemas utilizando Pydantic, garantindo a integridade dos dados antes de serem processados.


## Tecnologias Utilizadas

- **Linguagem:** Python 3.11
- **Framework Web:** FastAPI
- **ORM:** SQLAlchemy
- **Banco de Dados:** PostgreSQL
- **Gerenciamento de Dependências:** Pipenv
- **Conteinerização:** Docker e Docker Compose

## Pré-requisitos

- **Docker**
- **Docker Compose**
- **Pipenv** (opcional, para rodar localmente sem Docker)

## Configuração

### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# Credenciais do banco de dados
DATABASE_NAME="colaboradores_local"
DATABASE_HOST="db"
DATABASE_PORT="5432"
DATABASE_USER="postgres"
DATABASE_PASSWORD="123"
```

Obs: DATABASE_HOST e DATABASE_PORT devem ter o valor apresentado no exemplo

### 2. Executando com Docker

1. Construa e inicie os containers:
   ```bash
   docker-compose up --build
   ```

2. Acesse a aplicação em: [http://localhost:8000](http://localhost:8000).

3. Documentação interativa do FastAPI: [http://localhost:8000/docs](http://localhost:8000/docs).

### 3. Executando Localmente (Sem Docker)

1. Instale as dependências com **Pipenv**:
   ```bash
   pipenv install
   ```

2. Crie o banco de dados local.

2. Configure as variáveis de ambiente no sistema ou em um arquivo `.env`.

3. Execute a aplicação:
   ```bash
   pipenv run uvicorn app.main:app --reload
   ```

## Testes

1. Execute os testes unitários e de integração:
   ```bash
   docker-compose run app pytest app/tests
   ```

2. Ou localmente (com Pipenv):
   ```bash
   pipenv run pytest app/tests
   ```

