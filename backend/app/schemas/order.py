"""订单相关 Schema"""

from typing import Optional

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    """订单中的配置项"""

    option_id: int
    category: str
    name: str
    price: int


class ShippingAddress(BaseModel):
    """收货地址"""

    recipient_name: str = Field(default="", max_length=100)
    recipient_phone: str = Field(default="", max_length=30)
    address_line1: str = Field(default="", max_length=200)
    address_line2: str = Field(default="", max_length=200)
    city: str = Field(default="", max_length=100)
    state: str = Field(default="", max_length=100)
    zip_code: str = Field(default="", max_length=20)
    notes: str = Field(default="", max_length=500)


class CreateOrderRequest(BaseModel):
    """创建订单请求"""

    total_price: int = Field(..., ge=0, description="总价")
    configuration: list[OrderItem] = Field(..., description="配置列表")
    shipping_address: ShippingAddress | None = Field(None, description="收货地址")


class ShippingAddressResponse(BaseModel):
    """收货地址响应"""

    recipient_name: str | None = ""
    recipient_phone: str | None = ""
    address_line1: str | None = ""
    address_line2: str | None = ""
    city: str | None = ""
    state: str | None = ""
    zip_code: str | None = ""
    notes: str | None = ""


class OrderResponse(BaseModel):
    """订单响应"""

    id: int
    user_id: int
    total_price: int
    status: str
    configuration: list | str | None = None
    shipping_address: ShippingAddressResponse | None = None
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
    shipping_address: ShippingAddressResponse | None = None
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
