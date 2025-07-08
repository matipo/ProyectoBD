from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Text,Index, Table, PrimaryKeyConstraint
from .db import Base
from sqlalchemy.orm import relationship

class Asociacion(Base):
    __tablename__ = "asociaciones"

    id     = Column(Integer, primary_key=True)
    ciudad = Column(Text, nullable=False)
    pais   = Column(Text, nullable=False)

    # Relacion uno‑a‑muchos
    jugadores = relationship("Jugador", back_populates="asociacion")


class Categoria(Base):
    __tablename__ = "categorias"

    id             = Column(Integer, primary_key=True)
    edad_min       = Column(Integer, nullable=False)
    edad_max       = Column(Integer, nullable=False)
    genero         = Column(Text,    nullable=False)
    sets_x_partido = Column(Integer, nullable=False)
    puntos_x_set   = Column(Integer, nullable=False)

    # Relaciones (opcionales, pero útiles)
    equipos       = relationship("Equipo", back_populates="categoria")
    partidos      = relationship("Partido", back_populates="categoria")
    torneos_link  = relationship("CategoriaTorneo", back_populates="categoria")
    fases_link    = relationship("CategoriaFase",   back_populates="categoria")
    inscripciones = relationship("Inscripcion",     back_populates="categoria")


class Equipo(Base):
    __tablename__ = "equipo"

    id            = Column(Integer, primary_key=True)
    nombre_equipo = Column(Text,    nullable=False)
    categorias    = Column(Integer, ForeignKey("categorias.id",
                                               ondelete="CASCADE"),
                            nullable=False)

    categoria     = relationship("Categoria", back_populates="equipos")

    # Jugadores (dos tablas de enlace según tu esquema)
    jugadores  = relationship("Jugador",
                              secondary="equipo_jugador",
                              back_populates="equipos")
    jugadores2 = relationship("Jugador",
                              secondary="equipo_jugador_2",
                              back_populates="equipos2")

    # Para navegar partidos donde participa como equipo1 / equipo2
    partidos1 = relationship("Partido", back_populates="equipo1_rel",
                             foreign_keys="Partido.equipo1")
    partidos2 = relationship("Partido", back_populates="equipo2_rel",
                             foreign_keys="Partido.equipo2")

    inscripciones = relationship("Inscripcion", back_populates="equipo_rel")

# Índice explícito
Index("idx_equipo__categorias", Equipo.categorias)


class Jugador(Base):
    __tablename__ = "jugador"

    id              = Column(Integer, primary_key=True)
    pais            = Column(Text,  nullable=False)
    fecha_nacimiento= Column(Date,  nullable=False)
    genero          = Column(Text,  nullable=False)
    ciudad          = Column(Text,  nullable=False)
    asociaciones    = Column(Integer, ForeignKey("asociaciones.id",
                                                 ondelete="SET NULL"))

    asociacion = relationship("Asociacion", back_populates="jugadores")

    # Equipos
    equipos  = relationship("Equipo",
                            secondary="equipo_jugador",
                            back_populates="jugadores")
    equipos2 = relationship("Equipo",
                            secondary="equipo_jugador_2",
                            back_populates="jugadores2")

    # Partidos (como jugador1 / jugador2)
    partidos1 = relationship("Partido", back_populates="jugador1_rel",
                             foreign_keys="Partido.jugador1")
    partidos2 = relationship("Partido", back_populates="jugador2_rel",
                             foreign_keys="Partido.jugador2")

    inscripciones = relationship("Inscripcion", back_populates="jugador_rel")

Index("idx_jugador__asociaciones", Jugador.asociaciones)

# ---------------------------------------------------------------------------
# Tablas puente (many‑to‑many)
# ---------------------------------------------------------------------------

equipo_jugador = Table(
    "equipo_jugador",
    Base.metadata,
    Column("equipo",  Integer, ForeignKey("equipo.id",   ondelete="CASCADE"),
           primary_key=True),
    Column("jugador", Integer, ForeignKey("jugador.id", ondelete="CASCADE"),
           primary_key=True),
    Index("idx_equipo_jugador", "jugador")
)

equipo_jugador_2 = Table(
    "equipo_jugador_2",
    Base.metadata,
    Column("equipo",  Integer, ForeignKey("equipo.id",   ondelete="CASCADE"),
           primary_key=True),
    Column("jugador", Integer, ForeignKey("jugador.id", ondelete="CASCADE"),
           primary_key=True),
    Index("idx_equipo_jugador_2", "jugador")
)

# ---------------------------------------------------------------------------
# Partidos / mesas / resultados
# ---------------------------------------------------------------------------

class Partido(Base):
    __tablename__ = "partidos"

    id            = Column(Integer, primary_key=True)
    horario       = Column(DateTime, nullable=False)
    mesa_asignada = Column(Integer)
    es_bye        = Column(Boolean,  nullable=False)

    categorias = Column(Integer, ForeignKey("categorias.id",
                                            ondelete="CASCADE"),
                        nullable=False)
    jugador1   = Column(Integer, ForeignKey("jugador.id",
                                            ondelete="SET NULL"))
    jugador2   = Column(Integer, ForeignKey("jugador.id",
                                            ondelete="SET NULL"))
    equipo1    = Column(Integer, ForeignKey("equipo.id",
                                            ondelete="SET NULL"))
    equipo2    = Column(Integer, ForeignKey("equipo.id",
                                            ondelete="SET NULL"))

    categoria  = relationship("Categoria", back_populates="partidos")
    jugador1_rel = relationship("Jugador", foreign_keys=[jugador1],
                                back_populates="partidos1")
    jugador2_rel = relationship("Jugador", foreign_keys=[jugador2],
                                back_populates="partidos2")
    equipo1_rel  = relationship("Equipo",  foreign_keys=[equipo1],
                                back_populates="partidos1")
    equipo2_rel  = relationship("Equipo",  foreign_keys=[equipo2],
                                back_populates="partidos2")

    resultados = relationship("ResultadoSet", back_populates="partido",
                              cascade="all, delete-orphan")
    mesa       = relationship("Mesa", back_populates="partido",
                              uselist=False)
    fases      = relationship("Fase", back_populates="partido")

Index("idx_partidos__categorias", Partido.categorias)
Index("idx_partidos__equipo1",    Partido.equipo1)
Index("idx_partidos__equipo2",    Partido.equipo2)
Index("idx_partidos__jugador1",   Partido.jugador1)
Index("idx_partidos__jugador2",   Partido.jugador2)


class Mesa(Base):
    __tablename__ = "mesas"

    id       = Column(Integer, primary_key=True)
    partidos = Column(Integer, ForeignKey("partidos.id",
                                          ondelete="CASCADE"),
                      nullable=False)

    partido = relationship("Partido", back_populates="mesa")
    torneos = relationship("Torneo", back_populates="mesa")

Index("idx_mesas__partidos", Mesa.partidos)


class ResultadoSet(Base):
    __tablename__ = "resultados_set"

    id         = Column(Integer, primary_key=True)
    numero_set = Column(Integer, nullable=False)
    puntos     = Column(Integer, nullable=False)
    partidos   = Column(Integer, ForeignKey("partidos.id",
                                            ondelete="CASCADE"),
                        nullable=False)

    partido = relationship("Partido", back_populates="resultados")

Index("idx_resultados_set__partidos", ResultadoSet.partidos)

# ---------------------------------------------------------------------------
# Torneos y fases
# ---------------------------------------------------------------------------

class Torneo(Base):
    __tablename__ = "torneos"

    id                = Column(Integer, primary_key=True)
    nombre            = Column(Text, nullable=False)
    fechas_inscripcion= Column(Date, nullable=False)
    fecha_competencia = Column(Date, nullable=False)
    mesas             = Column(Integer, ForeignKey("mesas.id",
                                                   ondelete="CASCADE"),
                               nullable=False)

    mesa       = relationship("Mesa",    back_populates="torneos")
    fases      = relationship("Fase",    back_populates="torneo")
    categorias = relationship("CategoriaTorneo",
                              back_populates="torneo")
    inscripciones = relationship("Inscripcion",
                                 back_populates="torneo")

Index("idx_torneos__mesas", Torneo.mesas)


class CategoriaTorneo(Base):
    __tablename__ = "categorias_torneos"

    categorias = Column(Integer, ForeignKey("categorias.id"),
                        primary_key=True)
    torneos    = Column(Integer, ForeignKey("torneos.id"),
                        primary_key=True)

    categoria = relationship("Categoria", back_populates="torneos_link")
    torneo    = relationship("Torneo",    back_populates="categorias")

Index("idx_categorias_torneos", CategoriaTorneo.torneos)


class Fase(Base):
    __tablename__ = "fases"

    id       = Column(Integer, primary_key=True)
    tipo     = Column(Text, nullable=False)
    nombre   = Column(Text, nullable=False)
    torneos  = Column(Integer, ForeignKey("torneos.id",
                                          ondelete="CASCADE"),
                      nullable=False)
    partidos = Column(Integer, ForeignKey("partidos.id",
                                          ondelete="CASCADE"),
                      nullable=False)

    torneo   = relationship("Torneo",  back_populates="fases")
    partido  = relationship("Partido", back_populates="fases")
    categorias = relationship("CategoriaFase",
                              back_populates="fase")

Index("idx_fases__partidos", Fase.partidos)
Index("idx_fases__torneos", Fase.torneos)


class CategoriaFase(Base):
    __tablename__ = "categorias_fases"

    categorias = Column(Integer, ForeignKey("categorias.id"),
                        primary_key=True)
    fases      = Column(Integer, ForeignKey("fases.id"),
                        primary_key=True)

    categoria = relationship("Categoria", back_populates="fases_link")
    fase      = relationship("Fase",      back_populates="categorias")

Index("idx_categorias_fases", CategoriaFase.fases)

# ---------------------------------------------------------------------------
# Inscripciones (PK compuesta)
# ---------------------------------------------------------------------------

class Inscripcion(Base):
    __tablename__ = "inscripciones"

    id         = Column(Integer, nullable=False)
    categorias = Column(Integer, ForeignKey("categorias.id",
                                            ondelete="CASCADE"),
                        nullable=False)
    torneos    = Column(Integer, ForeignKey("torneos.id",
                                            ondelete="CASCADE"),
                        nullable=False)
    jugador = Column(Integer, ForeignKey("jugador.id",
                                         ondelete="SET NULL"))
    equipo  = Column(Integer, ForeignKey("equipo.id",
                                         ondelete="SET NULL"))

    __table_args__ = (
        PrimaryKeyConstraint("id", "categorias"),
        Index("idx_inscripciones__categorias", "categorias"),
        Index("idx_inscripciones__torneos",    "torneos"),
        Index("idx_inscripciones__jugador",    "jugador"),
        Index("idx_inscripciones__equipo",     "equipo"),
    )

    categoria = relationship("Categoria", back_populates="inscripciones")
    torneo    = relationship("Torneo",    back_populates="inscripciones")
    jugador_rel = relationship("Jugador", back_populates="inscripciones")
    equipo_rel  = relationship("Equipo",  back_populates="inscripciones")