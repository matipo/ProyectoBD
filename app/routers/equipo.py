from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import datetime
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
def get_equipos_endpoint(session: Session = Depends(get_db)):
    return obtener_equipos(session)

@router.get("/{equipo_id}")
def get_equipo_endpoint(equipo_id: int, session: Session = Depends(get_db)):
    equipo = obtener_equipo(session, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    
    return {
    "id": equipo.id,
    "nombre_equipo": equipo.nombre_equipo,
    "categoria": equipo.categoria,
    "jugador1": {
        "id": equipo.jugadores[0].id,
        "nombre": equipo.jugadores[0].nombre
    } if equipo.jugadores else None,
    "jugador2": {
        "id": equipo.jugadores2[0].id,
        "nombre": equipo.jugadores2[0].nombre
    } if equipo.jugadores2 else None
}



@router.post("/")
def create_equipo_endpoint(
    nombre_equipo: str,
    jugadores: int,
    jugadores2: int,
    categoria: int,
    session: Session = Depends(get_db)
):
    equipo = crear_equipo(
            session,
            nombre_equipo,
            jugadores,
            jugadores2,
            categoria,
        )
    return equipo

@router.put("/{equipo_id}")
def update_equipo_endpoint(
    equipo_id: int,
    nombre_equipo: Optional[str] = None,
    jugadores: Optional[int] = None,
    jugadores2: Optional[int] = None,
    categoria: Optional[int] = None,
    session: Session = Depends(get_db)
):
    try:
        equipo_actualizado = actualizar_equipo(
            session, equipo_id, categoria, nombre_equipo, jugadores, jugadores2
        )
        if not equipo_actualizado:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        return equipo_actualizado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{equipo_id}")
def delete_equipo_endpoint(equipo_id: int, session: Session = Depends(get_db)):
    return eliminar_equipo(session, equipo_id)

def get_equipos(session: Session = Depends(get_db)):
    return obtener_equipos(session)

