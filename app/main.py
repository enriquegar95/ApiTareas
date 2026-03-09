from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.database import SessionLocal
from app.db.seed import seed_catalogos
import app.db.base  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        seed_catalogos(db)
    finally:
        db.close()
    yield


app = FastAPI(title="API Tareas", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")