<template>
  <div class="dashboard-page">
    <h1 class="admin-page-title">仪表盘</h1>

    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="4" animated />
    </div>

    <div v-else class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon users-icon">
          <el-icon><UserFilled /></el-icon>
        </div>
        <div class="stat-body">
          <span class="stat-value">{{ stats.total_users }}</span>
          <span class="stat-label">用户总数</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon orders-icon">
          <el-icon><Document /></el-icon>
        </div>
        <div class="stat-body">
          <span class="stat-value">{{ stats.total_orders }}</span>
          <span class="stat-label">订单总数</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon pending-icon">
          <el-icon><Clock /></el-icon>
        </div>
        <div class="stat-body">
          <span class="stat-value">{{ stats.pending_orders }}</span>
          <span class="stat-label">待处理订单</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon completed-icon">
          <el-icon><CircleCheckFilled /></el-icon>
        </div>
        <div class="stat-body">
          <span class="stat-value">{{ stats.completed_orders }}</span>
          <span class="stat-label">已完成订单</span>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon options-icon">
          <el-icon><Setting /></el-icon>
        </div>
        <div class="stat-body">
          <span class="stat-value">{{ stats.total_options }}</span>
          <span class="stat-label">配置选项数</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { UserFilled, Document, Clock, CircleCheckFilled, Setting } from '@element-plus/icons-vue'
import { adminApi } from '@/api/admin'
import type { DashboardStats } from '@/types'

const stats = ref<DashboardStats>({
  total_users: 0,
  total_orders: 0,
  pending_orders: 0,
  completed_orders: 0,
  total_options: 0,
})
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await adminApi.getDashboard()
    stats.value = res.data
  } catch {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
})
</script>

<style scoped lang="scss">
.dashboard-page {
  padding: 0;
}

.admin-page-title {
  font-size: 1.6rem;
  color: var(--text-primary);
  margin-bottom: 32px;
  letter-spacing: 2px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 20px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 28px 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.2s;

  &:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
  }
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;

  &.users-icon {
    background: rgba(66, 165, 245, 0.15);
    color: var(--info);
  }

  &.orders-icon {
    background: rgba(200, 164, 92, 0.15);
    color: var(--accent);
  }

  &.pending-icon {
    background: rgba(255, 152, 0, 0.15);
    color: var(--warning);
  }

  &.completed-icon {
    background: rgba(76, 175, 80, 0.15);
    color: var(--success);
  }

  &.options-icon {
    background: rgba(156, 39, 176, 0.15);
    color: #9c27b0;
  }
}

.stat-body {
  display: flex;
  flex-direction: column;

  .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
  }

  .stat-label {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 2px;
  }
}
</style>
