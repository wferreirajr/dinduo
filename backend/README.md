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
git clone [url-do-repositorio]
cd backend
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

## Contribuindo

1. Fork o projeto
2. Crie sua Feature Branch
3. Commit suas mudanças
4. Push para a Branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT.

## Contato

[Wilson Ferreira Junior] - [wilson.f.jr@gmail.com] Link do projeto: https://github.com/wferreirajr/dinduo Nota: Nunca compartilhe chaves secretas ou credenciais no código fonte ou no README.