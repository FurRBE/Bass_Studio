"""配置选项 Schema"""

from pydantic import BaseModel, Field


class OptionResponse(BaseModel):
    """配置选项响应"""

    id: int
    category: str
    name: str
    description: str | None = ""
    price: int
    image_url: str | None = None

    model_config = {"from_attributes": True}


class OptionsByCategory(BaseModel):
    """按分类的配置选项"""

    category: str
    options: list[OptionResponse]


# ========== Admin Schemas ==========

class AdminOptionResponse(BaseModel):
    """管理员查看配置选项（含 is_active / created_at）"""

    id: int
    category: str
    name: str
    description: str | None = ""
    price: int
    image_url: str | None = None
    is_active: bool
    created_at: str

    model_config = {"from_attributes": True}


class AdminOptionListResponse(BaseModel):
    """管理员配置选项列表"""

    total: int
    page: int
    page_size: int
    items: list[AdminOptionResponse]


class CreateOptionRequest(BaseModel):
    """创建配置选项请求"""

    category: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    price: int = Field(default=0, ge=0)
    image_url: str | None = None
    is_active: bool = True


class UpdateOptionRequest(BaseModel):
    """更新配置选项请求（所有字段可选）"""

    category: str | None = Field(None, min_length=1, max_length=50)
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: int | None = Field(None, ge=0)
    image_url: str | None = None
    is_active: bool | None = None


class RenameCategoryRequest(BaseModel):
    """重命名分类请求"""

    new_name: str = Field(..., min_length=1, max_length=50)


class CategoryItem(BaseModel):
    """分类条目"""

    name: str
    count: int
