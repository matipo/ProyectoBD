# routes/equipo.py
from fastapi import APIRouter, Depends, HTTPException
from ..db import get_db
from ..cruds.equipo import (
    create_equipo, get_equipo, get_equipos,
    update_equipo, delete_equipo
)

router = APIRouter()

@router.get("/")
def list_equipos(session=Depends(get_db)):
    return [e.__dict__ for e in get_equipos(session)]

@router.get("/{equipo_id}")
def read_equipo(equipo_id: int, session=Depends(get_db)):
    e = get_equipo(session, equipo_id)
    if not e: raise HTTPException(404, "Equipo no encontrado")
    return e.__dict__

@router.post("/", status_code=201)
def new_equipo(nombre_equipo: str, categoria_id: int, session=Depends(get_db)):
    return create_equipo(session, nombre_equipo=nombre_equipo,
                         categoria_id=categoria_id).__dict__

@router.put("/{equipo_id}")
def mod_equipo(equipo_id: int, nombre_equipo: str, categoria_id: int,
               session=Depends(get_db)):
    e = update_equipo(session, equipo_id, nombre_equipo=nombre_equipo,
                      categoria_id=categoria_id)
    if not e: raise HTTPException(404, "Equipo no encontrado")
    return e.__dict__

@router.delete("/{equipo_id}")
def rem_equipo(equipo_id: int, session=Depends(get_db)):
    e = delete_equipo(session, equipo_id)
    if not e: raise HTTPException(404, "Equipo no encontrado")
    return {"detail": "Equipo eliminado"}
