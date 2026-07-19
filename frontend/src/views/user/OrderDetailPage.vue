<template>
  <DefaultLayout>
    <div class="order-detail-page">
      <div class="container">
        <div class="page-header">
          <el-button text @click="$router.back()">
            <el-icon><ArrowLeft /></el-icon> 返回
          </el-button>
          <h1>订单详情</h1>
          <el-button v-if="order" @click="handlePrint" style="margin-left: auto;">
            <el-icon><Printer /></el-icon> 打印订单
          </el-button>
        </div>

        <div v-if="loading" class="loading-state">
          <el-skeleton :rows="6" animated />
        </div>

        <div v-else-if="order" class="order-content">
          <!-- 订单基本信息 -->
          <div class="info-card">
            <div class="info-row">
              <span class="label">订单编号</span>
              <span class="value mono">#{{ String(order.id).padStart(6, '0') }}</span>
            </div>
            <div class="info-row">
              <span class="label">下单时间</span>
              <span class="value">{{ formatDate(order.created_at) }}</span>
            </div>
            <div class="info-row">
              <span class="label">订单状态</span>
              <el-tag :type="ORDER_STATUS_COLORS[order.status] as any">
                {{ ORDER_STATUS_LABELS[order.status] || order.status }}
              </el-tag>
            </div>
            <div class="info-row total-row">
              <span class="label">订单总价</span>
              <span class="value price">¥{{ order.total_price.toLocaleString() }}</span>
            </div>
          </div>

          <div class="detail-right">
            <!-- 收货地址 -->
            <div class="config-card" v-if="order.shipping_address">
              <h3>收货信息</h3>
              <div class="shipping-info">
                <div class="shipping-row">
                  <span class="shipping-label">收件人：</span>
                  <span>{{ order.shipping_address.recipient_name }}</span>
                  <span class="shipping-label" style="margin-left: 24px;">电话：</span>
                  <span>{{ order.shipping_address.recipient_phone }}</span>
                </div>
                <div class="shipping-row">
                  <span class="shipping-label">地址：</span>
                  <span>{{ order.shipping_address.address_line1 }}
                    {{ order.shipping_address.address_line2 }}
                    ，{{ order.shipping_address.city }}
                    {{ order.shipping_address.state }}
                    {{ order.shipping_address.zip_code }}</span>
                </div>
                <div class="shipping-row" v-if="order.shipping_address.notes">
                  <span class="shipping-label">备注：</span>
                  <span>{{ order.shipping_address.notes }}</span>
                </div>
              </div>
            </div>

            <!-- 配置详情 -->
            <div class="config-card">
              <h3>贝斯配置</h3>
              <div class="config-items" v-if="order.configuration && order.configuration.length > 0">
                <div
                  v-for="(item, idx) in order.configuration"
                  :key="idx"
                  class="config-item"
                >
                  <div class="config-item-header">
                    <span class="config-cat">{{ CATEGORY_LABELS[item.category] || item.category }}</span>
                    <span v-if="item.price > 0" class="config-price">
                      +¥{{ item.price.toLocaleString() }}
                    </span>
                    <span v-else class="config-price included">已包含</span>
                  </div>
                  <div class="config-name">{{ item.name }}</div>
                </div>
              </div>
              <div v-else class="empty-config">
                <p>暂无配置信息</p>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="error-state">
          <el-empty description="订单不存在" />
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, Printer } from '@element-plus/icons-vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { ordersApi } from '@/api/orders'
import { CATEGORY_LABELS, ORDER_STATUS_LABELS, ORDER_STATUS_COLORS } from '@/types'
import { printOrder } from '@/utils/print'
import type { OrderDetail } from '@/types'

const route = useRoute()
const order = ref<OrderDetail | null>(null)
const loading = ref(true)

onMounted(async () => {
  const orderId = Number(route.params.id)
  if (!orderId) return

  try {
    const res = await ordersApi.getOrderDetail(orderId)
    order.value = res.data
  } catch {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
})

function handlePrint() {
  if (order.value) {
    printOrder(order.value)
  }
}

function formatDate(dateStr: string) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>

<style scoped lang="scss">
.order-detail-page {
  min-height: calc(100vh - 200px);
  background: var(--bg-primary);
  padding: 48px 20px 80px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;

  h1 {
    font-size: 1.8rem;
    color: var(--text-primary);
    letter-spacing: 2px;
  }
}

.order-content {
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 24px;
  align-items: start;
}

.info-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 28px 24px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid var(--border-color);

  &:last-child {
    border-bottom: none;
  }

  .label {
    color: var(--text-muted);
    font-size: 0.9rem;
  }

  .value {
    color: var(--text-primary);
    font-size: 0.9rem;

    &.mono {
      font-family: monospace;
      font-weight: 600;
    }

    &.price {
      font-size: 1.4rem;
      font-weight: 700;
      color: var(--accent);
    }
  }

  &.total-row {
    padding-top: 20px;
    margin-top: 8px;
  }
}

.detail-right {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.config-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 28px 24px;

  h3 {
    font-size: 1.1rem;
    color: var(--text-primary);
    margin-bottom: 20px;
    letter-spacing: 1px;
  }
}

.config-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.config-item {
  padding: 14px 16px;
  background: var(--bg-secondary);
  border-radius: 10px;
}

.config-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;

  .config-cat {
    font-size: 0.8rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .config-price {
    font-size: 0.85rem;
    color: var(--accent);
    font-weight: 600;

    &.included {
      color: var(--text-muted);
      font-weight: 400;
    }
  }
}

.config-name {
  color: var(--text-primary);
  font-size: 0.95rem;
}

// Shipping
.shipping-info {
  background: var(--bg-secondary);
  border-radius: 8px;
  padding: 14px 16px;
}

.shipping-row {
  margin-bottom: 6px;
  font-size: 0.9rem;
  color: var(--text-secondary);

  &:last-child {
    margin-bottom: 0;
  }

  .shipping-label {
    color: var(--text-muted);
    font-size: 0.82rem;
  }
}

.empty-config {
  text-align: center;
  color: var(--text-muted);
  padding: 20px;
}

.loading-state,
.error-state {
  padding: 48px 0;
}

@media (max-width: 768px) {
  .order-content {
    grid-template-columns: 1fr;
  }
}
</style>
