"""订单服务"""

import json

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order
from ..models.user import User
from ..schemas.order import CreateOrderRequest


async def create_order(
    db: AsyncSession, user: User, data: CreateOrderRequest
) -> Order:
    """创建订单"""
    configuration_json = json.dumps(
        [item.model_dump() for item in data.configuration],
        ensure_ascii=False,
    )

    order = Order(
        user_id=user.id,
        total_price=data.total_price,
        status="pending",
        configuration_json=configuration_json,
    )
    db.add(order)
    await db.flush()
    await db.refresh(order)

    return order


async def get_user_orders(
    db: AsyncSession, user: User, page: int = 1, page_size: int = 10
) -> dict:
    """获取用户订单列表"""
    offset = (page - 1) * page_size

    # 总数
    count_result = await db.execute(
        select(func.count()).select_from(Order).where(Order.user_id == user.id)
    )
    total = count_result.scalar() or 0

    # 分页查询
    result = await db.execute(
        select(Order)
        .where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    orders = result.scalars().all()

    items = []
    for o in orders:
        config = []
        try:
            config = json.loads(o.configuration_json) if o.configuration_json else []
        except (json.JSONDecodeError, TypeError):
            config = []

        items.append({
            "id": o.id,
            "user_id": o.user_id,
            "username": user.username,
            "total_price": o.total_price,
            "status": o.status,
            "configuration": config,
            "created_at": o.created_at.isoformat() if o.created_at else "",
            "updated_at": o.updated_at.isoformat() if o.updated_at else "",
        })

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


async def get_order_detail(
    db: AsyncSession, order_id: int, user: User | None = None
) -> dict:
    """获取订单详情"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在",
        )

    # 非管理员只能查看自己的订单
    if user and not user.is_admin and order.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权查看此订单",
        )

    config = []
    try:
        config = json.loads(order.configuration_json) if order.configuration_json else []
    except (json.JSONDecodeError, TypeError):
        config = []

    return {
        "id": order.id,
        "user_id": order.user_id,
        "username": user.username if user else None,
        "total_price": order.total_price,
        "status": order.status,
        "configuration": config,
        "created_at": order.created_at.isoformat() if order.created_at else "",
        "updated_at": order.updated_at.isoformat() if order.updated_at else "",
    }
