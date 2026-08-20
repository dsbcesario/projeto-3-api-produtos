from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import engine, get_db, Base

# Cria as tabelas no banco (se ainda não existirem)
Base.metadata.create_all(bind=engine)

# Instância do FastAPI
app = FastAPI(title="API de Produtos")

# Rota de login: gera o token JWT
@app.post("/auth/login")
def login():
    token = auth.criar_token_acesso({"sub": "usuario"})
    return {"access_token": token, "token_type": "bearer"}

# Rota protegida: cria um produto (exige token)
@app.post("/produtos", response_model=schemas.Produto, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: schemas.ProdutoCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(auth.verificar_token),
):
    novo = models.Produto(**produto.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

# Lista todos os produtos (pública)
@app.get("/produtos", response_model=list[schemas.Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(models.Produto).all()

# Busca um produto por id (pública)
@app.get("/produtos/{produto_id}", response_model=schemas.Produto)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

# Atualiza um produto (protegida)
@app.put("/produtos/{produto_id}", response_model=schemas.Produto)
def atualizar_produto(
    produto_id: int,
    dados: schemas.ProdutoCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(auth.verificar_token),
):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for campo, valor in dados.model_dump().items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto

# Deleta um produto (protegida)
@app.delete("/produtos/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(auth.verificar_token),
):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()