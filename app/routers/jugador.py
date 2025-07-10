from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..db import get_db
from ..cruds.jugador import (
    crear_jugador,
    obtener_jugador,
    obtener_jugadores,
    actualizar_jugador,
    eliminar_jugador,
)

router = APIRouter()

@router.get("/")
def get_jugadores_endpoint(session: Session = Depends(get_db)):
    return obtener_jugadores(session)

@router.get("/{jugador_id}")
def get_jugador_endpoint(jugador_id: int, session: Session = Depends(get_db)):
    jugador = obtener_jugador(session, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@router.post("/")
def create_jugador_endpoint(nombre: str,pais:str , telefono: str,genero: str, ciudad: str,fecha_nacimiento: datetime,session: Session = Depends(get_db)):
    return crear_jugador(session, nombre, pais,telefono, genero,ciudad,fecha_nacimiento)

@router.put("/{jugador_id}")
def update_jugador_endpoint(jugador_id: int, nombre: str,pais:str, telefono: str, ciudad: str, session: Session = Depends(get_db)):
    return actualizar_jugador(session, jugador_id, nombre, pais, telefono, ciudad)

@router.delete("/{jugador_id}")
def delete_jugador_endpoint(jugador_id: int, session: Session = Depends(get_db)):
    return eliminar_jugador(session, jugador_id)
