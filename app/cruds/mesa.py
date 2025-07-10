from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Mesa

def crear_mesa(session, numero, capacidad, torneo, fecha_creacion: Optional[datetime] = None):
    if fecha_creacion is None:
        fecha_creacion = datetime.now()
    mesa = Mesa(
        numero=numero, 
        capacidad=capacidad,
        torneo=torneo, 
        fecha_creacion=fecha_creacion
        )

    session.add(mesa)
    session.commit()
    session.refresh(mesa)
    return mesa

def obtener_mesas(session):
    return session.query(Mesa).all()

def obtener_mesas_torneo(session, torneo_id):
    return session.query(Mesa).filter(Mesa.torneo_id == torneo_id).all()

def actualizar_mesa(session, id, numero, capacidad):
    mesa = session.query(Mesa).filter(Mesa.id == id).first()
    mesa.numero = numero
    mesa.capacidad = capacidad
    session.commit()
    return mesa

def eliminar_mesa(session, id):
    mesa = session.query(Mesa).filter(Mesa.id == id).first()
    session.delete(mesa)
    session.commit()
    return mesa