from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mangum import Mangum

app = FastAPI()

@app.get("/api/test")
async def read_root():
    return {"Hello": "World"}

@app.get("/")
async def root():
    return JSONResponse({"message": "Welcome to FastAPI on Vercel"})

handler = Mangum(app)
