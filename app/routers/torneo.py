from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional
from ..db import get_db
from ..cruds.torneo import (
    crear_torneo,
    obtener_torneo,
    obtener_torneos,
    actualizar_torneo,
    eliminar_torneo,
)

router = APIRouter()

@router.get("/")
def get_torneos(session: Session = Depends(get_db)):
    return obtener_torneos(session)

@router.get("/{torneo_id}")
def get_torneo(torneo_id: int, session: Session = Depends(get_db)):
    torneo = obtener_torneo(session, torneo_id)
    if not torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return torneo

@router.post("/")
def create_torneo(
    nombre: str,
    fechas_inscripcion: date,
    fecha_competencia: date,
    mesas_requeridas: int,
    session: Session = Depends(get_db),
):
    try:
        return crear_torneo(
            session,
            nombre,
            fechas_inscripcion,
            fecha_competencia,
            mesas_requeridas,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{torneo_id}")
def update_torneo(
    torneo_id: int,
    nombre: str,
    fechas_inscripcion: date,
    fecha_competencia: date,
    mesas_requeridas: int,
    session: Session = Depends(get_db),
):
    
    torneo = actualizar_torneo(
        session,
        torneo_id,
        nombre,
        fechas_inscripcion,
        fecha_competencia,
        mesas_requeridas
    )
    if not torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return torneo

@router.delete("/{torneo_id}")
def delete_torneo(torneo_id: int, session: Session = Depends(get_db)):
    torneo = eliminar_torneo(session, torneo_id)
    if not torneo:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return {"detail": "Torneo eliminado correctamente"}
