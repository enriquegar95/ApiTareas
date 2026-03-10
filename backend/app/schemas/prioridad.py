# app/schemas/prioridad.py
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class PrioridadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    nombre: str