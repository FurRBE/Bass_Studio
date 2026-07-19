---
name: project-overview
description: Bass Studio 项目概述 — 全栈贝斯定制工作室，用于学习练习
metadata:
  type: project
---

# Bass Studio — 项目概述

Bass Studio（贝斯定制工作室）是一个用于学习和练习的全栈 Web 应用，模拟贝斯定制工作室。用户可以配置和定制自己的贝斯，提交订单；管理员可以管理用户和订单。

**目的：** 学习练习项目，非生产商用。

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite + Element Plus + Pinia + Vue Router |
| 后端 | Python 3.12+ + FastAPI + SQLAlchemy 2.x + Pydantic |
| 数据库 | SQLite (aiosqlite) |
| 认证 | JWT (python-jose) + bcrypt 密码哈希 (passlib) |
| 部署 | Nginx + systemd + Ubuntu 24.04 |

## 项目结构

```
Bass_Studio/
├── frontend/          # Vue 3 SPA
│   └── src/
│       ├── api/       # axios 封装 + 拦截器
│       ├── views/     # public/ user/ admin/
│       ├── stores/    # Pinia (auth, customize)
│       ├── router/    # Vue Router (history mode)
│       ├── types/     # TS 类型 + 中文映射
│       ├── components/# AppHeader, AppFooter
│       └── layouts/   # DefaultLayout, AdminLayout
├── backend/           # FastAPI 应用
│   └── app/
│       ├── main.py    # 入口：lifespan, CORS, 路由注册
│       ├── core/      # config, security, deps
│       ├── database/  # session.py, base.py
│       ├── models/    # User, Order, BassOption
│       ├── schemas/   # Pydantic v2
│       ├── routers/   # auth, options, orders, admin
│       └── services/  # auth_service, order_service, admin_service
├── deploy/            # nginx.conf, systemd service
└── .claude/           # settings + memory
```

## 关键约定

- 价格单位：整数（元），基础价 5000，各选项叠加
- 订单状态：pending → confirmed → production → completed / cancelled
- 数据库：首次启动自动建表（lifespan），init_data.py 初始化种子数据
- API 前缀：/api/，全局异常处理，中文错误消息
- 前端 axios：自动带 token，401 自动清除登录态
- 所有开发命令在项目根目录下执行

**Why:** 项目整体概览，所有其他记忆以此为基础。
**How to apply:** 任何时候了解项目上下文时参考此文件。
