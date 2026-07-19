"""配置选项管理服务"""

import os
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.option import BassOption

# 图片上传目录
UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads" / "options"


async def ensure_upload_dir():
    """确保上传目录存在"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_upload_image(file: UploadFile, admin_user_id: int) -> str:
    """保存上传的图片，返回访问 URL 路径"""
    await ensure_upload_dir()

    # 验证文件类型
    allowed_types = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/svg+xml"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的图片格式: {file.content_type}，支持 jpg/png/gif/webp/svg",
        )

    # 生成唯一文件名
    ext = os.path.splitext(file.filename or "image.jpg")[1] or ".jpg"
    safe_ext = ext.lower() if ext.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"} else ".jpg"
    filename = f"{uuid.uuid4().hex}{safe_ext}"
    filepath = UPLOAD_DIR / filename

    # 保存文件
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB 限制
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="图片大小不能超过 10MB",
        )

    with open(filepath, "wb") as f:
        f.write(content)

    # 返回相对于 /uploads/ 的路径
    return f"/uploads/options/{filename}"


async def get_admin_options(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    category: str | None = None,
    is_active: bool | None = None,
) -> dict:
    """获取配置选项列表（管理员）"""
    offset = (page - 1) * page_size

    query = select(BassOption)
    count_query = select(func.count()).select_from(BassOption)

    if category:
        query = query.where(BassOption.category == category)
        count_query = count_query.where(BassOption.category == category)

    if is_active is not None:
        query = query.where(BassOption.is_active == is_active)
        count_query = count_query.where(BassOption.is_active == is_active)

    count_result = await db.execute(count_query)
    total = count_result.scalar() or 0

    result = await db.execute(
        query.order_by(BassOption.category, BassOption.price).offset(offset).limit(page_size)
    )
    options = result.scalars().all()

    items = [
        {
            "id": opt.id,
            "category": opt.category,
            "name": opt.name,
            "description": opt.description or "",
            "price": opt.price,
            "image_url": opt.image_url,
            "is_active": opt.is_active,
            "created_at": opt.created_at.isoformat() if opt.created_at else "",
        }
        for opt in options
    ]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items,
    }


async def create_option(db: AsyncSession, data: dict) -> dict:
    """创建配置选项"""
    option = BassOption(**data)
    db.add(option)
    await db.flush()
    await db.refresh(option)

    return {
        "id": option.id,
        "category": option.category,
        "name": option.name,
        "description": option.description or "",
        "price": option.price,
        "image_url": option.image_url,
        "is_active": option.is_active,
        "created_at": option.created_at.isoformat() if option.created_at else "",
    }


async def update_option(db: AsyncSession, option_id: int, data: dict) -> dict:
    """更新配置选项"""
    result = await db.execute(select(BassOption).where(BassOption.id == option_id))
    option = result.scalar_one_or_none()

    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置选项不存在",
        )

    # 只更新传入的字段
    for key, value in data.items():
        if value is not None:
            setattr(option, key, value)

    await db.flush()
    await db.refresh(option)

    return {
        "id": option.id,
        "category": option.category,
        "name": option.name,
        "description": option.description or "",
        "price": option.price,
        "image_url": option.image_url,
        "is_active": option.is_active,
        "created_at": option.created_at.isoformat() if option.created_at else "",
    }


async def delete_option(db: AsyncSession, option_id: int) -> None:
    """删除配置选项"""
    result = await db.execute(select(BassOption).where(BassOption.id == option_id))
    option = result.scalar_one_or_none()

    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="配置选项不存在",
        )

    await db.delete(option)


async def get_categories(db: AsyncSession) -> list[dict]:
    """获取所有分类及其选项数量"""
    result = await db.execute(
        select(BassOption.category, func.count(BassOption.id))
        .group_by(BassOption.category)
        .order_by(BassOption.category)
    )
    rows = result.all()

    return [{"name": row[0], "count": row[1]} for row in rows]


async def rename_category(db: AsyncSession, old_name: str, new_name: str) -> dict:
    """重命名分类"""
    result = await db.execute(
        select(BassOption).where(BassOption.category == old_name)
    )
    options = result.scalars().all()

    if not options:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"分类 '{old_name}' 不存在",
        )

    for opt in options:
        opt.category = new_name

    await db.flush()

    return {
        "old_name": old_name,
        "new_name": new_name,
        "updated_count": len(options),
    }
