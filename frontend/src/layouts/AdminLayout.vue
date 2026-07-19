<template>
  <div class="admin-layout">
    <aside class="admin-sidebar">
      <div class="admin-brand">
        <router-link to="/admin">
          <h2>BASS STUDIO</h2>
          <span>后台管理</span>
        </router-link>
      </div>
      <nav class="admin-nav">
        <router-link to="/admin" class="nav-item" exact-active-class="active">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表盘</span>
        </router-link>
        <router-link to="/admin/users" class="nav-item" active-class="active">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </router-link>
        <router-link to="/admin/orders" class="nav-item" active-class="active">
          <el-icon><Document /></el-icon>
          <span>订单管理</span>
        </router-link>
        <el-divider style="border-color: #2a2a2a; margin: 16px 0;" />
        <a class="nav-item back-home" href="/">
          <el-icon><HomeFilled /></el-icon>
          <span>返回前台</span>
        </a>
        <a class="nav-item logout" @click.prevent="handleLogout">
          <el-icon><SwitchButton /></el-icon>
          <span>退出登录</span>
        </a>
      </nav>
    </aside>
    <main class="admin-main">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped lang="scss">
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-primary);
}

.admin-sidebar {
  width: 240px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  padding: 24px 0;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
}

.admin-brand {
  padding: 0 24px 24px;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 16px;

  h2 {
    font-size: 1.25rem;
    color: var(--accent);
    letter-spacing: 3px;
    margin-bottom: 4px;
  }

  span {
    font-size: 0.8rem;
    color: var(--text-muted);
  }
}

.admin-nav {
  flex: 1;
  padding: 0 12px;
  display: flex;
  flex-direction: column;

  .nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    border-radius: 8px;
    color: var(--text-secondary);
    transition: all 0.2s;
    cursor: pointer;
    font-size: 0.95rem;

    &:hover {
      background: var(--bg-card-hover);
      color: var(--text-primary);
    }

    &.active,
    &.router-link-exact-active {
      background: rgba(200, 164, 92, 0.1);
      color: var(--accent);
    }

    &.logout {
      margin-top: auto;
      color: var(--danger);

      &:hover {
        background: rgba(239, 83, 80, 0.1);
      }
    }
  }
}

.admin-main {
  flex: 1;
  margin-left: 240px;
  padding: 32px;
  min-height: 100vh;
}

@media (max-width: 768px) {
  .admin-sidebar {
    width: 64px;

    .admin-brand h2,
    .admin-brand span,
    .nav-item span {
      display: none;
    }

    .admin-brand {
      padding: 16px 12px;
      text-align: center;
    }

    .nav-item {
      justify-content: center;
      padding: 12px;
    }
  }

  .admin-main {
    margin-left: 64px;
    padding: 16px;
  }
}
</style>
