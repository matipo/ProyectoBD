from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Mesa

def crear_mesa(sesion, numero, capacidad, fecha_creacion: Optional[datetime] = None):
    if fecha_creacion is None:
        fecha_creacion = datetime.now()
    mesa = Mesa(numero=numero, capacidad=capacidad, fecha_creacion=fecha_creacion)
    sesion.add(mesa)
    sesion.commit()
    return mesa

def obtener_mesas(sesion):
    return sesion.query(Mesa).all()

def obtener_mesas_torneo(sesion, torneo_id):
    return sesion.query(Mesa).filter(Mesa.torneo_id == torneo_id).all()

def actualizar_mesa(sesion, id, numero, capacidad):
    mesa = sesion.query(Mesa).filter(Mesa.id == id).first()
    mesa.numero = numero
    mesa.capacidad = capacidad
    sesion.commit()
    return mesa

def eliminar_mesa(sesion, id):
    mesa = sesion.query(Mesa).filter(Mesa.id == id).first()
    sesion.delete(mesa)
    sesion.commit()
    return mesa