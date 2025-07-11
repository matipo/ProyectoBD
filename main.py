import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .app.routers import jugador,asociacion,equipo,fases,inscripciones,torneo,categoria,partido


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Inicio de la aplicación
    logging.info("Aplicación iniciada")

    yield

    # Cierre de la aplicación
    logging.info("Aplicación cerrada")
    pass


FASTAPI_CONFIG = {
    "title": "Aplicación FastAPI",
    "description": "Una aplicación de ejemplo utilizando FastAPI",
    "openapi_url": "/openapi.json",
    "version": "0.1.0",
    "swagger_ui_parameters": {"defaultModelsExpandDepth": -1},
}

MIDDLEWARE_CONFIG = {
    "allow_origins": ["*"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}  # Permite solicitudes desde cualquier origen

app = FastAPI(**FASTAPI_CONFIG, lifespan=lifespan)
app.add_middleware(CORSMiddleware, **MIDDLEWARE_CONFIG)

# Routers
app.include_router(asociacion.router, prefix="/asociacion", tags=["Asociacion"])
app.include_router(jugador.router, prefix="/jugador", tags=["Jugador"])
app.include_router(categoria.router, prefix="/categoria", tags=["Categoria"])
app.include_router(equipo.router, prefix="/equipo", tags=["Equipo"])
app.include_router(torneo.router, prefix="/torneo", tags=["Torneo"])

app.include_router(inscripciones.router, prefix="/inscripciones", tags=["Inscripciones"])
app.include_router(partido.router, prefix="/partido", tags=["Partido"])
app.include_router(fases.router, prefix="/fases", tags=["Fases"])

