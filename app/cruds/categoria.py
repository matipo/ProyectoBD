from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Categoria 

def crear_categoria(session, nombre, genero, sets_por_partido, puntos_por_sets, edad_min, edad_max):

    if genero not in ['masculino', 'femenino']:
        raise ValueError('El genero debe ser "masculino" o "femenino"')
    

    categoria = Categoria(
      nombre=nombre, 
      genero=genero,
      sets_por_partido=sets_por_partido,
      puntos_por_sets=puntos_por_sets,
      edad_min=edad_min,
      edad_max=edad_max
      )
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

def obtener_categorias(session):
    return session.query(Categoria).all()

def obtener_categoria(session, id):
    return session.query(Categoria).filter(Categoria.id == id).first()

def actualizar_categoria(session, id, nombre, genero, sets_por_partido, puntos_por_sets, edad_min, edad_max):
    categoria = session.query(Categoria).filter(Categoria.id == id).first()
    categoria.nombre = nombre
    categoria.genero = genero
    categoria.sets_por_partido = sets_por_partido
    categoria.puntos_por_sets = puntos_por_sets
    categoria.edad_min = edad_min
    categoria.edad_max = edad_max
    session.commit()
    session.refresh(categoria)
    return categoria

def eliminar_categoria(session, id):
    categoria = session.query(Categoria).filter(Categoria.id == id).first()
    session.delete(categoria)
    session.commit()
    return categoria