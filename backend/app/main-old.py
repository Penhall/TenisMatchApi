# /backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.core.config import settings
from app.database.session import create_tables
from app.api.routes import router as api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para matching de tênis usando Machine Learning",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(api_router, prefix=settings.API_V1_STR)

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