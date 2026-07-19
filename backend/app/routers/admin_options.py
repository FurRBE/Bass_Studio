"""管理员 - 配置选项管理路由"""

from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.deps import get_admin_user
from ..database.session import get_db
from ..models.user import User
from ..schemas.option import (
    CreateOptionRequest,
    OptionResponse,
    RenameCategoryRequest,
    UpdateOptionRequest,
)
from ..services import options_service

router = APIRouter(prefix="/api/admin/options", tags=["管理员-配置管理"])


@router.get("", summary="获取所有配置选项（管理员）")
async def list_options(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: str | None = Query(None, description="按分类筛选"),
    is_active: bool | None = Query(None, description="按启用状态筛选"),
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """获取所有配置选项（含未启用的），支持分页和筛选"""
    return await options_service.get_admin_options(
        db, page=page, page_size=page_size, category=category, is_active=is_active
    )


@router.post("", status_code=201, summary="新增配置选项")
async def create_option(
    data: CreateOptionRequest,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """新增一个贝斯配置选项"""
    return await options_service.create_option(db, data.model_dump())


@router.put("/{option_id}", summary="更新配置选项")
async def update_option(
    option_id: int,
    data: UpdateOptionRequest,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """更新指定配置选项"""
    # 只传非 None 的字段
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    return await options_service.update_option(db, option_id, update_data)


@router.delete("/{option_id}", summary="删除配置选项")
async def delete_option(
    option_id: int,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """永久删除指定配置选项"""
    await options_service.delete_option(db, option_id)
    return {"message": "配置选项已删除"}


@router.post("/upload-image", summary="上传选项图片")
async def upload_option_image(
    file: UploadFile = File(..., description="图片文件（jpg/png/gif/webp/svg）"),
    admin_user: User = Depends(get_admin_user),
):
    """上传选项示例图片，返回图片 URL"""
    url = await options_service.save_upload_image(file, admin_user.id)
    return {"image_url": url, "message": "上传成功"}


@router.get("/categories", summary="获取所有分类")
async def list_categories(
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """获取所有不同的分类名称及其选项数量"""
    return await options_service.get_categories(db)


@router.put("/categories/{old_name}/rename", summary="重命名分类")
async def rename_category_by_path(
    old_name: str,
    data: RenameCategoryRequest,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """将某个分类下的所有选项迁移到新分类名"""
    return await options_service.rename_category(db, old_name, data.new_name)
