# routes/categoria.py
from fastapi import APIRouter, Depends, HTTPException
from ..db import get_db
from ..cruds.categoria import (
    create_categoria, get_categoria, get_categorias,
    update_categoria, delete_categoria
)

router = APIRouter()

@router.get("/")
def list_categorias(session=Depends(get_db)):
    return [c.__dict__ for c in get_categorias(session)]

@router.get("/{categoria_id}")
def read_categoria(categoria_id: int, session=Depends(get_db)):
    cat = get_categoria(session, categoria_id)
    if not cat:
        raise HTTPException(404, "Categoría no encontrada")
    return cat.__dict__

@router.post("/", status_code=201)
def new_categoria(edad_min: int, edad_max: int, genero: str,
                  sets_x_partido: int, puntos_x_set: int,
                  session=Depends(get_db)):
    return create_categoria(session, edad_min=edad_min, edad_max=edad_max,
                            genero=genero, sets_x_partido=sets_x_partido,
                            puntos_x_set=puntos_x_set).__dict__

@router.put("/{categoria_id}")
def mod_categoria(categoria_id: int, edad_min: int, edad_max: int, genero: str,
                  sets_x_partido: int, puntos_x_set: int,
                  session=Depends(get_db)):
    cat = update_categoria(session, categoria_id, edad_min=edad_min,
                           edad_max=edad_max, genero=genero,
                           sets_x_partido=sets_x_partido,
                           puntos_x_set=puntos_x_set)
    if not cat:
        raise HTTPException(404, "Categoría no encontrada")
    return cat.__dict__

@router.delete("/{categoria_id}")
def rem_categoria(categoria_id: int, session=Depends(get_db)):
    cat = delete_categoria(session, categoria_id)
    if not cat:
        raise HTTPException(404, "Categoría no encontrada")
    return {"detail": "Categoría eliminada"}
