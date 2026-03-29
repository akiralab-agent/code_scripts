"""Ponto de entrada da aplicação FastAPI."""

from fastapi import FastAPI

from app.api.routes.run import router as run_router

app = FastAPI(
    title="Code Scripts API",
    description="API para execução dinâmica de scripts Python.",
    version="0.1.0",
)

app.include_router(run_router)
