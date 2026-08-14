from fastapi import APIRouter
from app.api.routes import questions, quota

api_router = APIRouter()
api_router.include_router(questions.router)
api_router.include_router(quota.router)


