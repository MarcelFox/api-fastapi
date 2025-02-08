from logging.config import fileConfig

from sqlalchemy import NullPool, MetaData

from src.plugins import load_models_plugin

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# load_models_plugin()
# target_metadata = MetaData()
# target_metadata = target_metadata.union(*[metadata for metadata in load_models_plugin()])

# print([metadata for metadata in load_models_plugin()])

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config

# Read Alembic configuration
config = context.config

# Create an async engine
connectable = async_engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    poolclass=NullPool,
)

async def run_migrations():
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

def do_run_migrations(connection):
    all_metadata = MetaData()
    
    for metadata in load_models_plugin():
        for table in metadata.tables.values():
            table.tometadata(all_metadata)
    context.configure(connection=connection, target_metadata=all_metadata)
    with context.begin_transaction():
        context.run_migrations()

asyncio.run(run_migrations())
