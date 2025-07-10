from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..cruds.inscripciones import (
    crear_inscripcion,
    obtener_inscripcion,
    obtener_inscripciones,
    actualizar_inscripcion,
    eliminar_inscripcion,
)

router = APIRouter()

@router.get("/{inscripcion_id}/{categoria_id}")
def get_inscripcion(inscripcion_id: int, categoria_id: int, session: Session = Depends(get_db)):
    inscripcion = obtener_inscripcion(session, inscripcion_id, categoria_id)
    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return inscripcion

@router.get("/")
def get_inscripciones(session: Session = Depends(get_db)):
    return obtener_inscripciones(session)


@router.post("/")
def create_inscripcion(id: int, categoria_id: int, torneo_id: int, jugador_id: int, equipo_id: int, session: Session = Depends(get_db)):
    return crear_inscripcion(session, id, categoria_id, torneo_id, jugador_id, equipo_id)

@router.put("/{inscripcion_id}/{categoria_id}")
def update_inscripcion(inscripcion_id: int, categoria_id: int, jugador_id: int, equipo_id: int, session: Session = Depends(get_db)):
    return actualizar_inscripcion(session, inscripcion_id, categoria_id, jugador_id, equipo_id)

@router.delete("/{inscripcion_id}/{categoria_id}")
def delete_inscripcion(inscripcion_id: int, categoria_id: int, session: Session = Depends(get_db)):
    return eliminar_inscripcion(session, inscripcion_id, categoria_id)
