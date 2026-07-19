<template>
  <div class="admin-users-page">
    <div class="page-header">
      <h1 class="admin-page-title">用户管理</h1>
      <div class="search-bar">
        <el-input
          v-model="searchText"
          placeholder="搜索用户名或邮箱"
          :prefix-icon="Search"
          clearable
          @input="onSearch"
          @clear="onSearch"
        />
      </div>
    </div>

    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else>
      <el-table :data="users" style="width: 100%" v-if="users.length > 0">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_admin ? 'warning' : 'info'" size="small">
              {{ row.is_admin ? '管理员' : '用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="注册时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-popconfirm
              title="确定要删除此用户吗？"
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="handleDelete(row.id)"
            >
              <template #reference>
                <el-button
                  type="danger"
                  size="small"
                  text
                  :disabled="row.is_admin"
                >
                  删除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <div v-else class="empty-state">
        <el-empty description="暂无用户数据" />
      </div>

      <div class="pagination-wrap" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="fetchUsers"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { adminApi } from '@/api/admin'
import type { AdminUserItem } from '@/types'

const users = ref<AdminUserItem[]>([])
const loading = ref(true)
const currentPage = ref(1)
const pageSize = 10
const total = ref(0)
const searchText = ref('')
let searchTimer: ReturnType<typeof setTimeout> | null = null

onMounted(() => {
  fetchUsers()
})

async function fetchUsers() {
  loading.value = true
  try {
    const res = await adminApi.getUsers(currentPage.value, pageSize, searchText.value || undefined)
    users.value = res.data.items
    total.value = res.data.total
  } catch {
    // 错误已在拦截器中处理
  } finally {
    loading.value = false
  }
}

function onSearch() {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    fetchUsers()
  }, 300)
}

async function handleDelete(userId: number) {
  try {
    await adminApi.deleteUser(userId)
    ElMessage.success('用户已删除')
    fetchUsers()
  } catch {
    // 错误已在拦截器中处理
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
.admin-users-page {
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

.search-bar {
  width: 280px;
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
</style>
