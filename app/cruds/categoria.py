from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Categoria 

def crear_categoria(sesion, nombre, genero, sets_por_partido, puntos_por_sets, edad_min, edad_max,  fecha_creacion: Optional[datetime] = None):
    if fecha_creacion is None:
        fecha_creacion = datetime.now()
    categoria = Categoria(
      nombre=nombre, 
      genero=genero,
      sets_por_partido=sets_por_partido,
      puntos_por_sets=puntos_por_sets,
      edad_min=edad_min,
      edad_max=edad_max,
      fecha_creacion=fecha_creacion)
    sesion.add(categoria)
    sesion.commit()
    return categoria

def obtener_categorias(sesion):
    return sesion.query(Categoria).all()

def obtener_categoria(sesion, id):
    return sesion.query(Categoria).filter(Categoria.id == id).first()

def actualizar_categoria(sesion, id, nombre, genero, sets_por_partido, puntos_por_sets, edad_min, edad_max):
    categoria = sesion.query(Categoria).filter(Categoria.id == id).first()
    categoria.nombre = nombre
    categoria.genero = genero
    categoria.sets_por_partido = sets_por_partido
    categoria.puntos_por_sets = puntos_por_sets
    categoria.edad_min = edad_min
    categoria.edad_max = edad_max
    sesion.commit()
    return categoria

def eliminar_categoria(sesion, id):
    categoria = sesion.query(Categoria).filter(Categoria.id == id).first()
    sesion.delete(categoria)
    sesion.commit()
    return categoria