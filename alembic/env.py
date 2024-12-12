import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context

# Подгружаем путь к проекту, если нужно
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Импортируем наш DATABASE_URL из config.py
from config import DATABASE_URL
from models import Base  # Предполагаем, что Base описан в models.py

# Это Alembic Config объект, через него доступны настройки.
config = context.config

# Если используется файл конфигурации логирования, загружаем его
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Целевая метадата - метадата наших моделей
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме.
    В этом режиме мы не создаём Engine, а просто формируем SQL запросы.
    """
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме.
    В этом режиме мы создаём Engine и устанавливаем соединение с БД.
    """
    # Создаём движок из нашего URL
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
