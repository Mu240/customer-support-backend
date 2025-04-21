from sqlalchemy.ext.asyncio import AsyncEngine
from app.models.user import Base
from app.core.config import settings
from alembic import context
from logging.config import fileConfig

# Load Alembic configuration
config = context.config

# Set up logging
fileConfig(config.config_file_name)

# Set database URL from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Create async engine for migrations
connectable = AsyncEngine(create_async_engine(settings.DATABASE_URL))

def run_migrations_online():
    """
    Run migrations in online mode using an async connection.
    """
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()