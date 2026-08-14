from collections.abc import Generator
from typing import Annotated
from app.core.clerk import CurrentUser, authenticate_and_get_user_details
from fastapi import Depends, Header, HTTPException, status
from sqlmodel import Session
from app.core.db import engine


def get_db() -> Generator[Session, None, None]:
    """
    为每个请求创建数据库会话。
    请求结束时自动关闭会话。
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
CurrentUserDep = Annotated[CurrentUser, Depends(authenticate_and_get_user_details)]

