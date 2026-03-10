# app/schemas/estado.py
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class EstadoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nombre: str