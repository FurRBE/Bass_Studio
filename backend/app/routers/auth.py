"""认证路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.deps import get_current_user
from ..database.session import get_db
from ..models.user import User
from ..schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserInfoResponse,
)
from ..services import auth_service

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", status_code=201, summary="用户注册")
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """注册新用户"""
    user = await auth_service.register_user(db, data)
    return {"message": "注册成功", "user_id": user.id}


@router.post("/login", response_model=TokenResponse, summary="用户登录")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """用户登录，返回 JWT Token"""
    return await auth_service.login_user(db, data.username, data.password)


@router.get("/me", response_model=UserInfoResponse, summary="获取当前用户信息")
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户的信息"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else "",
    }
