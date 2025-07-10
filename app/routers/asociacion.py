from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..cruds.asociacion import (
    crear_asociacion,
    obtener_asociacion,
    obtener_asociaciones,
    actualizar_asociacion,
    eliminar_asociacion,
)

router = APIRouter()

@router.get("/")
def get_asociaciones(session: Session = Depends(get_db)):
    return obtener_asociaciones(session)

@router.get("/{asociacion_id}")
def get_asociacion(asociacion_id: int, session: Session = Depends(get_db)):
    asociacion = obtener_asociacion(session, asociacion_id)
    if not asociacion:
        raise HTTPException(status_code=404, detail="Asociación no encontrada")
    return asociacion

@router.post("/")
def create_asociacion(nombre: str, ciudad: str,pais:str, session: Session = Depends(get_db)):
    return crear_asociacion(session, nombre, ciudad, pais)

@router.put("/{asociacion_id}")
def update_asociacion(asociacion_id: int, nombre: str, ciudad: str,pais:str , session: Session = Depends(get_db)):
    return actualizar_asociacion(session, asociacion_id, nombre, ciudad,pais)

@router.delete("/{asociacion_id}")
def delete_asociacion(asociacion_id: int, session: Session = Depends(get_db)):
    return eliminar_asociacion(session, asociacion_id)
