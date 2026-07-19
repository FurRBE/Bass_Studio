"""用户相关 Schema"""

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """用户响应（不含密码）"""

    id: int
    username: str
    email: str
    is_admin: bool
    created_at: str

    model_config = {"from_attributes": True}


class AdminUserListItem(BaseModel):
    """管理员查看用户列表项"""

    id: int
    username: str
    email: str
    is_admin: bool
    created_at: str

    model_config = {"from_attributes": True}


class AdminUserListResponse(BaseModel):
    """管理员查看用户列表"""

    total: int
    page: int
    page_size: int
    items: list[AdminUserListItem]
