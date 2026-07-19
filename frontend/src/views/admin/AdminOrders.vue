<template>
  <div class="admin-orders-page">
    <div class="page-header">
      <h1 class="admin-page-title">订单管理</h1>
      <div class="filter-bar">
        <el-select
          v-model="statusFilter"
          placeholder="全部状态"
          clearable
          @change="onFilterChange"
        >
          <el-option label="全部" value="" />
          <el-option
            v-for="(label, key) in ORDER_STATUS_LABELS"
            :key="key"
            :label="label"
            :value="key"
          />
        </el-select>
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else>
      <el-table :data="orders" style="width: 100%" v-if="orders.length > 0">
        <el-table-column label="订单编号" width="140">
          <template #default="{ row }">
            <span class="order-id">#{{ String(row.id).padStart(6, '0') }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户" width="120" />
        <el-table-column label="总价" width="120">
          <template #default="{ row }">
            <span class="order-price">¥{{ row.total_price.toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-select
              :model-value="row.status"
              size="small"
              @change="(val: string) => handleStatusChange(row.id, val)"
            >
              <el-option
                v-for="(label, key) in ORDER_STATUS_LABELS"
                :key="key"
                :label="label"
                :value="key"
              />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="下单时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button type="primary" size="small" text @click="showDetail(row)">
              详情
            </el-button>
            <el-button size="small" text @click="handlePrint(row)">
              <el-icon><Printer /></el-icon>
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-else class="empty-state">
        <el-empty description="暂无订单数据" />
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

    <!-- 订单详情弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      title="订单详情"
      width="700px"
      destroy-on-close
    >
      <div v-if="detailOrder" class="order-detail">
        <div class="detail-header">
          <div>
            <span class="detail-label">订单编号</span>
            <span class="detail-value mono">#{{ String(detailOrder.id).padStart(6, '0') }}</span>
          </div>
          <div class="detail-header-actions">
            <el-button size="small" @click="handlePrintDetail">
              <el-icon><Printer /></el-icon> 打印
            </el-button>
            <el-tag :type="ORDER_STATUS_COLORS[detailOrder.status] as any">
              {{ ORDER_STATUS_LABELS[detailOrder.status] || detailOrder.status }}
            </el-tag>
          </div>
        </div>
        <div class="detail-info">
          <div class="detail-row">
            <span>用户：{{ detailOrder.username }}</span>
            <span>总价：¥{{ detailOrder.total_price.toLocaleString() }}</span>
          </div>
          <div class="detail-row">
            <span>创建时间：{{ formatDate(detailOrder.created_at) }}</span>
            <span>更新时间：{{ formatDate(detailOrder.updated_at) }}</span>
          </div>
        </div>

        <!-- 收货地址 -->
        <div class="shipping-section" v-if="detailOrder.shipping_address">
          <el-divider style="border-color: #2a2a2a;" />
          <h4>收货信息</h4>
          <div class="shipping-info">
            <div class="shipping-row">
              <span class="shipping-label">收件人：</span>
              <span>{{ detailOrder.shipping_address.recipient_name }}</span>
              <span class="shipping-label" style="margin-left: 24px;">电话：</span>
              <span>{{ detailOrder.shipping_address.recipient_phone }}</span>
            </div>
            <div class="shipping-row">
              <span class="shipping-label">地址：</span>
              <span>{{ detailOrder.shipping_address.address_line1 }}
                {{ detailOrder.shipping_address.address_line2 }}
                ，{{ detailOrder.shipping_address.city }}
                {{ detailOrder.shipping_address.state }}
                {{ detailOrder.shipping_address.zip_code }}</span>
            </div>
            <div class="shipping-row" v-if="detailOrder.shipping_address.notes">
              <span class="shipping-label">备注：</span>
              <span>{{ detailOrder.shipping_address.notes }}</span>
            </div>
          </div>
        </div>

        <el-divider style="border-color: #2a2a2a;" />
        <h4>配置详情</h4>
        <div class="config-list" v-if="detailOrder.configuration && detailOrder.configuration.length > 0">
          <div
            v-for="(item, idx) in detailOrder.configuration"
            :key="idx"
            class="config-item"
          >
            <span class="config-cat">{{ CATEGORY_LABELS[item.category] || item.category }}</span>
            <span class="config-name">{{ item.name }}</span>
            <span v-if="item.price > 0" class="config-price">+¥{{ item.price.toLocaleString() }}</span>
            <span v-else class="config-price included">已包含</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Printer } from '@element-plus/icons-vue'
import { adminApi } from '@/api/admin'
import { CATEGORY_LABELS, ORDER_STATUS_LABELS, ORDER_STATUS_COLORS } from '@/types'
import { printOrder } from '@/utils/print'
import type { OrderListItem, OrderDetail } from '@/types'

const orders = ref<OrderListItem[]>([])
const loading = ref(true)
const currentPage = ref(1)
const pageSize = 10
const total = ref(0)
const statusFilter = ref('')
const dialogVisible = ref(false)
const detailOrder = ref<OrderDetail | null>(null)

onMounted(() => {
  fetchOrders()
})

async function fetchOrders() {
  loading.value = true
  try {
    const res = await adminApi.getOrders(
      currentPage.value,
      pageSize,
      statusFilter.value || undefined,
    )
    orders.value = res.data.items
    total.value = res.data.total
  } catch {
  } finally {
    loading.value = false
  }
}

function onFilterChange() {
  currentPage.value = 1
  fetchOrders()
}

async function handleStatusChange(orderId: number, newStatus: string) {
  try {
    await adminApi.updateOrderStatus(orderId, newStatus)
    ElMessage.success('订单状态已更新')
    fetchOrders()
  } catch {
  }
}

async function showDetail(row: OrderListItem) {
  try {
    const res = await adminApi.getOrderDetail(row.id)
    detailOrder.value = res.data
    dialogVisible.value = true
  } catch {
  }
}

async function handlePrint(row: OrderListItem) {
  try {
    const res = await adminApi.getOrderDetail(row.id)
    printOrder(res.data)
  } catch {
  }
}

function handlePrintDetail() {
  if (detailOrder.value) {
    printOrder(detailOrder.value)
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
.admin-orders-page {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.admin-page-title {
  font-size: 1.6rem;
  color: var(--text-primary);
  letter-spacing: 2px;
  margin: 0;
}

.filter-bar {
  width: 160px;
}

.order-id {
  font-family: monospace;
  font-weight: 600;
}

.order-price {
  font-weight: 600;
  color: var(--accent);
}

.pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.loading-state,
.empty-state {
  padding: 40px 0;
}

// Dialog styles
.order-detail {
  color: var(--text-primary);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;

  .detail-label {
    color: var(--text-muted);
    margin-right: 8px;
  }

  .detail-value {
    font-family: monospace;
    font-weight: 600;

    &.mono {
      font-family: monospace;
    }
  }

  .detail-header-actions {
    display: flex;
    align-items: center;
    gap: 12px;
  }
}

.detail-info {
  .detail-row {
    display: flex;
    gap: 32px;
    margin-bottom: 8px;
    color: var(--text-muted);
    font-size: 0.9rem;
  }
}

// Shipping section
.shipping-section {
  h4 {
    margin-bottom: 12px;
    color: var(--text-primary);
  }
}

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

h4 {
  margin-bottom: 12px;
  color: var(--text-primary);
}

.config-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.config-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  background: var(--bg-secondary);
  border-radius: 8px;
  font-size: 0.9rem;

  .config-cat {
    color: var(--text-muted);
    font-size: 0.8rem;
    min-width: 80px;
  }

  .config-name {
    color: var(--text-primary);
    flex: 1;
  }

  .config-price {
    color: var(--accent);
    font-weight: 600;

    &.included {
      color: var(--text-muted);
      font-weight: 400;
    }
  }
}
</style>
