# /backend/app/api/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_api_key
)
from app.api.deps import get_current_active_user
from app.schemas.users import UserCreate, UserResponse, Token, APIKey
from app.database.session import get_db
from app.database.models import User

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
    description="Cria um novo usuário com email e senha"
)
async def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    # Verifica se email já existe
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já registrado"
        )
    
    # Cria novo usuário
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        api_key=create_api_key()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post(
    "/token",
    response_model=Token,
    summary="Login para obter token",
    description="Realiza login com email e senha para obter token JWT"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Autentica usuário
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se usuário está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    # Atualiza último login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Gera token JWT
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email,
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post(
    "/api-key",
    response_model=APIKey,
    summary="Gerar nova API Key",
    description="Gera uma nova API Key para o usuário atual"
)
async def generate_api_key(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Gera nova API key
    current_user.api_key = create_api_key()
    db.commit()
    
    return {
        "api_key": current_user.api_key,
        "created_at": datetime.utcnow()
    }

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Dados do usuário atual",
    description="Retorna os dados do usuário autenticado"
)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user