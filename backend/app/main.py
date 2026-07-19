"""Bass Studio - FastAPI 应用入口"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .database.base import Base
from .database.session import engine
from .routers import admin, auth, options, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时创建表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
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


@app.get("/api/health", tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}
