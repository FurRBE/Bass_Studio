# 🎸 Bass Studio - 贝斯定制工作室

一个用于学习和练习的全栈 Web 应用，模拟贝斯定制工作室。用户可以在线配置和定制自己的贝斯，提交订单；管理员可以管理用户和订单。

## v2.0 更新

- 🖼️ **配置选项可视化管理** — 管理员可在后台可视化增删改查贝斯配置选项，支持上传示例图片
- 🖨️ **订单打印** — 一键生成专业订单确认单并打印
- 📦 **收货地址** — 下单时填写收货信息，订单详情展示完整配送地址
- 📊 **仪表盘增强** — 新增配置选项数量统计
- 🗂️ **分类管理** — 支持动态创建、重命名、删除配置分类

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite + Element Plus + Pinia + Vue Router |
| 后端 | Python 3.12+ + FastAPI + SQLAlchemy 2.x + Pydantic |
| 数据库 | SQLite |
| 认证 | JWT + bcrypt 密码哈希 |
| 部署 | Nginx + systemd + Ubuntu 24.04 |

## 项目结构

```
BassStudio/
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── api/             # API 请求封装
│   │   ├── assets/          # 静态资源 & 全局样式
│   │   ├── components/      # 通用组件
│   │   ├── layouts/         # 布局组件
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── types/           # TypeScript 类型定义
│   │   ├── utils/          # 工具函数（打印等）
│   │   └── views/           # 页面
│   │       ├── public/      # 公开页面
│   │       ├── user/        # 用户页面
│   │       └── admin/       # 管理员页面
│   ├── package.json
│   └── vite.config.ts
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── main.py          # 应用入口
│   │   ├── core/            # 配置、安全、依赖注入
│   │   ├── database/        # 数据库连接与 Base
│   │   ├── models/          # SQLAlchemy 模型
│   │   ├── schemas/         # Pydantic Schema
│   │   ├── routers/         # API 路由
│   │   └── services/        # 业务逻辑
│   ├── data/                # SQLite 数据库文件
│   ├── requirements.txt
│   ├── .env.example
│   ├── run.py               # 开发启动脚本
│   └── init_data.py         # 数据初始化脚本
├── deploy/                  # 部署配置
│   ├── nginx.conf.example
│   ├── bassstudio.service.example
│   └── README.md
├── .gitignore
└── README.md
```

## 功能

### 前台

- 🏠 **首页** - 品牌展示，工作室介绍，定制流程，精选作品
- 📝 **用户注册** - 用户名/邮箱/密码注册
- 🔑 **用户登录** - JWT 认证，支持用户名或邮箱登录
- 🎸 **贝斯配置器** - 选择琴体、琴颈、指板、拾音器、琴桥、颜色、弦数、左右手，实时计算价格
- 👤 **个人中心** - 查看个人信息和订单历史
- 📋 **订单详情** - 查看订单完整配置和状态

### 后台管理

- 📊 **仪表盘** - 用户数、订单数、选项数统计
- 👥 **用户管理** - 用户列表、搜索、删除
- 📦 **订单管理** - 订单列表、状态筛选、状态更新、打印订单
- ⚙️ **配置管理** - 可视化增删改查贝斯配置选项，上传示例图片，分类管理

## 本地开发

### 环境要求

- Node.js 20+
- Python 3.12+
- Git

### 后端启动

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env

# 初始化数据（创建管理员和配置选项）
python init_data.py

# 启动开发服务器
python run.py
# 或: uvicorn app.main:app --reload --port 8000
```

后端启动后访问: http://localhost:8000

API 文档: http://localhost:8000/docs

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端启动后访问: http://localhost:5173

### 默认管理员账号

| 字段 | 值 |
|------|-----|
| 用户名 | `admin` |
| 密码 | `Admin@123456` |

⚠️ **首次部署后请立即修改密码！**

## API 文档

启动后端后访问：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 生产环境构建

```bash
cd frontend
npm run build
```

构建产物在 `frontend/dist/` 目录。

## 部署到 Ubuntu 服务器

详见 [deploy/README.md](deploy/README.md)

快速步骤：

1. `git clone` 项目到 `/opt/BassStudio`
2. 安装 Python 依赖，配置 `.env`
3. 运行 `python init_data.py` 初始化数据库
4. 构建前端：`npm install && npm run build`
5. 配置 Nginx 反向代理
6. 使用 systemd 运行 FastAPI

## 环境变量

参考 `backend/.env.example`：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SECRET_KEY` | JWT 密钥 | 生产环境必须修改 |
| `DATABASE_URL` | 数据库连接 | `sqlite+aiosqlite:///./data/bassstudio.db` |
| `ADMIN_USERNAME` | 管理员用户名 | `admin` |
| `ADMIN_PASSWORD` | 管理员密码 | `Admin@123456` |
| `CORS_ORIGINS` | 允许的跨域来源 | `["http://localhost:5173"]` |

## 常见问题

### Q: 数据库文件在哪里？

`backend/data/bassstudio.db`，首次启动自动创建。

### Q: 忘记管理员密码怎么办？

删除 `backend/data/bassstudio.db`，重新运行 `python init_data.py`。

### Q: 前端请求后端报 CORS 错误？

检查 `backend/.env` 中的 `CORS_ORIGINS` 是否包含前端地址。

### Q: Windows 上运行报错？

确保使用 Python 3.12+，且安装所有依赖。路径使用正斜杠 `/`。

## 后续可扩展功能

- 图片上传（贝斯配置可视化）
- 邮件通知（订单状态变更）
- 支付集成
- 多语言支持
- 配置选项动态管理（后台增删改）
- 数据导出（CSV/Excel）
- 单元测试和 E2E 测试
- Docker 部署
- HTTPS 配置
- Redis 缓存
- 评价系统
- 实时聊天客服

## License

MIT - 仅供学习练习使用
