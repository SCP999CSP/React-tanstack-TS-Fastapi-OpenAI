from sqlmodel import Session, create_engine
from app.core.config import settings

engine = create_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=True,
    pool_size=10,           # 基础连接池大小
    max_overflow=20,        # 最大溢出连接数（总共最多 30 个连接）
    pool_timeout=30,        # 等待连接的超时时间（秒）
    pool_recycle=3600,      # 连接回收时间（1小时），防止连接过期
    pool_pre_ping=True,     # 连接前检查连接是否有效
)

