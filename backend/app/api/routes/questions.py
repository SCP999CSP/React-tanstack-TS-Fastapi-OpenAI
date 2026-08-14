from datetime import datetime, timezone
from typing import List
import uuid
import app.crud.crud as crud
from fastapi import APIRouter, HTTPException
from app.api.ai_generator import generate_question_with_ai
from app.api.deps import CurrentUserDep, SessionDep
from app.crud.crud import create_question, get_and_reset_challenge_quota, get_question_by_id, get_questionslist_by_owner
from app.models.model import Question, QuestionDifficulty, QuestionList, QuestionPublic


router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("questionlist", response_model=List[QuestionList])
async def read_questionslist(*, session: SessionDep, current_user: CurrentUserDep):
    """
    根据 user_id 查询题目列表。
    """
    questions = get_questionslist_by_owner(
        session=session,
        owner_id=current_user.user_id
    )
    # 将 Question 对象转换为 QuestionList 对象
    return [QuestionList.model_validate(q) for q in questions]

@router.get("/{question_id}", response_model=QuestionPublic)
async def read_question(*, session: SessionDep, current_user: CurrentUserDep, question_id: uuid.UUID):
    """
    根据 question_id 查询完整题目与答案。
    """
    question = get_question_by_id(
        session=session,
        question_id=question_id
    )
    if question.owner_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return question

@router.post("/", response_model=QuestionPublic)
async def create_question(*, session: SessionDep, current_user: CurrentUserDep, difficulty: QuestionDifficulty
) -> QuestionPublic:

    """
    创建题目。
    """
    try:
        quota = get_and_reset_challenge_quota(
            session=session,
            user_id=current_user.user_id
        )
        if quota is None:
            raise HTTPException(status_code=404, detail="Quota not found")
        if quota.remaining_quota <= 0:
            raise HTTPException(status_code=429, detail="Quota exhausted")

        question_data = generate_question_with_ai(difficulty)
        question = crud.create_question(
            session=session,
            id=uuid.uuid4(),
            difficulty=difficulty,
            question_description=question_data["question_description"],
            question_content=question_data["question_content"],
            options=question_data["options"],
            correct_option_index=question_data["correct_option_index"],
            explanation=question_data["explanation"],
            created_at=datetime.now(timezone.utc),
            owner_id=current_user.user_id
        )
        quota.remaining_quota -= 1
        session.add(quota)
        session.commit()
        session.refresh(quota)
        session.refresh(question)
        return question
    except HTTPException as e:
        raise e
    


    
