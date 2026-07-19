"""应用配置 - 通过环境变量读取"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """应用设置"""

    APP_NAME: str = "Bass Studio"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # 数据库 - 使用相对于 backend 目录的路径
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/bassstudio.db"

    # JWT
    SECRET_KEY: str = "change-me-to-a-random-secret-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 小时

    # 管理员默认账号
    ADMIN_USERNAME: str = "admin"
    ADMIN_EMAIL: str = "admin@bassstudio.com"
    ADMIN_PASSWORD: str = "Admin@123456"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


settings = Settings()
