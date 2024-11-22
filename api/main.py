from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from .database import engine, Base
import sys

app = FastAPI(
    title="Transactions API v1",
    description="API para análise de transações",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Erro ao criar tabelas: {e}")
    sys.exit(1)

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Transactions API is running",
        "version": "1.0.0",
        "docs": "/api/v1/docs",
        "redoc": "/api/v1/redoc"
    }

@app.get("/health")
async def health_check():
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "version": "1.0.0",
            "database": "connected",
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
