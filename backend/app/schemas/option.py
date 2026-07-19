"""配置选项 Schema"""

from pydantic import BaseModel


class OptionResponse(BaseModel):
    """配置选项响应"""

    id: int
    category: str
    name: str
    description: str | None = ""
    price: int

    model_config = {"from_attributes": True}


class OptionsByCategory(BaseModel):
    """按分类的配置选项"""

    category: str
    options: list[OptionResponse]
