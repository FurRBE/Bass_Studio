---
name: architecture-frontend
description: Vue 3 前端架构约定与模式
metadata:
  type: project
---

# 前端架构

## 技术栈

Vue 3 (Composition API) + TypeScript + Vite 6 + Element Plus + Pinia + Vue Router 4

## 目录结构

```
src/
├── api/           # axios 实例 (baseURL: /api) + 各模块 API
├── types/index.ts # 所有 TS 接口 + 中文映射常量
├── stores/        # Pinia: auth.ts, customize.ts
├── router/        # Vue Router history mode + 路由守卫
├── views/         # public/, user/, admin/
├── components/    # AppHeader, AppFooter
└── layouts/       # DefaultLayout, AdminLayout
```

## API 层 (`api/index.ts`)

- `axios.create({ baseURL: '/api', timeout: 10000 })`
- 请求拦截器：自动从 localStorage 读取 token 附加 Authorization: Bearer
- 响应拦截器：按状态码显示 ElMessage 错误提示；401 自动清除 token/user
- Vite 开发代理：`/api` → `http://127.0.0.1:8000`

## 路由 (`router/index.ts`)

| 路径 | 组件 | 权限 |
|------|------|------|
| / | HomePage | 公开 |
| /login | LoginPage | guest only |
| /register | RegisterPage | guest only |
| /customize | CustomizePage | 公开 |
| /profile | ProfilePage | requiresAuth |
| /orders/:id | OrderDetailPage | requiresAuth |
| /admin | AdminLayout → Dashboard/Users/Orders | requiresAdmin |
| /:pathMatch(.*)* | NotFoundPage | 公开 |

路由守卫：beforeEach 检查 requiresAuth、requiresAdmin、guest 三个 meta 标记

## 状态管理

### authStore
- `user`, `token` — 响应式状态 + localStorage 持久化
- `isLoggedIn` — computed from token
- `isAdmin` — computed from user.is_admin
- `fetchUser()` — 调用 /api/auth/me，失败则 logout
- 从 localStorage 恢复 user 用于刷新保持登录态

### customizeStore
- `selections: Record<string, BassOption>` — 按分类存储用户选择
- `basePrice = 5000` — 基础价格
- `totalPrice` — computed，basePrice + 各选项 price 累加
- `configuration` — computed，生成 OrderItem[] 供提交
- `selectOption`, `clearSelection`, `resetAll`

## 类型常量

- `CATEGORY_LABELS` — 8 个分类的中文名映射
- `ORDER_STATUS_LABELS` / `ORDER_STATUS_COLORS` — 5 种状态的中文名和 Element Plus 颜色

## Element Plus 约定

- 全局使用中文错误提示 (ElMessage)
- 表单使用 ElForm + ElInput 等组件
- 表格使用 ElTable
- 图标使用 @element-plus/icons-vue

**Why:** 前端所有组件和模式的标准参考。
**How to apply:** 新增页面遵循 views/ 目录按角色分类，API 调用统一通过 api/ 模块，类型定义统一放在 types/index.ts。
