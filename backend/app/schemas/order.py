"""订单相关 Schema"""

from typing import Optional

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    """订单中的配置项"""

    option_id: int
    category: str
    name: str
    price: int


class CreateOrderRequest(BaseModel):
    """创建订单请求"""

    total_price: int = Field(..., ge=0, description="总价")
    configuration: list[OrderItem] = Field(..., description="配置列表")


class OrderResponse(BaseModel):
    """订单响应"""

    id: int
    user_id: int
    total_price: int
    status: str
    configuration: list | str | None = None
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class OrderListItem(BaseModel):
    """订单列表项"""

    id: int
    user_id: int
    username: Optional[str] = None
    total_price: int
    status: str
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    """订单列表"""

    total: int
    page: int
    page_size: int
    items: list[OrderListItem]


class UpdateOrderStatusRequest(BaseModel):
    """更新订单状态"""

    status: str = Field(..., pattern="^(pending|confirmed|production|completed|cancelled)$")
