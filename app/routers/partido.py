from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..db import get_db
from ..cruds.partido import (
    crear_partido,
    obtener_partido,
    obtener_partidos,
    actualizar_partido,
    eliminar_partido,
)

router = APIRouter()
@router.get("/")
def get_partidos_endpoint(session: Session = Depends(get_db)):
    return obtener_partidos(session)

@router.get("/{partido_id}")
def get_partido_endpoint(partido_id: int, session: Session = Depends(get_db)):
    partido = obtener_partido(session, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@router.post("/")
def create_partido_endpoint(
    es_bye: bool,
    fase: str,
    categoria: int,
    tipo: str,
    jugador1: int,
    jugador2: Optional[int] = None,
    horario: Optional[datetime] = None,
    session: Session = Depends(get_db)
):
    try:
        return crear_partido(
            session=session,
            es_bye=es_bye,
            fase=fase,
            categoria=categoria,
            tipo=tipo,
            jugador1=jugador1,
            jugador2=jugador2,
            horario=horario,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{partido_id}")
def update_partido_endpoint(
    partido_id: int,
    mesa_id: int,
    es_bye: bool,
    fase: str,
    categoria: int,
    tipo: str,
    jugador1: int,
    jugador2: Optional[int] = None,
    session: Session = Depends(get_db)
):
    partido = obtener_partido(session, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    return actualizar_partido(
        session=session,
        id=partido_id,
        mesa=mesa_id,
        es_bye=es_bye,
        fase=fase,
        categoria=categoria,
        tipo=tipo,
        jugador1=jugador1,
        jugador2=jugador2
    )

@router.delete("/{partido_id}")
def delete_partido_endpoint(partido_id: int, session: Session = Depends(get_db)):
    partido = obtener_partido(session, partido_id)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return eliminar_partido(session, partido_id)