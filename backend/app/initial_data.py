"""初始化数据库，创建所有表。"""
from sqlmodel import SQLModel
from app.core.db import engine
# 直接从 model 模块导入，避免通过 __init__.py 的导入问题
from app.models.model import Question, ChallengeQuota


def init_db() -> None:
    """初始化数据库，创建所有表。"""
    print("正在创建数据库表...")
    SQLModel.metadata.create_all(engine)
    print("✅ 数据库表创建成功！")


if __name__ == "__main__":
    init_db()

