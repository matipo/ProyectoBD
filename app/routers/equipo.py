from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..cruds.equipo import (
    crear_equipo,
    obtener_equipo,
    obtener_equipos,
    actualizar_equipo,
    eliminar_equipo,
)

router = APIRouter()

@router.get("/")
def get_equipos(session: Session = Depends(get_db)):
    return obtener_equipos(session)

@router.get("/{equipo_id}")
def get_equipo(equipo_id: int, session: Session = Depends(get_db)):
    equipo = obtener_equipo(session, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@router.post("/")
def create_equipo(nombre: str, jugador1: int, jugador2: int, categoria: int, session: Session = Depends(get_db)):
    return crear_equipo(session, nombre, jugador1, jugador2, categoria)

@router.put("/{equipo_id}")
def update_equipo(equipo_id: int, nombre: str, jugador1: int, jugador2: int, session: Session = Depends(get_db)):
    return actualizar_equipo(session, equipo_id, nombre, jugador1, jugador2)

@router.delete("/{equipo_id}")
def delete_equipo(equipo_id: int, session: Session = Depends(get_db)):
    return eliminar_equipo(session, equipo_id)

