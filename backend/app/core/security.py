# /backend/app/core/security.py
from datetime import datetime, timedelta
from typing import Any, Union
import secrets
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    """
    Cria um token de acesso JWT
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    
    # Usando secrets para gerar token seguro
    token = secrets.token_urlsafe(32)
    return token

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Gera hash seguro para uma senha
    """
    return pwd_context.hash(password)

def create_api_key() -> str:
    """
    Gera uma chave de API segura
    """
    return f"tk_{secrets.token_urlsafe(32)}"

def sanitize_filename(filename: str) -> str:
    """
    Sanitiza nome de arquivo para evitar path traversal
    """
    return ''.join(c for c in filename if c.isalnum() or c in '._-')

def rate_limit_key(request) -> str:
    """
    Gera chave para rate limiting baseada no IP
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip = forwarded.split(",")[0]
    else:
        ip = request.client.host
    return f"ratelimit:{ip}"

def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> bool:
    """
    Valida tamanho do arquivo (padrão: 10MB)
    """
    return file_size <= max_size

def validate_file_type(content_type: str, allowed_types: list = None) -> bool:
    """
    Valida tipo do arquivo
    """
    if allowed_types is None:
        allowed_types = ['text/csv', 'application/vnd.ms-excel']
    return content_type in allowed_types