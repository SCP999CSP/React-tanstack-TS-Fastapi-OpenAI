from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.model import Question, ChallengeQuota, QuestionDifficulty, Option
import uuid


def create_question(*, session: Session, 
    id: uuid.UUID,
    difficulty: QuestionDifficulty,
    question_description: str | None ,
    question_content: str,
    options: List[Option],
    correct_option_index: int,
    explanation: str,
    created_at: datetime,
    owner_id: str,
    ) -> Question:

    db_obj = Question(
        id=id,
        difficulty=difficulty,
        question_description=question_description,
        question_content=question_content,
        options=options,
        correct_option_index=correct_option_index,
        explanation=explanation,
        created_at=created_at,
        owner_id=owner_id,
    )
    session.add(db_obj)
    return db_obj

def get_questionslist_by_owner(*, session: Session, owner_id: str) -> list[Question]:
    """
    根据 owner_id 查询题目列表。
    """
    statement = select(Question).where(Question.owner_id == owner_id).order_by(Question.created_at.desc())
    questionslist: list[Question] = (session.exec(statement).all())
    return questionslist

def get_question_by_id(*, session: Session, question_id: uuid.UUID) -> Question:
    """
    根据 question_id 查询题目。
    """
    statement = select(Question).where(Question.id == question_id)
    question: Question = session.exec(statement).first()
    return question

def get_challenge_quota(*, session: Session, user_id: str) -> ChallengeQuota:
    """
    获取挑战次数。
    """
    statement = select(ChallengeQuota).where(ChallengeQuota.user_id == user_id)
    session_challenge_quota = session.exec(statement).first()
    return session_challenge_quota

def create_challenge_quota(*, session: Session, user_id: str) -> ChallengeQuota:
    """
    创建挑战次数。
    """
    db_obj = ChallengeQuota(
        user_id=user_id,
        remaining_quota=10,
        daily_quota=10
    )
    return db_obj

def get_and_reset_challenge_quota(*, session: Session, user_id: str) -> ChallengeQuota:
    """
    获取并每日重置挑战次数（一天最多一次）
    """
    quota = get_challenge_quota(session=session, user_id=user_id)

    if not quota:
        quota = create_challenge_quota(
            session=session,
            user_id=user_id
        )
        return quota
    
    now = datetime.now(timezone.utc)

    # 是否已经是同一天（UTC）
    if quota.last_reset_at.date() == now.date():
        # 今天已经重置过
        return quota

    # 执行重置
    quota.remaining_quota = quota.daily_quota
    quota.last_reset_at = now

    return quota