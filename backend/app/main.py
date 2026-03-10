from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.db.database import SessionLocal
from app.db.seed import seed_catalogos
import app.db.base  # noqa: F401

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_catalogos(db)
    finally:
        db.close()
    yield


docs_url = "/docs"
redoc_url = "/redoc"

if settings.environment == "production":
    docs_url = None
    redoc_url = None

app = FastAPI(
    title="API Tareas",
    lifespan=lifespan,
    docs_url=docs_url,
    redoc_url=redoc_url,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://api-tareas-chi.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")