from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from .. import ResultadoSetCreate, ResultadoSetUpdate, ResultadoSetResponse
from ..cruds import set

router = APIRouter(
    prefix="/resultados_set",
    tags=["Resultados de Set"]
)

# ------------------- CREAR -------------------

@router.post("/", response_model=ResultadoSetResponse)
def crear_resultado_set(
    data: ResultadoSetCreate,
    db: Session = Depends(get_db)
):
    try:
        resultado = set.crear_resultado_set(
            session=db,
            partido_id=data.partido_id,
            numero_set=data.numero_set,
            puntos_j1=data.puntos_j1,
            puntos_j2=data.puntos_j2
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ------------------- OBTENER UNO -------------------

@router.get("/{id}", response_model=ResultadoSetResponse)
def obtener_resultado_set(id: int, db: Session = Depends(get_db)):
    resultado = set.obtener_resultado_set(db, id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Set no encontrado")
    return resultado


# ------------------- OBTENER TODOS POR PARTIDO -------------------

@router.get("/partido/{partido_id}", response_model=List[ResultadoSetResponse])
def obtener_resultados_por_partido(partido_id: int, db: Session = Depends(get_db)):
    return set.obtener_resultados_por_partido(db, partido_id)


# ------------------- ACTUALIZAR -------------------

@router.put("/{id}", response_model=ResultadoSetResponse)
def actualizar_resultado_set(
    id: int,
    data: ResultadoSetUpdate,
    db: Session = Depends(get_db)
):
    resultado = set.actualizar_resultado_set(
        session=db,
        id=id,
        puntos_j1=data.puntos_j1,
        puntos_j2=data.puntos_j2
    )
    if not resultado:
        raise HTTPException(status_code=404, detail="Set no encontrado")
    return resultado


# ------------------- ELIMINAR -------------------

@router.delete("/{id}", response_model=ResultadoSetResponse)
def eliminar_resultado_set(id: int, db: Session = Depends(get_db)):
    resultado = set.eliminar_resultado_set(db, id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Set no encontrado")
    return resultado
