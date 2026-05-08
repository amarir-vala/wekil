# backend/main.py
from fastapi import FastAPI
from backend.routers.webhook import router

app = FastAPI(title="Wekil API", version="0.1.0")

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Wekil is running"}