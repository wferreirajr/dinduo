COomando para executar o servidor:
poetry run uvicorn app.main:app --reload 

1. Criar um Usuário (POST)
curl -X POST http://localhost:8000/api/v1/users \
     -H "Content-Type: application/json" \
     -d '{"email": "testuser@example.com", "password": "password123"}'

2. Listar Usuários (GET)
curl http://localhost:8000/api/v1/users

3. Obter um Usuário Específico (GET)
curl http://localhost:8000/api/v1/users/1

4. Atualizar um Usuário (PUT)
curl -X PUT http://localhost:8000/api/v1/users/1 \
     -H "Content-Type: application/json" \
     -d '{"email": "updated@example.com"}'

5. Deletar um Usuário (DELETE)
curl -X DELETE http://localhost:8000/api/v1/users/1
