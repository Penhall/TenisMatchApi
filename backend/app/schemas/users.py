# /backend/app/schemas/users.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """
    Schema base para dados do usuário
    """
    email: EmailStr = Field(..., description="Email do usuário")

class UserCreate(UserBase):
    """
    Schema para criação de usuário
    """
    password: str = Field(
        ..., 
        min_length=8,
        description="Senha do usuário (mínimo 8 caracteres)"
    )

class UserUpdate(BaseModel):
    """
    Schema para atualização de usuário
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """
    Schema de resposta com dados do usuário
    """
    id: int = Field(..., description="ID único do usuário")
    is_active: bool = Field(..., description="Status do usuário")
    created_at: datetime = Field(..., description="Data de criação")

    class Config:
        from_attributes = True

class Token(BaseModel):
    """
    Schema para token de acesso
    """
    access_token: str = Field(..., description="Token de acesso JWT")
    token_type: str = Field(..., description="Tipo do token")

class TokenData(BaseModel):
    """
    Schema para dados contidos no token
    """
    email: Optional[str] = None
    expires_at: Optional[datetime] = None

class APIKey(BaseModel):
    """
    Schema para chave de API
    """
    api_key: str = Field(..., description="Chave de API")
    created_at: datetime = Field(..., description="Data de criação")
    last_used: Optional[datetime] = Field(None, description="Último uso")