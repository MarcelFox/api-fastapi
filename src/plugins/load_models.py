import importlib
from pathlib import Path


def load_models_plugin():
    """Dynamically load routes for each domain under app.
    Router files must be named as 'src/app/DOMAIN/routes.py'.

    Args:
        app (FastAPI): FastAPI main instance.
    """
    base_path = Path("src/app")
    for route_file in base_path.rglob("**/model.py"):
        module_path = route_file.relative_to(base_path).with_suffix("").as_posix()
        module = importlib.import_module(
            f"src.app.{module_path.replace('/', '.')}", "Base"
        )
        yield module.Base.metadata
