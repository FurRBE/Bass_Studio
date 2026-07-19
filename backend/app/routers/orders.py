"""订单路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.deps import get_current_user
from ..database.session import get_db
from ..models.user import User
from ..schemas.order import CreateOrderRequest
from ..services import order_service

router = APIRouter(prefix="/api/orders", tags=["订单"])


@router.post("", status_code=201, summary="创建订单")
async def create_order(
    data: CreateOrderRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """创建新的贝斯定制订单"""
    order = await order_service.create_order(db, current_user, data)
    return {"message": "订单创建成功", "order_id": order.id}


@router.get("/me", summary="获取我的订单")
async def get_my_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取当前用户的订单列表"""
    return await order_service.get_user_orders(db, current_user, page, page_size)


@router.get("/{order_id}", summary="获取订单详情")
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取指定订单的详细信息"""
    return await order_service.get_order_detail(db, order_id, current_user)
