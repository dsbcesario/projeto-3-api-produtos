from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Helper: gera um token para usar nas rotas protegidas
def obter_token():
    resposta = client.post("/auth/login")
    return resposta.json()["access_token"]

def test_login_gera_token():
    resposta = client.post("/auth/login")
    assert resposta.status_code == 200
    assert "access_token" in resposta.json()

def test_criar_produto():
    token = obter_token()
    headers = {"Authorization": f"Bearer {token}"}
    dados = {"nome": "Notebook", "descricao": "Notebook 16GB", "preco": 3500.0, "quantidade": 10}
    resposta = client.post("/produtos", json=dados, headers=headers)
    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Notebook"
    assert "id" in resposta.json()

def test_listar_produtos():
    resposta = client.get("/produtos")
    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)

def test_buscar_produto_inexistente():
    resposta = client.get("/produtos/999")
    assert resposta.status_code == 404

def test_criar_produto_sem_token():
    dados = {"nome": "Mouse", "preco": 50.0}
    resposta = client.post("/produtos", json=dados)
    assert resposta.status_code == 401