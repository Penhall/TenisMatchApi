# /backend/app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.config import settings
from app.database.session import get_db
from app.database.models import User
from app.core.security import verify_password
from app.schemas.users import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Valida o token JWT e retorna o usuário atual
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica o token JWT
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        
        # Valida expiração
        expires_at = datetime.fromtimestamp(payload.get("exp", 0))
        if datetime.utcnow() > expires_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado"
            )
            
        token_data = TokenData(email=email, expires_at=expires_at)
    except JWTError:
        raise credentials_exception
        
    # Busca usuário no banco
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário inativo"
        )
        
    return user

async def verify_api_key(
    api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db)
) -> User:
    """
    Valida a chave de API e retorna o usuário
    """
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key inválida"
        )
    
    # Atualiza último uso
    user.last_login = datetime.utcnow()
    db.commit()
    
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependência para garantir que o usuário está ativo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    return current_user