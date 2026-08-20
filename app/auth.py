import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Chave secreta vem do ambiente (definida no .env / docker-compose)
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-super-segura")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Diz ao FastAPI onde o token é enviado (no header Authorization)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Cria o token JWT
def criar_token_acesso(dados: dict, expires_delta: Optional[timedelta] = None):
    dados_copia = dados.copy()
    if expires_delta:
        expira = datetime.now(timezone.utc) + expires_delta
    else:
        expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_copia.update({"exp": expira})
    token = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Valida o token e retorna os dados do usuário
def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )