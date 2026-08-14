from typing import Annotated
from fastapi import Depends, HTTPException, Request
from clerk_backend_api import Clerk, AuthenticateRequestOptions
from sqlmodel import SQLModel
from app.core.config import settings

clerk_sdk = Clerk(settings.CLERK_SECRET_KEY)


class CurrentUser(SQLModel):
    user_id: str


def authenticate_and_get_user_details(request: Request) -> CurrentUser:
    """
    FastAPI 认证依赖：
    - 验证 Clerk Token
    - 返回当前用户
    """
    try:
        # 调试：打印接收到的 Authorization header
        auth_header = request.headers.get("Authorization")
        
        
        request_status = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=[
                    "http://localhost:5173",  # Vite 默认端口
                    "http://127.0.0.1:5173",
                    "http://localhost:5174",  # 保留其他端口支持
                    "http://127.0.0.1:5174",  
                ],
                jwt_key=settings.JWKS_PUBLIC_KEY,
            ),
        )

        if not request_status.is_signed_in:
            print(f"DEBUG: User not signed in")
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_id = request_status.payload.get("sub")
        if not user_id:
            print(f"DEBUG: User ID not found in token payload")
            raise HTTPException(status_code=401, detail="User ID not found in token")

        print(f"DEBUG: Authentication successful for user: {user_id}")
        return CurrentUser(user_id=user_id)

    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Authentication error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Authentication error: {str(e)}",
        )


CurrentUserDep = Annotated[
    CurrentUser,
    Depends(authenticate_and_get_user_details),
]
