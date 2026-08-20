from pydantic import BaseModel, ConfigDict
from typing import Optional

# Schema de entrada: o que o cliente envia ao criar/atualizar um produto
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade: int = 0

# Usado na criação (POST)
class ProdutoCreate(ProdutoBase):
    pass

# Usado na resposta (o que a API devolve, incluindo o id)
class Produto(ProdutoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)