# /backend/app/core/security.py
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
import secrets
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Cria um token de acesso JWT
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access_token",
        "iat": datetime.utcnow()
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
    Verifica e decodifica um token JWT
    """
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.JWTError:
        raise ValueError("Token inválido")

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

def verify_api_key(api_key: str) -> bool:
    """
    Verifica se uma chave de API tem o formato correto
    """
    if not api_key.startswith("tk_"):
        return False
    return len(api_key) >= 45  # tk_ + 32 bytes em base64

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