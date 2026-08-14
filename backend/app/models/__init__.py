"""导入所有模型，确保 Alembic 能够检测到它们。"""
# 直接从 model 模块导入，避免通过 __init__.py 导致的循环导入问题
from app.models.model import (
    Question,
    QuestionBase,
    QuestionPublic,
    QuestionDifficulty,
    ChallengeQuota,
)

__all__ = [
    "Question",
    "QuestionBase",
    "QuestionPublic",
    "QuestionDifficulty",
    "ChallengeQuota",
]



