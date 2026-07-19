"""Bass Studio - FastAPI 应用入口"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .core.config import settings
from .database.base import Base
from .database.session import engine
from .routers import admin, admin_options, auth, options, orders
from .database import session

# 确保上传目录存在
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads" / "options"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def _migrate_db(conn):
    """为新版本添加缺失的数据库列（v1 → v2）"""
    import os
    from sqlalchemy import text

    db_path = session.DATA_DIR / "bassstudio.db"

    # 只在已有数据文件时进行迁移
    if not db_path.exists():
        return

    # 检查并添加 Order 表的新列
    new_columns = {
        "orders": [
            ("recipient_name", "VARCHAR(100)", "''"),
            ("recipient_phone", "VARCHAR(30)", "''"),
            ("address_line1", "VARCHAR(200)", "''"),
            ("address_line2", "VARCHAR(200)", "''"),
            ("city", "VARCHAR(100)", "''"),
            ("state", "VARCHAR(100)", "''"),
            ("zip_code", "VARCHAR(20)", "''"),
            ("notes", "TEXT", "''"),
        ],
        "bass_options": [
            ("image_url", "VARCHAR(500)", "NULL"),
        ],
    }

    for table, columns in new_columns.items():
        # 获取现有列
        result = await conn.execute(text(f"PRAGMA table_info({table})"))
        existing_columns = {row[1] for row in result.fetchall()}

        for col_name, col_type, col_default in columns:
            if col_name not in existing_columns:
                await conn.execute(text(
                    f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type} DEFAULT {col_default}"
                ))
                print(f"  [Migration] Added {table}.{col_name}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时创建表并执行迁移"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _migrate_db(conn)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="贝斯定制工作室 API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务 - 上传的图片
uploads_root = Path(__file__).resolve().parent.parent / "uploads"
uploads_root.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(uploads_root)), name="uploads")


# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"服务器内部错误: {str(exc)}"},
    )


# 注册路由
app.include_router(auth.router)
app.include_router(options.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(admin_options.router)


@app.get("/api/health", tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
