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
    torneo = Torneo(
    nombre=nombre,
    fechas_inscripcion=fechas_inscripcion,
    fecha_competencia=fecha_competencia,
    mesas_requeridas=mesas_requeridas,
    )
    
    session.add(torneo)
    
    session.commit()
    if mesas_requeridas is not None:
        mesas_disponibles = session.query(Mesa).filter(Mesa.torneo_id == None).limit(mesas_requeridas).all()
        print("MESAS DISPONIBLES :", mesas_disponibles)
        for i in range(mesas_requeridas - len(mesas_disponibles)):
            nueva_mesa = crear_mesa(session,i+1,torneo.id,None)
            mesas_disponibles.append(nueva_mesa)
            print("LLEGO HASTA ACÁ")

        for i, mesa in enumerate(mesas_disponibles[:mesas_requeridas]):
            mesa.torneo_id = torneo.id
            mesa.numero = i + 1  # Renumerar si querés
            session.add(mesa)
        session.commit()
    else:
        print("No se ejecuto", mesas_requeridas, print(torneo.id))
    session.refresh(torneo)
    
    
    return torneo


def obtener_torneo(session, id):
    return session.query(Torneo).filter(Torneo.id == id).first()   

def obtener_torneos(session):
    return session.query(Torneo).all()

def actualizar_torneo(session, id, nombre, fechas_inscripcion, fecha_competencia, mesas_requeridas):
    torneo = session.query(Torneo).filter(Torneo.id == id).first()
    torneo.nombre = nombre
    torneo.fechas_inscripcion = fechas_inscripcion
    torneo.fecha_competencia = fecha_competencia
    torneo.mesas_requeridas = mesas_requeridas

    session.commit()
    return torneo

def eliminar_torneo(session, id):
    torneo = session.query(Torneo).filter(Torneo.id == id).first()
    session.delete(torneo)
    session.commit()
    return torneo