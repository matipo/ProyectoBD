from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
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
    inicio_inscripcion: date,
    fin_inscripcion: date,
    inicio_competencia: date,
    fin_competencia: date,
    mesas_disponibles: int,
    session: Session = Depends(get_db),
):
    return crear_torneo(
        session,
        nombre,
        inicio_inscripcion,
        fin_inscripcion,
        inicio_competencia,
        fin_competencia,
        mesas_disponibles
    )

@router.put("/{torneo_id}")
def update_torneo(
    torneo_id: int,
    nombre: str,
    inicio_inscripcion: date,
    fin_inscripcion: date,
    inicio_competencia: date,
    fin_competencia: date,
    mesas_disponibles: int,
    session: Session = Depends(get_db),
):
    torneo = actualizar_torneo(
        session,
        torneo_id,
        nombre,
        inicio_inscripcion,
        fin_inscripcion,
        inicio_competencia,
        fin_competencia,
        mesas_disponibles
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
