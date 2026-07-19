"""管理员路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.deps import get_admin_user
from ..database.session import get_db
from ..models.user import User
from ..schemas.order import UpdateOrderStatusRequest
from ..services import admin_service

router = APIRouter(prefix="/api/admin", tags=["管理员"])


@router.get("/dashboard", summary="仪表盘统计")
async def get_dashboard(
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """获取后台仪表盘统计数据"""
    return await admin_service.get_dashboard_stats(db)


@router.get("/users", summary="用户列表")
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    search: str | None = Query(None, description="搜索用户名或邮箱"),
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """获取用户列表（分页、搜索）"""
    return await admin_service.get_admin_users(db, page, page_size, search)


@router.delete("/users/{user_id}", summary="删除用户")
async def delete_user(
    user_id: int,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """删除指定用户"""
    await admin_service.delete_user(db, user_id)
    return {"message": "用户已删除"}


@router.get("/orders", summary="订单列表")
async def get_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    status: str | None = Query(None, description="按状态筛选"),
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """获取所有订单列表（分页、筛选）"""
    return await admin_service.get_admin_orders(db, page, page_size, status)


@router.get("/orders/{order_id}", summary="订单详情")
async def get_order_detail(
    order_id: int,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """获取指定订单详情"""
    return await admin_service.get_admin_order_detail(db, order_id)


@router.put("/orders/{order_id}/status", summary="更新订单状态")
async def update_order_status(
    order_id: int,
    data: UpdateOrderStatusRequest,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """更新订单状态"""
    return await admin_service.update_order_status(db, order_id, data.status)
