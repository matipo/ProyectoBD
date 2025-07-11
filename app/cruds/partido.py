from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Partido
from . mesa import Mesa

def crear_partido(session, es_bye, fase, categoria, tipo, jugador1, jugador2, horario: datetime = None):
    if horario is None:
        horario = datetime.now()

    if tipo not in ['individual', 'dobles']:
        raise ValueError('El tipo de partido debe ser individual o dobles')
    if fase not in ['grupos', 'octavos', 'cuartos', 'semifinal', 'final']:
        raise ValueError('La fase debe ser grupos, octavos, cuartos, semifinal o final')
    if es_bye and jugador2 is not None:
        raise ValueError('Si es un bye, no puede haber jugador2')

    # 🔎 Buscar mesa libre para el horario
    mesa_ocupada_ids = [p.mesa_id for p in session.query(Partido).filter(Partido.horario == horario).all()]
    mesa_libre = session.query(Mesa).filter(~Mesa.id.in_(mesa_ocupada_ids)).first()

    if not mesa_libre:
        # ✅ Crear una nueva mesa
        nuevo_numero = (session.query(Mesa).count() + 1)  # o lógica diferente
        mesa_libre = Mesa(numero=nuevo_numero, fecha_creacion=horario.date())
        session.add(mesa_libre)
        session.flush()  # Necesario para obtener mesa_libre.id

    # Crear el partido
    partido = Partido(
        horario=horario,
        es_bye=es_bye,
        mesa_id=mesa_libre.id,
        categorias=categoria,
        jugador1=jugador1,
        jugador2=jugador2 if tipo == 'individual' else None,
        equipo1=jugador1 if tipo == 'dobles' else None,
        equipo2=jugador2 if tipo == 'dobles' else None,
    )

    session.add(partido)
    session.commit()
    session.refresh(partido)
    return partido

def obtener_partidos(session: Session):
    return session.query(Partido).all()

def obtener_partido(session: Session, id: int):
    return session.query(Partido).filter(Partido.id == id).first()

def actualizar_partido(session: Session, id: int, mesa: int, es_bye: bool, fase: int, categoria: int, tipo: str, jugador1: int, jugador2: int):
    partido = session.query(Partido).filter(Partido.id == id).first()
    partido.mesa = mesa
    partido.es_bye = es_bye
    partido.fase = fase
    partido.categoria = categoria
    partido.tipo = tipo
    partido.jugador1 = jugador1
    partido.jugador2 = jugador2
    session.commit()
    session.refresh(partido)
    return partido

def eliminar_partido(session: Session, id: int):
    partido = session.query(Partido).filter(Partido.id == id).first()
    session.delete(partido)
    session.commit()
    return partido