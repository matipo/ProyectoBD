from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..cruds.jugador import (
    create_participante,
    get_participante,
    get_participantes,
    actualizar_participante,
    eliminar_participante,
)

router = APIRouter()

@router.get("/")
def get_jugadores(session: Session = Depends(get_db)):
    return get_participantes(session)

@router.get("/{jugador_id}")
def get_jugador(jugador_id: int, session: Session = Depends(get_db)):
    jugador = get_participante(session, jugador_id)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@router.post("/")
def create_jugador(nombre: str, email: str, telefono: str, ciudad: str, session: Session = Depends(get_db)):
    return create_participante(session, nombre, email, telefono, ciudad)

@router.put("/{jugador_id}")
def update_jugador(jugador_id: int, nombre: str, email: str, telefono: str, ciudad: str, session: Session = Depends(get_db)):
    return actualizar_participante(session, jugador_id, nombre, email, telefono, ciudad)

@router.delete("/{jugador_id}")
def delete_jugador(jugador_id: int, session: Session = Depends(get_db)):
    return eliminar_participante(session, jugador_id)
