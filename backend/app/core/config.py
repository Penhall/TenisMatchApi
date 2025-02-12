# /backend/app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from typing import Optional

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
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()