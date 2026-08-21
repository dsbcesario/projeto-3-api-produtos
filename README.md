# API de Gerenciamento de Produtos

API REST completa para cadastro e gerenciamento de produtos, com
autenticação, persistência em PostgreSQL e execução via Docker.

## 🎯 Objetivo
Demonstrar construção de API profissional: modelagem de dados, CRUD,
autenticação, validação e containerização.

## 🛠️ Tecnologias
- Python 3.12 + FastAPI
- SQLAlchemy (ORM)
- PostgreSQL 16
- Docker + Docker Compose
- JWT (autenticação)

## 📂 Estrutura
├── app/
│   ├── main.py            # Ponto de entrada da API
│   ├── models.py          # Modelos do banco de dados
│   ├── schemas.py         # Validação de entrada/saída
│   ├── auth.py            # Autenticação JWT
│   └── database.py        # Conexão com o banco
├── tests/
│   └── test_produtos.py   # Testes da API
├── docker-compose.yml     # Sobe API + banco juntos
├── Dockerfile
├── .env.example
├── conftest.py
├── README.md
└── requirements.txt


## 🚀 Como rodar
1. Copie o arquivo de ambiente:
   cp .env.example .env
2. Suba a aplicação e o banco:
   docker compose up --build
3. Acesse a documentação automática:
   http://localhost:8000/docs

## 🔐 Endpoints principais
- POST /auth/login → gera token JWT
- POST /produtos → cria produto (autenticado)
- GET /produtos → lista produtos
- GET /produtos/{id} → busca produto
- PUT /produtos/{id} → atualiza produto
- DELETE /produtos/{id} → remove produto

## 🧪 Testes
docker compose exec api pytest --cov=app