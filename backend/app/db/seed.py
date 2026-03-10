from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

import app.db.base  # noqa: F401  # asegura que los modelos queden registrados

from app.models.estado import Estado
from app.models.prioridad import Prioridad

PRIORIDADES_BASE = ["Baja", "Media", "Alta", "Urgente"]
ESTADOS_BASE = ["Pendiente", "En Progreso", "En Pausa", "Completada"]


def seed_prioridades(db: Session) -> None:
    existentes = set(
        db.scalars(select(Prioridad.nombre).where(Prioridad.nombre.in_(PRIORIDADES_BASE))).all()
    )
    faltan = [n for n in PRIORIDADES_BASE if n not in existentes]
    if faltan:
        db.add_all([Prioridad(nombre=n) for n in faltan])


def seed_estados(db: Session) -> None:
    existentes = set(
        db.scalars(select(Estado.nombre).where(Estado.nombre.in_(ESTADOS_BASE))).all()
    )
    faltan = [n for n in ESTADOS_BASE if n not in existentes]
    if faltan:
        db.add_all([Estado(nombre=n) for n in faltan])


def seed_catalogos(db: Session) -> None:
    try:
        seed_prioridades(db)
        seed_estados(db)
        db.commit()
    except Exception:
        db.rollback()
        raise