from fastapi import APIRouter, HTTPException
from app.crud.crud import get_and_reset_challenge_quota
from app.api.deps import SessionDep
from app.models.model import ChallengeQuotaPublic
from app.api.deps import CurrentUserDep

router = APIRouter(prefix="/quota", tags=["quota"])

@router.get("/quota", response_model=ChallengeQuotaPublic)
async def read_quota(*, session: SessionDep, current_user: CurrentUserDep):
    """
    根据 user_id 查询配额。
    """
    quota = get_and_reset_challenge_quota(
        session=session,
        user_id=current_user.user_id
    )
    if quota is None:
        raise HTTPException(status_code=404, detail="Quota not found")
    session.add(quota)
    session.commit()
    session.refresh(quota)
    
    return quota