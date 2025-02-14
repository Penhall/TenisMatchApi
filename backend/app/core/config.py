# /backend/app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from typing import Optional, List

class Settings(BaseSettings):
    # API configs
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TenisMatch API"
    DEBUG: bool = True
    
    # Database configs
    DATABASE_URL: str = "sqlite:///./tennis_match.db"
    
    # ML Model configs
    MODEL_PATH: str = "data/models/tennis_match_model.joblib"
    
    # CORS configs
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    # Security configs
    SECRET_KEY: str = "93125b70b6c8c4f319cd36c7a941ea1505fc24e138b94e946946a0c7a0e494c9"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas para desenvolvimento
    ALGORITHM: str = "HS256"
    
    # API Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # File upload configs
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_UPLOAD_TYPES: List[str] = ["text/csv", "application/vnd.ms-excel"]
    
    # ML Model configs
    MODEL_PATH: str = "./data/models/tennis_match_model.joblib" 
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()