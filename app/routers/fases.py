from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..cruds.fases import (
    crear_fase,
    obtener_fase,
    obtener_fases,
    actualizar_fase,
    eliminar_fase,
)

router = APIRouter()

@router.get("/")
def get_fases(session: Session = Depends(get_db)):
    return obtener_fases(session)

@router.get("/{fase_id}")
def get_fase(fase_id: int, session: Session = Depends(get_db)):
    fase = obtener_fase(session, fase_id)
    if not fase:
        raise HTTPException(status_code=404, detail="Fase no encontrada")
    return fase

@router.post("/")
def create_fase(tipo: str, nombre: str, torneo_id: int, partido_id: int, session: Session = Depends(get_db)):
    return crear_fase(session, tipo, nombre, torneo_id, partido_id)

@router.put("/{fase_id}")
def update_fase(fase_id: int, tipo: str, nombre: str, torneo_id: int, partido_id: int, session: Session = Depends(get_db)):
    return actualizar_fase(session, fase_id, tipo, nombre, torneo_id, partido_id)

@router.delete("/{fase_id}")
def delete_fase(fase_id: int, session: Session = Depends(get_db)):
    return eliminar_fase(session, fase_id)
