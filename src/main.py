import logging

from dotenv import load_dotenv

from src.config.swagger_configuration import swagger_config
from src.plugins import load_routes_plugin

"""Main module."""
from fastapi import FastAPI

logger = logging.getLogger("uvicorn")


def create_app() -> FastAPI:
    """App Factory function.

    Returns:
        FastAPI: Server Instance.
    """
    app = FastAPI(**swagger_config)
    load_dotenv()

    @app.get("/")
    async def root():
        return {"message": "Hello, FastAPI!"}

    load_routes_plugin(app)

    return app


app = create_app()
