from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Categoria

def create_categoria(session: Session, *, edad_min: int, edad_max: int,
                     genero: str, sets_x_partido: int,
                     puntos_x_set: int) -> Categoria:
    cat = Categoria(edad_min=edad_min, edad_max=edad_max, genero=genero,
                    sets_x_partido=sets_x_partido, puntos_x_set=puntos_x_set)
    session.add(cat); session.commit(); session.refresh(cat)
    return cat

def get_categoria(session: Session, categoria_id: int) -> Optional[Categoria]:
    return session.get(Categoria, categoria_id)

def get_categorias(session: Session) -> List[Categoria]:
    return session.query(Categoria).all()

def update_categoria(session: Session, categoria_id: int, *,
                     edad_min: int, edad_max: int, genero: str,
                     sets_x_partido: int, puntos_x_set: int
                     ) -> Optional[Categoria]:
    cat = session.get(Categoria, categoria_id)
    if not cat: return None
    cat.edad_min = edad_min; cat.edad_max = edad_max; cat.genero = genero
    cat.sets_x_partido = sets_x_partido; cat.puntos_x_set = puntos_x_set
    session.commit(); session.refresh(cat); return cat

def delete_categoria(session: Session, categoria_id: int) -> Optional[Categoria]:
    cat = session.get(Categoria, categoria_id)
    if not cat: return None
    session.delete(cat); session.commit(); return cat
