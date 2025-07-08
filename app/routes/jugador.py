# routes/jugador.py
from fastapi import APIRouter, Depends, HTTPException
from ..db import get_db
from ..cruds.jugador import (
    create_jugador, get_jugador, get_jugadores,
    update_jugador, delete_jugador
)

router = APIRouter()

@router.get("/")
def list_jugadores(session=Depends(get_db)):
    return [j.__dict__ for j in get_jugadores(session)]

@router.get("/{jugador_id}")
def read_jugador(jugador_id: int, session=Depends(get_db)):
    j = get_jugador(session, jugador_id)
    if not j: raise HTTPException(404, "Jugador no encontrado")
    return j.__dict__

@router.post("/", status_code=201)
def new_jugador(pais: str, fecha_nacimiento: str, genero: str,
                ciudad: str, asociacion_id: int | None = None,
                session=Depends(get_db)):
    return create_jugador(session, pais=pais,
                          fecha_nacimiento=date.fromisoformat(fecha_nacimiento),
                          genero=genero, ciudad=ciudad,
                          asociacion_id=asociacion_id).__dict__

@router.put("/{jugador_id}")
def mod_jugador(jugador_id: int, pais: str, fecha_nacimiento: str, genero: str,
                ciudad: str, asociacion_id: int | None = None,
                session=Depends(get_db)):
    j = update_jugador(session, jugador_id, pais=pais,
                       fecha_nacimiento=date.fromisoformat(fecha_nacimiento),
                       genero=genero, ciudad=ciudad,
                       asociacion_id=asociacion_id)
    if not j: raise HTTPException(404, "Jugador no encontrado")
    return j.__dict__

@router.delete("/{jugador_id}")
def rem_jugador(jugador_id: int, session=Depends(get_db)):
    j = delete_jugador(session, jugador_id)
    if not j: raise HTTPException(404, "Jugador no encontrado")
    return {"detail": "Jugador eliminado"}
