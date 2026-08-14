from typing import List, Dict, Any
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, ForeignKey, String, Enum as SQLEnum
from sqlmodel import Field, Relationship, SQLModel
from enum import Enum
from sqlalchemy.dialects.postgresql import JSONB

class QuestionDifficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Option(SQLModel):
    option_index: int
    option_text: str


class QuestionBase(SQLModel):
    """题目基础模型。"""
    difficulty: QuestionDifficulty = Field(default=QuestionDifficulty.easy, description="题目难度")
    question_description: str | None = Field(max_length=500, description="简短描述", nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="创建时间")


class QuestionList(QuestionBase):
    """题目列表模型。"""
    id: uuid.UUID = Field(description="题目id")


class QuestionPublic(QuestionBase):
    """题目公开响应模型。"""
    id: uuid.UUID = Field(description="题目id")
    options: List[Option] = Field(description="题目选项")
    correct_option_index: int = Field(description="正确选项索引")
    question_content: str = Field(max_length=1000, description="题目内容")
    explanation: str = Field(description="解释")

class Question(QuestionBase, table=True):
    """题目数据库表模型。"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: str = Field(sa_column=Column(String, ForeignKey("challengequota.user_id", ondelete="CASCADE"), index=True, nullable=False), description="题目所有者ID（Clerk用户ID）")
    difficulty: QuestionDifficulty = Field(sa_column=Column(SQLEnum(QuestionDifficulty), nullable=False), default=QuestionDifficulty.easy, description="题目难度")
    question_description: str | None = Field(sa_column=Column(String(500), nullable=True), description="简短描述")
    question_content: str = Field(sa_column=Column(String(1000), nullable=False), description="题目内容")
    options: List[Option] = Field(sa_column=Column(JSONB),description="题目选项")
    correct_option_index: int = Field(description="正确选项索引")
    explanation: str = Field(sa_column=Column(String, nullable=False), description="解释")
    owner: "ChallengeQuota" = Relationship(back_populates="questions")




class ChallengeQuotaBase(SQLModel):
    remaining_quota: int = Field(
        default=10, 
        description="剩余引用次数", 
        nullable=False,
        ge=0  # 确保不能为负数
    )
    daily_quota: int = Field(
        default=10,
        description="每日配额",
        nullable=False,
        ge=0
    )


class ChallengeQuotaPublic(ChallengeQuotaBase):
    """挑战配额响应模型。"""
    pass


class ChallengeQuota(ChallengeQuotaBase, table=True):
    """挑战配额数据库表模型。"""
    user_id: str = Field(primary_key=True, description="Clerk 用户 ID", nullable=False)
    questions: list["Question"] = Relationship(back_populates="owner",cascade_delete=True)
    last_reset_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="上一次配额重置时间（UTC）"
    )