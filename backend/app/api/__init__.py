# /backend/app/api/__init__.py
from fastapi import APIRouter
from app.api.routes import router as tennis_router
from app.api.auth_routes import router as auth_router

# Criar router principal
api_router = APIRouter()

# Incluir os routers específicos
api_router.include_router(auth_router, prefix="/api/v1")
api_router.include_router(tennis_router, prefix="/api/v1")