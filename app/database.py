# conexão com o PostgreSQL

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# A URL de conexão vem da variável de ambiente (definida no docker-compose)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/produtos"
)

# O "motor" que liga o Python ao PostgreSQL
engine = create_engine(DATABASE_URL)

# Fábrica de sessões: cada requisição usa uma sessão para falar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos (tabelas) que vamos criar no models.py
class Base(DeclarativeBase):
    pass

# Dependência do FastAPI: abre uma sessão por requisição e fecha no final
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()