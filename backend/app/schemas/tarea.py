from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.prioridad import PrioridadOut
from app.schemas.estado import EstadoOut


class TareaBase(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=100, examples=["Comprar leche"])
    descripcion: Optional[str] = Field(None, max_length=2000, examples=["Ir al súper por la tarde"])
    prioridad_id: UUID
    estado_id: UUID


class TareaCreate(TareaBase):
    pass


class TareaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=2000)
    prioridad_id: Optional[UUID] = None
    estado_id: Optional[UUID] = None


class TareaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    titulo: str
    descripcion: Optional[str]
    prioridad_id: UUID
    estado_id: UUID
    fecha_creacion: datetime
    fecha_modificacion: datetime


class TareaOutDetallada(TareaOut):
    prioridad: PrioridadOut
    estado: EstadoOut