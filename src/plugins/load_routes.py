import importlib
from pathlib import Path
from fastapi import FastAPI


def load_routes_plugin(app: FastAPI):
    """Dynamically load routes for each domain under app.
    Router files must be named as 'src/app/DOMAIN/routes.py'.

    Args:
        app (FastAPI): FastAPI main instance.
    """
    base_path = Path("src/app")
    for route_file in base_path.rglob("routes.py"):
        module_path = route_file.relative_to(base_path).with_suffix("").as_posix()
        module_name = f"src.app.{module_path.replace('/', '.')}"
        prefix = f"/{module_path.split('/')[0]}"

        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "router"):
                app.include_router(module.router, prefix=prefix, tags=[prefix])
            else:
                print(f"Module {module_name} does not have a 'router' attribute.")
        except ModuleNotFoundError:
            print(f"Module {module_name} not found.")
