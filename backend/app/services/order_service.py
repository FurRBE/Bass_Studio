"""订单服务"""

import json

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order
from ..models.user import User
from ..schemas.order import CreateOrderRequest, ShippingAddress


def _build_shipping_address(order: Order) -> dict:
    """从 order 模型提取收货地址"""
    return {
        "recipient_name": order.recipient_name or "",
        "recipient_phone": order.recipient_phone or "",
        "address_line1": order.address_line1 or "",
        "address_line2": order.address_line2 or "",
        "city": order.city or "",
        "state": order.state or "",
        "zip_code": order.zip_code or "",
        "notes": order.notes or "",
    }


def _order_to_response(order: Order, username: str | None = None) -> dict:
    """将 order 模型转换为响应 dict"""
    config = []
    try:
        config = json.loads(order.configuration_json) if order.configuration_json else []
    except (json.JSONDecodeError, TypeError):
        config = []

    result = {
        "id": order.id,
        "user_id": order.user_id,
        "total_price": order.total_price,
        "status": order.status,
        "configuration": config,
        "shipping_address": _build_shipping_address(order),
        "created_at": order.created_at.isoformat() if order.created_at else "",
        "updated_at": order.updated_at.isoformat() if order.updated_at else "",
    }

    if username is not None:
        result["username"] = username

    return result


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

    # 写入收货地址
    if data.shipping_address:
        addr = data.shipping_address
        order.recipient_name = addr.recipient_name or ""
        order.recipient_phone = addr.recipient_phone or ""
        order.address_line1 = addr.address_line1 or ""
        order.address_line2 = addr.address_line2 or ""
        order.city = addr.city or ""
        order.state = addr.state or ""
        order.zip_code = addr.zip_code or ""
        order.notes = addr.notes or ""

    db.add(order)
    await db.flush()
    await db.refresh(order)

    return order


async def get_user_orders(
    db: AsyncSession, user: User, page: int = 1, page_size: int = 10
) -> dict:
    """获取用户订单列表"""
    offset = (page - 1) * page_size

    count_result = await db.execute(
        select(func.count()).select_from(Order).where(Order.user_id == user.id)
    )
    total = count_result.scalar() or 0

    result = await db.execute(
        select(Order)
        .where(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    orders = result.scalars().all()

    items = [_order_to_response(o, username=user.username) for o in orders]

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

    username = user.username if user else None

    # 如果不是自己的订单，查询用户名
    if user and user.is_admin and order.user_id != user.id:
        user_result = await db.execute(select(User).where(User.id == order.user_id))
        order_user = user_result.scalar_one_or_none()
        username = order_user.username if order_user else "未知"

    return _order_to_response(order, username=username)
