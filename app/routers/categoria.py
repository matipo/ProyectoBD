from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..cruds.categoria import (
    crear_categoria,
    obtener_categoria,
    obtener_categorias,
    actualizar_categoria,
    eliminar_categoria,
)

router = APIRouter()

@router.get("/")
def get_categorias(session: Session = Depends(get_db)):
    return obtener_categorias(session)

@router.get("/{categoria_id}")
def get_categoria(categoria_id: int, session: Session = Depends(get_db)):
    categoria = obtener_categoria(session, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/")
def create_categoria(nombre: str, genero: str, sets_por_partido: int, puntos_por_sets: int, edad_min: int, edad_max: int, session: Session = Depends(get_db)):
    return crear_categoria(session, nombre, genero, sets_por_partido, puntos_por_sets, edad_min, edad_max)

@router.put("/{categoria_id}")
def update_categoria(categoria_id: int, nombre: str, genero: str, sets_por_partido: int, puntos_por_sets: int, edad_min: int, edad_max: int, session: Session = Depends(get_db)):
    return actualizar_categoria(session, categoria_id, nombre, genero, sets_por_partido, puntos_por_sets, edad_min, edad_max)

@router.delete("/{categoria_id}")
def delete_categoria(categoria_id: int, session: Session = Depends(get_db)):
    return eliminar_categoria(session, categoria_id)
