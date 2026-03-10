from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db  # <- si tu get_db está en otro sitio, cambia este import
from app.models.tarea import Tarea
from app.models.prioridad import Prioridad
from app.models.estado import Estado
from app.schemas.tarea import TareaCreate, TareaOut, TareaOutDetallada, TareaUpdate

router = APIRouter(prefix="/tareas", tags=["Tareas"])


def _validar_prioridad_y_estado(db: Session, prioridad_id: UUID, estado_id: UUID) -> None:
    existe_prioridad = db.query(Prioridad.id).filter(Prioridad.id == prioridad_id).first()
    if not existe_prioridad:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"prioridad_id no existe: {prioridad_id}",
        )

    existe_estado = db.query(Estado.id).filter(Estado.id == estado_id).first()
    if not existe_estado:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"estado_id no existe: {estado_id}",
        )


@router.get("", response_model=list[TareaOutDetallada])
def listar_tareas(db: Session = Depends(get_db)) -> list[TareaOutDetallada]:
    tareas = (
        db.query(Tarea)
        .options(joinedload(Tarea.prioridad), joinedload(Tarea.estado))
        .order_by(Tarea.fecha_creacion.desc())
        .all()
    )
    return tareas


@router.get("/{tarea_id}", response_model=TareaOutDetallada)
def obtener_tarea(tarea_id: UUID, db: Session = Depends(get_db)) -> TareaOutDetallada:
    tarea = (
        db.query(Tarea)
        .options(joinedload(Tarea.prioridad), joinedload(Tarea.estado))
        .filter(Tarea.id == tarea_id)
        .first()
    )
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea


@router.post("", response_model=TareaOut, status_code=status.HTTP_201_CREATED)
def crear_tarea(payload: TareaCreate, db: Session = Depends(get_db)) -> TareaOut:
    _validar_prioridad_y_estado(db, payload.prioridad_id, payload.estado_id)

    tarea = Tarea(
        titulo=payload.titulo,
        descripcion=payload.descripcion,
        prioridad_id=payload.prioridad_id,
        estado_id=payload.estado_id,
    )
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return TareaOut.model_validate(tarea)


@router.patch("/{tarea_id}", response_model=TareaOut)
def actualizar_tarea(tarea_id: UUID, payload: TareaUpdate, db: Session = Depends(get_db)) -> TareaOut:
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    data = payload.model_dump(exclude_unset=True)

    # Si vienen ids, los validamos (pero soportando actualización parcial)
    prioridad_id = data.get("prioridad_id", tarea.prioridad_id)
    estado_id = data.get("estado_id", tarea.estado_id)
    _validar_prioridad_y_estado(db, prioridad_id, estado_id)

    for k, v in data.items():
        setattr(tarea, k, v)

    db.commit()
    db.refresh(tarea)
    return TareaOut.model_validate(tarea)


@router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_tarea(tarea_id: UUID, db: Session = Depends(get_db)) -> None:
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    db.delete(tarea)
    db.commit()
    return None