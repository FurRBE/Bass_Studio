<template>
  <DefaultLayout>
    <div class="profile-page">
      <div class="container">
        <h1 class="page-title">个人中心</h1>

        <!-- 用户信息卡片 -->
        <div class="profile-card">
          <div class="profile-avatar">
            <span>{{ authStore.user?.username?.charAt(0)?.toUpperCase() }}</span>
          </div>
          <div class="profile-info">
            <h2>{{ authStore.user?.username }}</h2>
            <p>{{ authStore.user?.email }}</p>
            <p class="register-date">
              注册时间：{{ formatDate(authStore.user?.created_at || '') }}
            </p>
            <el-tag v-if="authStore.isAdmin" type="warning" size="small">管理员</el-tag>
          </div>
        </div>

        <!-- 我的订单 -->
        <div class="orders-section">
          <h3>我的订单</h3>
          <div v-if="loading" class="loading-state">
            <el-skeleton :rows="3" animated />
          </div>
          <div v-else-if="orders.length === 0" class="empty-state">
            <el-empty description="暂无订单">
              <router-link to="/customize">
                <el-button type="primary">去定制贝斯</el-button>
              </router-link>
            </el-empty>
          </div>
          <div v-else class="orders-list">
            <div
              v-for="order in orders"
              :key="order.id"
              class="order-card"
              @click="$router.push(`/orders/${order.id}`)"
            >
              <div class="order-header">
                <span class="order-id">订单 #{{ String(order.id).padStart(6, '0') }}</span>
                <el-tag
                  :type="ORDER_STATUS_COLORS[order.status] as any"
                  size="small"
                >
                  {{ ORDER_STATUS_LABELS[order.status] || order.status }}
                </el-tag>
              </div>
              <div class="order-body">
                <span class="order-price">¥{{ order.total_price.toLocaleString() }}</span>
                <span class="order-date">{{ formatDate(order.created_at) }}</span>
              </div>
            </div>
          </div>

          <div class="pagination-wrap" v-if="total > pageSize">
            <el-pagination
              v-model:current-page="currentPage"
              :page-size="pageSize"
              :total="total"
              layout="prev, pager, next"
              @current-change="fetchOrders"
            />
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { useAuthStore } from '@/stores/auth'
import { ordersApi } from '@/api/orders'
import { ORDER_STATUS_LABELS, ORDER_STATUS_COLORS } from '@/types'
import type { OrderListItem } from '@/types'

const authStore = useAuthStore()
const orders = ref<OrderListItem[]>([])
const loading = ref(true)
const currentPage = ref(1)
const pageSize = 10
const total = ref(0)

onMounted(() => {
  fetchOrders()
})

async function fetchOrders() {
  loading.value = true
  try {
    const res = await ordersApi.getMyOrders(currentPage.value, pageSize)
    orders.value = res.data.items
    total.value = res.data.total
  } catch {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
}

function formatDate(dateStr: string) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}
</script>

<style scoped lang="scss">
.profile-page {
  min-height: calc(100vh - 200px);
  background: var(--bg-primary);
  padding: 48px 20px 80px;
}

.page-title {
  font-size: 1.8rem;
  color: var(--text-primary);
  letter-spacing: 2px;
  margin-bottom: 32px;
}

.profile-card {
  display: flex;
  align-items: center;
  gap: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 40px;
}

.profile-avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent), var(--accent-dark));
  display: flex;
  align-items: center;
  justify-content: center;

  span {
    font-size: 2rem;
    font-weight: 700;
    color: white;
  }
}

.profile-info {
  h2 {
    font-size: 1.3rem;
    color: var(--text-primary);
    margin-bottom: 4px;
  }

  p {
    color: var(--text-muted);
    font-size: 0.9rem;
  }

  .register-date {
    margin-top: 4px;
    font-size: 0.85rem;
  }
}

.orders-section {
  h3 {
    font-size: 1.2rem;
    color: var(--text-primary);
    margin-bottom: 20px;
    letter-spacing: 1px;
  }
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 20px 24px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--accent);
    background: var(--bg-card-hover);
  }
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;

  .order-id {
    font-weight: 600;
    color: var(--text-primary);
    font-family: monospace;
  }
}

.order-body {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .order-price {
    font-weight: 700;
    color: var(--accent);
    font-size: 1.1rem;
  }

  .order-date {
    color: var(--text-muted);
    font-size: 0.85rem;
  }
}

.pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.loading-state,
.empty-state {
  padding: 40px 0;
}

@media (max-width: 640px) {
  .profile-card {
    flex-direction: column;
    text-align: center;
  }
}
</style>
