from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Torneo
from .mesa import crear_mesa
from .mesa import Mesa

def crear_torneo(session, nombre, fechas_inscripcion, fecha_competencia, mesas_requeridas, fecha_creacion: Optional[datetime] = None):
    if fecha_creacion is None:
        fecha_creacion = datetime.now()
        fecha_creacion = fecha_creacion
    


    
    if fechas_inscripcion >= fecha_competencia:
        raise ValueError("La fecha de inicio de inscripciones debe ser menor a la fecha de la competencia")

    if mesas_requeridas <= 0:
        raise ValueError("El numero de mesas debe ser mayor a 0")


    # 24-28 - Asignaciones
    torneo = Torneo(
    nombre=nombre,
    fechas_inscripcion=fechas_inscripcion,
    fecha_competencia=fecha_competencia,
    mesas_requeridas=mesas_requeridas if mesas_requeridas <= 0  else None,
    )
    
    session.add(torneo)
    
    session.commit()
    if mesas_requeridas is not None:
        # Importa objeto de base de datos que no esten asignadas a otro torneo.
        mesas_disponibles = session.query(Mesa).filter(Mesa.torneo_id == None).limit(mesas_requeridas).all()

        # 39-42 - Utiliza mesas no asignadas y si faltan crea más.
        for i in range(mesas_requeridas - len(mesas_disponibles)):
            nueva_mesa = crear_mesa(session,i+1,torneo.id,None)
            mesas_disponibles.append(nueva_mesa)
            print("LLEGO HASTA ACÁ!! :)")
        
        # 45-48 - Asigna las mesas al torneo.
        for i, mesa in enumerate(mesas_disponibles[:mesas_requeridas]):
            mesa.torneo_id = torneo.id
            mesa.numero = i + 1  # Renumera
            session.add(mesa)
        session.commit()
    
    session.refresh(torneo)
    return torneo

# 55-59 - GETs
def obtener_torneo(session, id):
    return session.query(Torneo).filter(Torneo.id == id).first()   

def obtener_torneos(session):
    return session.query(Torneo).all()

# 62-70 - Un Update de toda la vida
def actualizar_torneo(session, id, nombre, fechas_inscripcion, fecha_competencia, mesas_requeridas):
    torneo = session.query(Torneo).filter(Torneo.id == id).first()
    torneo.nombre = nombre
    torneo.fechas_inscripcion = fechas_inscripcion
    torneo.fecha_competencia = fecha_competencia
    torneo.mesas_requeridas = mesas_requeridas

    session.commit()
    return torneo

# 72-77 - Exterminador de torneos :c
def eliminar_torneo(session, id):
    torneo = session.query(Torneo).filter(Torneo.id == id).first()
    session.delete(torneo)
    session.commit()
    return torneo