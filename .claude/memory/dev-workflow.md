---
name: dev-workflow
description: 本地开发与部署的工作流
metadata:
  type: project
---

# 开发工作流

## 环境要求

- Node.js 20+
- Python 3.12+
- Windows (开发环境)

## 后端启动

```bash
cd backend
# 虚拟环境在 backend/venv/
# Windows: venv/Scripts/python 或 venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env        # 生产环境需修改 SECRET_KEY
python init_data.py          # 初始化管理员 + 配置选项
python run.py                # uvicorn --reload --port 8000
```

后端：http://localhost:8000, API 文档：http://localhost:8000/docs

## 前端启动

```bash
cd frontend
npm install
npm run dev                  # Vite dev server --port 5173
```

前端：http://localhost:5173，通过 Vite proxy 代理 /api 到后端。

## 默认管理员

| 字段 | 值 |
|------|-----|
| 用户名 | admin |
| 密码 | Admin@123456 |

⚠️ 首次部署后必须修改密码！

## 生产构建

```bash
cd frontend && npm run build   # 产物在 frontend/dist/
```

## 部署 (Ubuntu 24.04)

1. 克隆到 /opt/BassStudio
2. 后端：venv + pip install + .env + init_data.py
3. 前端：npm install + npm run build → /var/www/bassstudio
4. Nginx：deploy/nginx.conf.example → /etc/nginx/sites-available/
5. systemd：deploy/bassstudio.service.example → /etc/systemd/system/

## 权限设置 (Claude Code)

`.claude/settings.local.json` 中允许的命令：
- npm install/run
- Python 脚本 (init_data.py, 项目 venv 下的 python)
- curl (localhost API)
- 进程管理 (pkill, taskkill)

**Why:** 记录所有开发和部署的常用命令和环境信息。
**How to apply:** 启动开发环境时参考，部署到生产时参考 deploy/ 下的配置模板。
