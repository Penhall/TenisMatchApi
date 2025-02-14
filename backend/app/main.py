# /backend/app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.database.session import create_tables, SessionLocal
from app.database.init_db import create_default_users
from app.api.routes import router as api_router
from app.api.auth_routes import router as auth_router
from app.core.exceptions import TenisMatchException
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código de inicialização
    create_tables()
    db = SessionLocal()
    try:
        create_default_users(db)
    finally:
        db.close()
    
    yield  # Aqui a aplicação está rodando
    
    # Código de encerramento (cleanup)
    # Por exemplo, fechar conexões de banco, etc.

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para matching de tênis usando Machine Learning",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging e tratamento de erros
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        return JSONResponse(
            status_code=500,
            content={"detail": str(e), "process_time": process_time}
        )

# Handler para exceções customizadas
@app.exception_handler(TenisMatchException)
async def tenis_match_exception_handler(request: Request, exc: TenisMatchException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Incluir rotas
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)

# Criar tabelas no startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Customização do OpenAPI para melhorar documentação Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        description="""
        TenisMatch API - Sistema de matching de tênis utilizando Machine Learning.
        
        ## Autenticação
        * JWT Token via /auth/token
        * API Key via header X-API-Key
        
        ## Funcionalidades
        * Upload e análise de datasets
        * Treinamento de modelos
        * Predições de matching
        * Gerenciamento de dados
        
        ## Ambientes
        * Desenvolvimento: {settings.API_V1_STR}
        * Documentação: /docs
        * ReDoc: /redoc
        """,
        routes=app.routes,
    )
    
    # Adiciona componentes de segurança ao schema
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        },
        "apiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
async def root():
    return {
        "message": "TenisMatch API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_version": "1.0.0",
        "env": "development" if settings.DEBUG else "production"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)