"""数据库会话管理"""

import os
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..core.config import settings

# 确保 data 目录存在
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 处理 SQLite 路径 - 确保是绝对路径
database_url = settings.DATABASE_URL
if "sqlite" in database_url:
    # 提取路径部分
    db_path = database_url.replace("sqlite+aiosqlite:///", "")
    if not os.path.isabs(db_path):
        db_path = str(DATA_DIR / "bassstudio.db")
    database_url = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    """获取数据库会话（FastAPI 依赖）"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
