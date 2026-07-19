"""管理员服务"""

import json

from fastapi import HTTPException, status
from sqlalchemy import func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order
from ..models.user import User


async def get_dashboard_stats(db: AsyncSession) -> dict:
    """获取仪表盘统计数据"""
    # 用户总数
    user_count_result = await db.execute(
        select(func.count()).select_from(User)
    )
    total_users = user_count_result.scalar() or 0

    # 订单总数
    order_count_result = await db.execute(
        select(func.count()).select_from(Order)
    )
    total_orders = order_count_result.scalar() or 0

    # 待处理订单
    pending_result = await db.execute(
        select(func.count()).select_from(Order).where(Order.status == "pending")
    )
    pending_orders = pending_result.scalar() or 0

    # 已完成订单
    completed_result = await db.execute(
        select(func.count()).select_from(Order).where(Order.status == "completed")
    )
    completed_orders = completed_result.scalar() or 0

    return {
        "total_users": total_users,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
    }


async def get_admin_users(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
) -> dict:
    """获取用户列表（管理员）"""
    offset = (page - 1) * page_size

    query = select(User)
    count_query = select(func.count()).select_from(User)

    if search:
        search_filter = or_(
            User.username.ilike(f"%{search}%"),
            User.email.ilike(f"%{search}%"),
        )
        query = query.where(search_filter)
        count_query = count_query.where(search_filter)

    # 总数
    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    # 分页
    result = await db.execute(
        query.order_by(User.id.desc()).offset(offset).limit(page_size)
    )
    users = result.scalars().all()

    items = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
            "created_at": u.created_at.isoformat() if u.created_at else "",
        }
        for u in users
    ]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


async def delete_user(db: AsyncSession, user_id: int) -> None:
    """删除用户（管理员）"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除管理员账号",
        )

    # 删除该用户的订单
    await db.execute(
        select(Order).where(Order.user_id == user_id)
    )
    orders_result = await db.execute(
        select(Order).where(Order.user_id == user_id)
    )
    for order in orders_result.scalars().all():
        await db.delete(order)

    await db.delete(user)


async def get_admin_orders(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 10,
    status_filter: str | None = None,
) -> dict:
    """获取订单列表（管理员）"""
    offset = (page - 1) * page_size

    query = select(Order)
    count_query = select(func.count()).select_from(Order)

    if status_filter:
        query = query.where(Order.status == status_filter)
        count_query = count_query.where(Order.status == status_filter)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    result = await db.execute(
        query.order_by(Order.created_at.desc()).offset(offset).limit(page_size)
    )
    orders = result.scalars().all()

    items = []
    for o in orders:
        # 获取用户名
        user_result = await db.execute(select(User).where(User.id == o.user_id))
        order_user = user_result.scalar_one_or_none()

        config = []
        try:
            config = json.loads(o.configuration_json) if o.configuration_json else []
        except (json.JSONDecodeError, TypeError):
            config = []

        items.append({
            "id": o.id,
            "user_id": o.user_id,
            "username": order_user.username if order_user else "未知",
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


async def update_order_status(
    db: AsyncSession, order_id: int, new_status: str
) -> dict:
    """更新订单状态"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在",
        )

    order.status = new_status
    await db.flush()
    await db.refresh(order)

    config = []
    try:
        config = json.loads(order.configuration_json) if order.configuration_json else []
    except (json.JSONDecodeError, TypeError):
        config = []

    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_price": order.total_price,
        "status": order.status,
        "configuration": config,
        "created_at": order.created_at.isoformat() if order.created_at else "",
        "updated_at": order.updated_at.isoformat() if order.updated_at else "",
    }


async def get_admin_order_detail(db: AsyncSession, order_id: int) -> dict:
    """获取订单详情（管理员）"""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在",
        )

    user_result = await db.execute(select(User).where(User.id == order.user_id))
    order_user = user_result.scalar_one_or_none()

    config = []
    try:
        config = json.loads(order.configuration_json) if order.configuration_json else []
    except (json.JSONDecodeError, TypeError):
        config = []

    return {
        "id": order.id,
        "user_id": order.user_id,
        "username": order_user.username if order_user else "未知",
        "total_price": order.total_price,
        "status": order.status,
        "configuration": config,
        "created_at": order.created_at.isoformat() if order.created_at else "",
        "updated_at": order.updated_at.isoformat() if order.updated_at else "",
    }
