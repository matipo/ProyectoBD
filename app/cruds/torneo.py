from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Torneo

def crear_torneo(sesion, nombre, inicio_inscripcion, fin_inscripcion, 
    inicio_competencia, fin_competencia, mesas_disponibles, fecha_creacion: Optional[datetime] = None):
    if fecha_creacion is None:
        fecha_creacion = datetime.now()
        fecha_creacion = fecha_creacion
    torneo = Torneo(
    nombre=nombre,
    inicio_inscripcion=inicio_inscripcion,
    fin_inscripcion=fin_inscripcion,
    inicio_competencia=inicio_competencia,
    fin_competencia=fin_competencia,
    mesas_disponibles=mesas_disponibles
    )
    sesion.add(torneo)
    sesion.commit()
    return torneo

def obtener_torneo(sesion, id):
    return sesion.query(Torneo).filter(Torneo.id == id).first()   

def obtener_torneos(sesion):
    return sesion.query(Torneo).all()

def actualizar_torneo(sesion, id, nombre, inicio_inscripcion, fin_inscripcion, inicio_competencia, fin_competencia, mesas_disponibles):
    torneo = sesion.query(Torneo).filter(Torneo.id == id).first()
    torneo.nombre = nombre
    torneo.inicio_inscripcion = inicio_inscripcion
    torneo.fin_inscripcion = fin_inscripcion
    torneo.inicio_competencia = inicio_competencia
    torneo.fin_competencia = fin_competencia
    torneo.mesas_disponibles = mesas_disponibles
    sesion.commit()
    return torneo

def eliminar_torneo(sesion, id):
    torneo = sesion.query(Torneo).filter(Torneo.id == id).first()
    sesion.delete(torneo)
    sesion.commit()
    return torneo