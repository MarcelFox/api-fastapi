import logging

from dotenv import load_dotenv
from pydantic import BaseModel

from src.config.swagger_configuration import swagger_config
from src.plugins import load_routes_plugin

"""Main module."""
from fastapi import FastAPI

logger = logging.getLogger("uvicorn")

class HealthResponse(BaseModel):
    message: str = 'ok'

def create_app() -> FastAPI:
    """App Factory function.

    Returns:
        FastAPI: Server Instance.
    """
    app = FastAPI(**swagger_config)
    load_dotenv()

    @app.get("/")
    async def health_check() -> HealthResponse:
        return {"message": "ok"}

    load_routes_plugin(app)

    return app


app = create_app()
