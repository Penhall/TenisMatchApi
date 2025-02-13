from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste isso depois para seus domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "TenisMatch API is running"}

@app.get("/api/v1/health-check")
async def health_check():
    return {"status": "ok", "message": "API is healthy"}