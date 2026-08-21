from fastapi.testclient import TestClient
from app.main import app
from datetime import timedelta
from app.auth import criar_token_acesso

client = TestClient(app)

# Helper: gera um token para usar nas rotas protegidas
def obter_token():
    """Faz login e retorna o token JWT, usado nas rotas protegidas."""
    resposta = client.post("/auth/login")
    return resposta.json()["access_token"]

# Teste do login
def test_login_gera_token():
    """Verifica se o endpoint /auth/login responde 200 e devolve um access_token."""
    resposta = client.post("/auth/login")
    assert resposta.status_code == 200
    assert "access_token" in resposta.json()

# Teste de criação de produto
def test_criar_produto():
    """Cria um produto autenticado e confere se responde 201 com o nome e o id."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"}
    dados = {"nome": "Notebook", "descricao": "Notebook 16GB", "preco": 3500.0, "quantidade": 10}
    resposta = client.post("/produtos", json=dados, headers=headers)
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Notebook"
    assert "id" in resposta.json()

# Teste de listagem de produtos
def test_listar_produtos():
    """Lista os produtos e confere se a resposta é 200 e uma lista."""
    resposta = client.get("/produtos")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)

# Teste de busca de produto inexistente
def test_buscar_produto_inexistente():
    """Busca um produto com id que não existe e espera 404."""
    resposta = client.get("/produtos/999")
    assert resposta.status_code == 404

# Teste de criação sem token
def test_criar_produto_sem_token():
    """Tenta criar um produto sem token e espera 401 (não autorizado)."""
    dados = {"nome": "Mouse", "preco": 50.0}
    resposta = client.post("/produtos", json=dados)
    assert resposta.status_code == 401

# Teste de atualização de produto
def test_atualizar_produto():
    """Cria um produto e depois atualiza, conferindo se os novos dados foram salvos."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Cria um produto para depois atualizar
    dados = {"nome": "Teclado", "preco": 150.0, "quantidade": 5}
    criado = client.post("/produtos", json=dados, headers=headers).json()
    produto_id = criado["id"]

    # Atualiza o produto
    novos_dados = {"nome": "Teclado Mecânico", "preco": 250.0, "quantidade": 8}
    resposta = client.put(f"/produtos/{produto_id}", json=novos_dados, headers=headers)
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Teclado Mecânico"
    assert resposta.json()["preco"] == 250.0

# Teste de atualização de produto inexistente
def test_atualizar_produto_inexistente():
    """Tenta atualizar um produto que não existe e espera 404."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"}
    dados = {"nome": "X", "preco": 1.0}
    resposta = client.put("/produtos/999", json=dados, headers=headers)
    assert resposta.status_code == 404

# Teste de exclusão de produto
def test_deletar_produto():
    """Cria um produto e depois o exclui, conferindo se responde 204."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"}

    dados = {"nome": "Mouse", "preco": 50.0, "quantidade": 3}
    criado = client.post("/produtos", json=dados, headers=headers).json()
    produto_id = criado["id"]

    resposta = client.delete(f"/produtos/{produto_id}", headers=headers)
    assert resposta.status_code == 204

# Teste de exclusão de produto inexistente
def test_deletar_produto_inexistente():
    """Tenta excluir um produto que não existe e espera 404."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"}
    resposta = client.delete("/produtos/999", headers=headers)
    assert resposta.status_code == 404

# Teste de token inválido
def test_token_invalido():
    """Envia um token inválido e espera 401 (cobre o except do auth.py)."""
    headers = {"Authorization": "Bearer token-invalido"}
    dados = {"nome": "Produto", "preco": 10.0}
    resposta = client.post("/produtos", json=dados, headers=headers)
    assert resposta.status_code == 401

def test_criar_token_com_expiracao_personalizada():
    """Chama criar_token_acesso com expires_delta explícito (cobre o if)."""
    token = criar_token_acesso({"sub": "teste"}, expires_delta=timedelta(minutes=5))
    assert isinstance(token, str)
    assert len(token) > 0

def test_buscar_produto_existente():
    """Cria um produto e depois o busca pelo id, conferindo se retorna 200 e os dados."""
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Cria um produto para depois buscar
    dados = {"nome": "Monitor", "preco": 900.0, "quantidade": 4}
    criado = client.post("/produtos", json=dados, headers=headers).json()
    produto_id = criado["id"]

    # Busca o produto criado
    resposta = client.get(f"/produtos/{produto_id}")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Monitor"
    assert resposta.json()["id"] == produto_id