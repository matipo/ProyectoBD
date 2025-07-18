from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..cruds.mesa import (
    crear_mesa,
    obtener_mesas,
    obtener_mesas_torneo,
    actualizar_mesa,
    eliminar_mesa,
)

router = APIRouter()

@router.get("/")
def get_mesas(session: Session = Depends(get_db)):
    return obtener_mesas(session)

@router.get("/torneo/{torneo_id}")
def get_mesas_torneo(torneo_id: int, session: Session = Depends(get_db)):
    

    return obtener_mesas_torneo(session, torneo_id)

@router.post("/")
def create_mesa(numero: int, torneo_id,  session: Session = Depends(get_db)):
    mesa = crear_mesa(session, numero, torneo_id=torneo_id )
    
    return mesa

@router.put("/{mesa_id}")
def update_mesa(mesa_id: int, numero: int, session: Session = Depends(get_db)):
    return actualizar_mesa(session, mesa_id, numero)

@router.delete("/{mesa_id}")
def delete_mesa(mesa_id: int, session: Session = Depends(get_db)):
    return eliminar_mesa(session, mesa_id)
