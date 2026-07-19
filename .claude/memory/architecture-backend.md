---
name: architecture-backend
description: FastAPI 后端架构约定与模式
metadata:
  type: project
---

# 后端架构

## 分层结构

```
routers/ → services/ → models/ (SQLAlchemy)
         → schemas/  (Pydantic)
         → core/deps (Depends 注入)
```

## 关键文件

- `backend/app/main.py` — 应用入口：lifespan 建表、CORS 中间件、全局异常处理、路由注册、/api/health 健康检查
- `backend/app/core/config.py` — Pydantic Settings，读取 .env，SECRET_KEY 生产环境必须修改
- `backend/app/core/security.py` — passlib bcrypt 密码哈希 + python-jose JWT 生成/解码
- `backend/app/core/deps.py` — 三个 FastAPI 依赖：`get_current_user` (强制登录)、`get_admin_user` (管理员)、`get_optional_user` (可选登录)
- `backend/app/database/session.py` — AsyncSession 工厂，自动处理 data/ 目录创建和 SQLite 路径
- `backend/app/database/base.py` — SQLAlchemy DeclarativeBase

## 模型

- **User** — id, username(unique), email(unique), password_hash, is_admin, created_at
- **BassOption** — id, category, name, description, price, is_active, created_at
- **Order** — id, user_id(FK), total_price, status, configuration_json(Text), created_at, updated_at

## API 路由

| 前缀 | 文件 | 功能 |
|------|------|------|
| /api/auth | routers/auth.py | register, login, me |
| /api/options | routers/options.py | 按分类获取选项 |
| /api/orders | routers/orders.py | 创建/查看订单 (需登录) |
| /api/admin | routers/admin.py | 仪表盘、用户管理、订单管理 (需管理员) |

## 服务层

- `auth_service` — 注册检查重复/二次密码，登录支持用户名或邮箱
- `order_service` — 创建订单 (JSON序列化配置)、用户订单分页、订单详情 (权限检查)
- `admin_service` — 仪表盘统计、用户列表(分页+搜索)、删除用户(不能删管理员并级联删订单)、订单列表(分页+状态筛选)、更新订单状态

## 数据库约定

- SQLite，文件位置 `backend/data/bassstudio.db`
- 使用 aiosqlite 异步驱动
- 首次请求自动建表，init_data.py 初始化种子数据（跳过已存在）
- session 中间件自动 commit/rollback

**Why:** 后端分层职责清晰，是修改和扩展的参考。
**How to apply:** 新增功能时遵循 routers → services → models 的分层模式，依赖注入使用 core/deps.py。
