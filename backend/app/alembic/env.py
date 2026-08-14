from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 导入配置和数据库
from app.core.config import settings
from app.core.db import engine
# 导入所有模型，让 Alembic 能够检测到
from app.models.model import Question, ChallengeQuota
from sqlmodel import SQLModel

# Alembic 配置对象
config = context.config

# 设置数据库 URL
config.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_DATABASE_URI))

# 如果配置了日志，则使用它
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 目标元数据对象
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """在 'offline' 模式下运行迁移。

    这将配置上下文，只使用 URL，而不是 Engine，
    尽管这里也创建了 Engine 和连接，但不会使用它们。

    通过跳过 Engine 的创建，我们甚至不需要 DBAPI 可用。

    调用 context.execute() 来发出字符串到脚本输出。
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在 'online' 模式下运行迁移。

    在这种情况下，我们需要创建一个 Engine 并将其与连接关联。
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()



