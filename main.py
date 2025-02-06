"""Main module."""
from fastapi import FastAPI

def create_app() -> FastAPI:
    """App Factory function.

    Returns:
        FastAPI: Server Instance.
    """    
    app = FastAPI()
    
    @app.get("/")
    async def hello():
        return {"message": "Hello, FastAPI!"}
    
    return app

app = create_app()
