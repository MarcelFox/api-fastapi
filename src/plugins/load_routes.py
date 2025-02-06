import importlib
from pathlib import Path
from fastapi import FastAPI

def load_routes_plugin(app: FastAPI):
    base_path = Path("src")
    for route_file in base_path.rglob('routes.py'):
        module_path = route_file.relative_to(base_path).with_suffix('').as_posix()
        module_name = f'src.{module_path.replace("/", ".")}'
        prefix = f'/{module_path.split("/")[0]}'

        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'router'):
                app.include_router(module.router, prefix=prefix)
            else:
                print(f"Module {module_name} does not have a 'router' attribute.")
        except ModuleNotFoundError:
            print(f"Module {module_name} not found.")
