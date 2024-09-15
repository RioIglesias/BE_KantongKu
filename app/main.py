import logging
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from app.core.config import config
from app.api.main import api_router

app = FastAPI(
    title="Skripsi",
)


@app.get("/huhu", include_in_schema=False)
async def health() -> JSONResponse:
    return {
        "db_url": config.db_url,
        "environment": config.environment,
        "log_level": config.log_level,
    }


app.include_router(api_router, prefix="/api")
    