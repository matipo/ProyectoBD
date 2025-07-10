from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Partido

def crear_partido(sesion: Session, mesa: int, es_bye: bool, fase: int, categoria: int, tipo: str, jugador1: int, jugador2: int, fecha_creacion: Optional[datetime] = None ):
    if fecha_creacion is None:
        fecha_creacion = datetime.now()
    if tipo not in ['individual', 'dobles']:
        raise ValueError('El tipo de partido debe ser individual o dobles')
    if fase not in ['grupos', 'octavos', 'cuartos', 'semifinal', 'final']:
        raise ValueError('La fase debe ser grupos, octavos, cuartos, semifinal o final')
    if es_bye and jugador2 is not None:
        raise ValueError('Si es un bye, no puede haber jugador2')


    mesa_ocupada = sesion.query(Partido).filter(Partido.mesa == mesa, Partido.fecha_creacion == fecha_creacion).first()
    
    if mesa_ocupada: raise ValueError('La mesa ya esta ocupada en esta fecha')
      
    partido = Partido(
        mesa=mesa,
        es_bye=es_bye,
        fase=fase,
        categoria=categoria,
        tipo=tipo,
        jugador1=jugador1,
        jugador2=jugador2,
        fecha_creacion=fecha_creacion
    )
    if tipo == 'individual':
        partido.jugador1 = jugador1
        partido.jugador2 = jugador2
    else:
        partido.equipo1 = jugador1
        partido.equipo2 = jugador2

    sesion.add(partido)
    sesion.commit()
    return partido 

def obtener_partidos(sesion: Session):
    return sesion.query(Partido).all()

def obtener_partido(sesion: Session, id: int):
    return sesion.query(Partido).filter(Partido.id == id).first()

def actualizar_partido(sesion: Session, id: int, mesa: int, es_bye: bool, fase: int, categoria: int, tipo: str, jugador1: int, jugador2: int):
    partido = sesion.query(Partido).filter(Partido.id == id).first()
    partido.mesa = mesa
    partido.es_bye = es_bye
    partido.fase = fase
    partido.categoria = categoria
    partido.tipo = tipo
    partido.jugador1 = jugador1
    partido.jugador2 = jugador2
    sesion.commit()
    return partido

def eliminar_partido(sesion: Session, id: int):
    partido = sesion.query(Partido).filter(Partido.id == id).first()
    sesion.delete(partido)
    sesion.commit()
    return partido