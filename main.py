from src.plugins import load_routes_plugin
from src.config.swagger_configuration import swagger_config

"""Main module."""
from fastapi import FastAPI

def create_app() -> FastAPI:
    """App Factory function.

    Returns:
        FastAPI: Server Instance.
    """    
    app = FastAPI(**swagger_config)
    
    @app.get("/")
    async def root():
        return {"message": "Hello, FastAPI!"}
    
    load_routes_plugin(app)
    
    return app

app = create_app()
