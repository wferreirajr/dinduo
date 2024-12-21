# DinDuo API

Uma API REST desenvolvida com FastAPI para gerenciamento de usuários e contas financeiras.

## Descrição

DinDuo é uma API que oferece funcionalidades para gerenciamento de usuários, contas, cartões e despesas, com autenticação JWT e testes automatizados.

## Tecnologias Utilizadas

- Python 3.12+
- FastAPI
- SQLAlchemy
- SQLite
- Poetry (Gerenciamento de dependências)
- JWT (JSON Web Tokens)
- Pytest (Testes automatizados)

## Principais Dependências

- `fastapi`: Framework web moderno e rápido
- `sqlalchemy`: ORM para banco de dados
- `python-jose[cryptography]`: Implementação JWT
- `passlib[bcrypt]`: Hashing de senhas
- `pytest`: Framework de testes
- `python-multipart`: Suporte a form-data
- `uvicorn`: Servidor ASGI

## Instalação

Clone o repositório:

```bash
git clone https://github.com/wferreirajr/dinduo
cd dinduo/backend
```

Instale o Poetry (se ainda não tiver):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Instale as dependências:

```bash
poetry install
```

Configure as variáveis de ambiente criando um arquivo `.env`:

```text
SECRET_KEY=sua_chave_secreta_aqui
```

## Executando a API

```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Documentação da API

Acesse a documentação interativa em:

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Endpoints Principais

### Autenticação

- `POST /api/v1/users/token`: Obter token JWT
- `POST /api/v1/users/`: Criar novo usuário

### Usuários

- `GET /api/v1/users/`: Listar usuários
- `GET /api/v1/users/{user_id}`: Obter usuário específico
- `PUT /api/v1/users/{user_id}`: Atualizar usuário
- `DELETE /api/v1/users/{user_id}`: Deletar usuário

## Segurança

- Autenticação via JWT (JSON Web Tokens)
- Senhas hasheadas com bcrypt
- Proteção contra CSRF
- Validação de dados com Pydantic
- Chaves secretas gerenciadas via variáveis de ambiente

## Testes

Execute os testes com:

```bash
poetry run pytest
```

## Estrutura do Projeto

```text
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── account.py
│   │   │   └── user.py
│   │   ├── __init__.py
│   │   └── models/
│   │       ├── account.py
│   │       ├── card.py
│   │       ├── category.py
│   │       ├── expense.py
│   │       ├── __init__.py
│   │       └── user.py
│   ├── core/
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── __init__.py
│   │   └── security.py
│   ├── db/
│   │   ├── database.py
│   │   └── __init__.py
│   └── main.py
├── conftest.py
├── create-db-tables.sql
├── pyproject.toml
├── README.md
└── tests
    └── test_user.py

```

## Desenvolvimento

Crie uma branch para sua feature:

```bash
git checkout -b feature/nova-funcionalidade
```

Execute os testes antes de commitar:

```bash
poetry run pytest
```

Mantenha o código formatado:

```bash
poetry run black .
```

## Sequência de Inicialização

1. **main.py** - Ponto de entrada da aplicação
    - Inicializa a aplicação FastAPI
    - Configura as rotas principais
    - Cria as tabelas do banco de dados
    - Define configurações globais da API

2. **core/config.py** - Carregado durante a inicialização
    - Define configurações globais
    - Carrega variáveis de ambiente
    - Estabelece constantes do sistema

## Detalhamento dos Diretórios e Arquivos

### 1. /app/core/
**config.py**
```python
# Configurações globais da aplicação
# Variáveis de ambiente
# Configurações de segurança (SECRET_KEY, ALGORITHM)
# URLs base e versão da API
```

**auth.py**
```python
# Gerenciamento de autenticação
# Funções para criar e validar tokens JWT
# Dependências de autenticação
# Verificação de usuários
```

**security.py**
```python
# Funções de segurança
# Hash de senhas
# Verificação de senhas
# Funções auxiliares de segurança
```

### 2. /app/db/
**database.py**
```python
# Configuração do banco de dados
# Conexão com SQLAlchemy
# Sessão do banco de dados
# Base para modelos ORM
```

### 3. /app/api/models/
**user.py, account.py, card.py, category.py, expense.py**
```python
# Modelos SQLAlchemy
# Definição das tabelas do banco de dados
# Relacionamentos entre tabelas
# Estrutura dos dados
```

### 4. /app/api/endpoints/
**user.py**
```python
# Rotas relacionadas a usuários
# CRUD de usuários
# Autenticação
# Gerenciamento de perfil
```

**account.py**
```python
# Rotas relacionadas a contas
# CRUD de contas
# Operações financeiras
# Gerenciamento de saldo
```

### 5. /tests/
**test_user.py**
```python
# Testes automatizados
# Testes de endpoints
# Testes de autenticação
# Verificações de CRUD
```

## Fluxo de Execução

1. **Inicialização**
```python
# main.py carrega as configurações
# Configura o banco de dados (database.py)
# Inicializa os modelos (models/*.py)
# Registra as rotas (endpoints/*.py)
```

2. **Requisição**
```python
# Cliente faz requisição
# Middleware de autenticação (auth.py)
# Rota específica (endpoints/*.py)
# Interação com banco de dados (models/*.py)
# Resposta ao cliente
```

## Arquivos de Configuração

**pyproject.toml**
- Dependências do projeto
- Configurações do Poetry
- Metadados do projeto

**conftest.py**
- Configurações globais de teste
- Fixtures do pytest
- Configurações de ambiente de teste

**create-db-tables.sql**
- Scripts SQL para criação inicial do banco
- Estrutura base do banco de dados

## Arquivos de Inicialização

**__init__.py**
- Tornam os diretórios módulos Python
- Podem conter inicializações específicas
- Facilitam importações

Esta estrutura segue o padrão de uma aplicação FastAPI moderna, com separação clara de responsabilidades e organização modular.


## Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch
3. Commit suas mudanças
4. Push para a Branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.

## Contato

Nome: Wilson Ferreira Junior  
E-mail: wilson.f.jr@gmail.com  
Link do projeto: [https://github.com/wferreirajr/dinduo](https://github.com/wferreirajr/dinduo)  
Nota: Nunca compartilhe chaves secretas ou credenciais no código fonte ou no README.

## Reconhecimentos

Este projeto foi desenvolvido por Wilson Ferreira Junior com assistência de ferramentas de IA, incluindo Perplexity AI, que forneceu orientações e sugestões durante o processo de desenvolvimento.
