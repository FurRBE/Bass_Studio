"""配置选项路由"""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.session import get_db
from ..models.option import BassOption
from ..schemas.option import OptionResponse, OptionsByCategory

router = APIRouter(prefix="/api/options", tags=["配置选项"])


@router.get("", summary="获取所有配置选项（按分类）")
async def get_all_options(db: AsyncSession = Depends(get_db)):
    """获取所有启用的配置选项，按分类组织"""
    result = await db.execute(
        select(BassOption)
        .where(BassOption.is_active == True)
        .order_by(BassOption.category, BassOption.price)
    )
    options = result.scalars().all()

    # 按分类组织
    categories: dict[str, list] = {}
    category_order = [
        "body", "neck", "fingerboard", "pickup", "bridge",
        "finish", "strings", "handedness",
    ]

    for opt in options:
        if opt.category not in categories:
            categories[opt.category] = []
        categories[opt.category].append({
            "id": opt.id,
            "category": opt.category,
            "name": opt.name,
            "description": opt.description or "",
            "price": opt.price,
            "image_url": opt.image_url,
        })

    # 按预定义顺序返回，新分类追加在末尾
    result_list = []
    for cat in category_order:
        if cat in categories:
            result_list.append({
                "category": cat,
                "options": categories[cat],
            })

    # 追加未在预定义顺序中的分类
    for cat, opts in categories.items():
        if cat not in category_order:
            result_list.append({
                "category": cat,
                "options": opts,
            })

    return result_list


@router.get("/{category}", summary="按分类获取配置选项")
async def get_options_by_category(
    category: str, db: AsyncSession = Depends(get_db)
):
    """获取指定分类的配置选项"""
    result = await db.execute(
        select(BassOption)
        .where(BassOption.category == category, BassOption.is_active == True)
        .order_by(BassOption.price)
    )
    options = result.scalars().all()

    return {
        "category": category,
        "options": [
            {
                "id": opt.id,
                "category": opt.category,
                "name": opt.name,
                "description": opt.description or "",
                "price": opt.price,
                "image_url": opt.image_url,
            }
            for opt in options
        ],
    }
