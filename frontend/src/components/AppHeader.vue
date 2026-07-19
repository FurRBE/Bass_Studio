<template>
  <header class="app-header" :class="{ scrolled }">
    <div class="header-inner container">
      <router-link to="/" class="brand">
        <span class="brand-icon">🎸</span>
        <span class="brand-text">BASS STUDIO</span>
      </router-link>

      <nav class="header-nav" :class="{ open: mobileMenuOpen }">
        <router-link to="/" @click="closeMobile">首页</router-link>
        <router-link to="/customize" @click="closeMobile">定制贝斯</router-link>
        <template v-if="authStore.isLoggedIn">
          <router-link to="/profile" @click="closeMobile">个人中心</router-link>
          <router-link v-if="authStore.isAdmin" to="/admin" @click="closeMobile">后台管理</router-link>
          <a @click="handleLogout" class="logout-link">退出</a>
        </template>
        <template v-else>
          <router-link to="/login" @click="closeMobile">登录</router-link>
          <router-link to="/register" @click="closeMobile">
            <el-button type="primary" size="small" class="register-btn">注册</el-button>
          </router-link>
        </template>
      </nav>

      <button class="menu-toggle" @click="mobileMenuOpen = !mobileMenuOpen">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)
const scrolled = ref(false)

function handleLogout() {
  authStore.logout()
  mobileMenuOpen.value = false
  router.push('/')
}

function closeMobile() {
  mobileMenuOpen.value = false
}

function onScroll() {
  scrolled.value = window.scrollY > 50
}

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped lang="scss">
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(13, 13, 13, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;

  &.scrolled {
    border-bottom-color: var(--border-color);
    background: rgba(13, 13, 13, 0.95);
  }
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-primary);
  text-decoration: none;

  .brand-icon {
    font-size: 1.6rem;
  }

  .brand-text {
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: 3px;
    color: var(--accent);
  }
}

.header-nav {
  display: flex;
  align-items: center;
  gap: 8px;

  a {
    color: var(--text-secondary);
    padding: 8px 16px;
    border-radius: 6px;
    transition: all 0.2s;
    font-size: 0.9rem;
    text-decoration: none;

    &:hover:not(.logout-link) {
      color: var(--text-primary);
      background: var(--bg-card-hover);
    }

    &.router-link-exact-active,
    &.router-link-active.router-link-exact-active {
      color: var(--accent);
    }

    &.logout-link {
      color: var(--text-muted);
      cursor: pointer;

      &:hover {
        color: var(--danger);
      }
    }
  }

  .register-btn {
    margin-left: 4px;
  }
}

.menu-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;

  span {
    width: 24px;
    height: 2px;
    background: var(--text-primary);
    transition: all 0.3s;
  }
}

@media (max-width: 768px) {
  .menu-toggle {
    display: flex;
  }

  .header-nav {
    position: fixed;
    top: 64px;
    left: 0;
    right: 0;
    background: var(--bg-secondary);
    flex-direction: column;
    padding: 16px;
    gap: 4px;
    border-bottom: 1px solid var(--border-color);
    transform: translateY(-100%);
    opacity: 0;
    pointer-events: none;
    transition: all 0.3s ease;

    &.open {
      transform: translateY(0);
      opacity: 1;
      pointer-events: auto;
    }

    a {
      width: 100%;
      padding: 12px 16px;
    }
  }
}
</style>
