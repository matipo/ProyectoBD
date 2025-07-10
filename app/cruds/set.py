from typing import Optional, List
from sqlalchemy.orm import Session
from ..models import ResultadoSet
from sqlalchemy import and_


# --------------------- CREAR CON VALIDACIÓN ---------------------

def crear_resultado_set(session: Session, partido_id: int, numero_set: int, puntos_j1: int, puntos_j2: int):
    diferencia = abs(puntos_j1 - puntos_j2)
    max_puntos = max(puntos_j1, puntos_j2)

    # Validar que se gane con al menos 11 puntos y diferencia mínima de 2
    if max_puntos < 11 or diferencia < 2:
        raise ValueError("El set debe ganarse con al menos 11 puntos y una diferencia mínima de 2")

    # Verificar si el partido ya tiene 2 sets ganados por algún jugador
    sets_jugados = session.query(ResultadoSet).filter(ResultadoSet.partido_id == partido_id).all()
    ganados_j1 = sum(1 for s in sets_jugados if s.puntos_jugador1 > s.puntos_jugador2)
    ganados_j2 = sum(1 for s in sets_jugados if s.puntos_jugador2 > s.puntos_jugador1)

    if ganados_j1 >= 2 or ganados_j2 >= 2:
        raise ValueError("Este partido ya fue ganado (mejor de 3 sets)")

    # Validar que el número de set no se repita
    set_existente = session.query(ResultadoSet).filter(
        and_(ResultadoSet.partido_id == partido_id, ResultadoSet.numero_set == numero_set)
    ).first()
    if set_existente:
        raise ValueError(f"Ya existe un set número {numero_set} para este partido")

    # Crear y guardar el nuevo set
    nuevo_set = ResultadoSet(
        partido_id=partido_id,
        numero_set=numero_set,
        puntos_jugador1=puntos_j1,
        puntos_jugador2=puntos_j2
    )
    session.add(nuevo_set)
    session.commit()
    session.refresh(nuevo_set)
    return nuevo_set


# --------------------- OBTENER UN SET ---------------------

def obtener_resultado_set(session: Session, id: int) -> Optional[ResultadoSet]:
    return session.query(ResultadoSet).filter(ResultadoSet.id == id).first()


# --------------------- OBTENER TODOS LOS SETS DE UN PARTIDO ---------------------

def obtener_resultados_por_partido(session: Session, partido_id: int) -> List[ResultadoSet]:
    return session.query(ResultadoSet).filter(ResultadoSet.partido_id == partido_id).order_by(ResultadoSet.numero_set).all()


# --------------------- ACTUALIZAR RESULTADO DE UN SET ---------------------

def actualizar_resultado_set(session: Session, id: int, puntos_j1: int, puntos_j2: int) -> Optional[ResultadoSet]:
    resultado = session.query(ResultadoSet).filter(ResultadoSet.id == id).first()
    if not resultado:
        return None

    resultado.puntos_jugador1 = puntos_j1
    resultado.puntos_jugador2 = puntos_j2
    session.commit()
    session.refresh(resultado)
    return resultado


# --------------------- ELIMINAR RESULTADO ---------------------

def eliminar_resultado_set(session: Session, id: int) -> Optional[ResultadoSet]:
    resultado = session.query(ResultadoSet).filter(ResultadoSet.id == id).first()
    if not resultado:
        return None
    session.delete(resultado)
    session.commit()
    return resultado