# /backend/app/core/exceptions.py
from typing import Any, Dict, Optional
from fastapi import HTTPException

class TenisMatchException(HTTPException):
    """
    Exceção base para erros da API
    """
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class CredentialsException(TenisMatchException):
    """
    Erro de credenciais inválidas
    """
    def __init__(
        self,
        detail: str = "Credenciais inválidas",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=401,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"} if headers is None else headers
        )

class PermissionDeniedException(TenisMatchException):
    """
    Erro de permissão negada
    """
    def __init__(
        self,
        detail: str = "Permissão negada",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=403, detail=detail, headers=headers)

class ResourceNotFoundException(TenisMatchException):
    """
    Erro de recurso não encontrado
    """
    def __init__(
        self,
        detail: str = "Recurso não encontrado",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=404, detail=detail, headers=headers)

class ValidationException(TenisMatchException):
    """
    Erro de validação de dados
    """
    def __init__(
        self,
        detail: str = "Erro de validação",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=422, detail=detail, headers=headers)

class DatabaseException(TenisMatchException):
    """
    Erro relacionado ao banco de dados
    """
    def __init__(
        self,
        detail: str = "Erro no banco de dados",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=500, detail=detail, headers=headers)

class FileUploadException(TenisMatchException):
    """
    Erro no upload de arquivo
    """
    def __init__(
        self,
        detail: str = "Erro no upload do arquivo",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=400, detail=detail, headers=headers)

class ModelTrainingException(TenisMatchException):
    """
    Erro no treinamento do modelo
    """
    def __init__(
        self,
        detail: str = "Erro no treinamento do modelo",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=500, detail=detail, headers=headers)

class RateLimitException(TenisMatchException):
    """
    Erro de limite de requisições excedido
    """
    def __init__(
        self,
        detail: str = "Limite de requisições excedido",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=429,
            detail=detail,
            headers={"Retry-After": "60"} if headers is None else headers
        )