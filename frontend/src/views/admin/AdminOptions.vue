<template>
  <div class="admin-options-page">
    <div class="page-header">
      <h1 class="admin-page-title">配置管理</h1>
      <div class="header-actions">
        <el-select
          v-model="categoryFilter"
          placeholder="全部分类"
          clearable
          @change="onFilterChange"
          style="width: 180px; margin-right: 12px;"
        >
          <el-option label="全部分类" value="" />
          <el-option
            v-for="cat in categories"
            :key="cat.name"
            :label="`${CATEGORY_LABELS[cat.name] || cat.name} (${cat.count})`"
            :value="cat.name"
          />
        </el-select>
        <el-button type="primary" @click="openCreateModal">
          <el-icon><Plus /></el-icon>
          新增选项
        </el-button>
      </div>
    </div>

    <!-- Categories quick management -->
    <div class="category-chips" v-if="categories.length > 0">
      <span class="chips-label">分类：</span>
      <el-tag
        v-for="cat in categories"
        :key="cat.name"
        closable
        :disable-transitions="false"
        class="cat-chip"
        @close="handleDeleteCategory(cat.name)"
        @click="handleRenameCategory(cat.name)"
        :title="'点击重命名，点击 × 删除（需先清空该分类下的选项）'"
      >
        {{ CATEGORY_LABELS[cat.name] || cat.name }} ({{ cat.count }})
      </el-tag>
    </div>

    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="6" animated />
    </div>

    <div v-else>
      <el-table :data="options" style="width: 100%" v-if="options.length > 0" stripe>
        <el-table-column label="ID" width="60" prop="id" />
        <el-table-column label="图片" width="90">
          <template #default="{ row }">
            <div class="img-thumb" v-if="row.image_url">
              <img :src="row.image_url" :alt="row.name" />
            </div>
            <div class="img-thumb placeholder" v-else>
              <el-icon><Picture /></el-icon>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="分类" width="120">
          <template #default="{ row }">
            <el-tag size="small" type="info">
              {{ CATEGORY_LABELS[row.category] || row.category }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="description" label="简介" min-width="200" show-overflow-tooltip />
        <el-table-column label="价格" width="110" align="right">
          <template #default="{ row }">
            <span v-if="row.price > 0" class="price-cell">¥{{ row.price.toLocaleString() }}</span>
            <span v-else class="price-cell free">已包含</span>
          </template>
        </el-table-column>
        <el-table-column label="启用" width="70" align="center">
          <template #default="{ row }">
            <el-switch
              :model-value="row.is_active"
              @change="(val: boolean) => handleToggleActive(row.id, val)"
              size="small"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" text @click="openEditModal(row)">
              编辑
            </el-button>
            <el-popconfirm
              title="确定要删除此选项吗？"
              @confirm="handleDelete(row.id)"
            >
              <template #reference>
                <el-button type="danger" size="small" text>删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <div v-else class="empty-state">
        <el-empty description="暂无配置选项">
          <el-button type="primary" @click="openCreateModal">新增选项</el-button>
        </el-empty>
      </div>

      <div class="pagination-wrap" v-if="total > pageSize">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="fetchOptions"
        />
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? '编辑选项' : '新增选项'"
      width="560px"
      destroy-on-close
      @closed="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="80px"
        label-position="top"
      >
        <el-form-item label="所属分类" prop="category" required>
          <el-select
            v-model="form.category"
            placeholder="选择或输入新分类"
            filterable
            allow-create
            default-first-option
            style="width: 100%;"
          >
            <el-option
              v-for="cat in categories"
              :key="cat.name"
              :label="CATEGORY_LABELS[cat.name] || cat.name"
              :value="cat.name"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="选项名称" prop="name" required>
          <el-input v-model="form.name" placeholder="如：Mahogany / 桃花心木" maxlength="100" />
        </el-form-item>

        <el-form-item label="简介描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="2"
            placeholder="简短介绍该选项的特点"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="价格 (¥)" prop="price">
          <el-input-number
            v-model="form.price"
            :min="0"
            :step="100"
            style="width: 100%;"
          />
        </el-form-item>

        <el-form-item label="是否启用">
          <el-switch v-model="form.is_active" />
        </el-form-item>

        <el-form-item label="示例图片">
          <div class="upload-area">
            <div class="image-preview" v-if="form.image_url">
              <img :src="form.image_url" alt="Preview" />
              <el-button
                type="danger"
                size="small"
                circle
                class="remove-img-btn"
                @click="form.image_url = null"
              >
                <el-icon><Close /></el-icon>
              </el-button>
            </div>
            <el-upload
              v-else
              class="image-uploader"
              :show-file-list="false"
              :before-upload="beforeImageUpload"
              :http-request="handleImageUpload"
              accept="image/jpeg,image/png,image/gif,image/webp,image/svg+xml"
            >
              <div class="upload-trigger">
                <el-icon class="upload-icon"><Plus /></el-icon>
                <span>上传图片</span>
              </div>
            </el-upload>
            <p class="upload-hint">支持 jpg/png/gif/webp/svg，不超过 10MB</p>
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ isEditing ? '保存修改' : '确认新增' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Rename Category Dialog -->
    <el-dialog
      v-model="renameDialogVisible"
      title="重命名分类"
      width="420px"
    >
      <el-form label-width="80px">
        <el-form-item label="原名">
          <span class="rename-old-name">{{ renamingCategory }}</span>
        </el-form-item>
        <el-form-item label="新名称" required>
          <el-input
            v-model="renameNewName"
            placeholder="输入新的分类名称"
            maxlength="50"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="renameDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleConfirmRename">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules, type UploadRequestOptions } from 'element-plus'
import { Plus, Picture, Close } from '@element-plus/icons-vue'
import { adminOptionsApi } from '@/api/adminOptions'
import { CATEGORY_LABELS } from '@/types'
import type { BassOptionWithStatus, CategoryItem } from '@/types'

// ---------- Data ----------
const options = ref<BassOptionWithStatus[]>([])
const categories = ref<CategoryItem[]>([])
const loading = ref(true)
const currentPage = ref(1)
const pageSize = 20
const total = ref(0)
const categoryFilter = ref('')

const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref<number | null>(null)
const submitting = ref(false)
const formRef = ref<FormInstance>()

const form = reactive({
  category: '',
  name: '',
  description: '',
  price: 0,
  image_url: null as string | null,
  is_active: true,
})

const formRules: FormRules = {
  category: [{ required: true, message: '请选择或输入分类', trigger: 'blur' }],
  name: [{ required: true, message: '请输入选项名称', trigger: 'blur' }],
}

// Category rename
const renameDialogVisible = ref(false)
const renamingCategory = ref('')
const renameNewName = ref('')

// ---------- Lifecycle ----------
onMounted(() => {
  fetchOptions()
  fetchCategories()
})

// ---------- Methods ----------
async function fetchOptions() {
  loading.value = true
  try {
    const res = await adminOptionsApi.list({
      page: currentPage.value,
      page_size: pageSize,
      category: categoryFilter.value || undefined,
    })
    options.value = res.data.items
    total.value = res.data.total
  } catch { /* handled by interceptor */ } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    const res = await adminOptionsApi.getCategories()
    categories.value = res.data
  } catch { /* handled */ }
}

function onFilterChange() {
  currentPage.value = 1
  fetchOptions()
}

function openCreateModal() {
  isEditing.value = false
  editingId.value = null
  dialogVisible.value = true
}

function openEditModal(row: BassOptionWithStatus) {
  isEditing.value = true
  editingId.value = row.id
  form.category = row.category
  form.name = row.name
  form.description = row.description || ''
  form.price = row.price
  form.image_url = row.image_url || null
  form.is_active = row.is_active
  dialogVisible.value = true
}

function resetForm() {
  form.category = ''
  form.name = ''
  form.description = ''
  form.price = 0
  form.image_url = null
  form.is_active = true
  formRef.value?.resetFields()
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    submitting.value = true
    try {
      const data = {
        category: form.category,
        name: form.name,
        description: form.description || '',
        price: form.price,
        image_url: form.image_url,
        is_active: form.is_active,
      }

      if (isEditing.value && editingId.value) {
        await adminOptionsApi.update(editingId.value, data)
        ElMessage.success('选项已更新')
      } else {
        await adminOptionsApi.create(data)
        ElMessage.success('选项已创建')
      }

      dialogVisible.value = false
      fetchOptions()
      fetchCategories()
    } catch {
      // handled by interceptor
    } finally {
      submitting.value = false
    }
  })
}

async function handleDelete(id: number) {
  try {
    await adminOptionsApi.delete(id)
    ElMessage.success('选项已删除')
    fetchOptions()
    fetchCategories()
  } catch { /* handled */ }
}

async function handleToggleActive(id: number, isActive: boolean) {
  try {
    await adminOptionsApi.update(id, { is_active: isActive })
    ElMessage.success(isActive ? '已启用' : '已停用')
    fetchOptions()
  } catch { /* handled */ }
}

// Image upload
function beforeImageUpload(file: File) {
  const isImage = /^image\/(jpeg|png|gif|webp|svg\+xml)$/.test(file.type)
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('仅支持 jpg/png/gif/webp/svg 格式的图片')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB')
    return false
  }
  return true
}

async function handleImageUpload(options: UploadRequestOptions) {
  try {
    const res = await adminOptionsApi.uploadImage(options.file as File)
    form.image_url = res.data.image_url
    ElMessage.success('图片上传成功')
  } catch {
    // handled by interceptor
  }
}

// Category management
async function handleDeleteCategory(catName: string) {
  try {
    await ElMessageBox.confirm(
      `确定要删除分类「${CATEGORY_LABELS[catName] || catName}」吗？\n\n该分类下的所有选项也将被删除。`,
      '删除分类',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
      },
    )
    // Delete all options in this category
    const catOptions = options.value.filter(o => o.category === catName)
    for (const opt of catOptions) {
      await adminOptionsApi.delete(opt.id)
    }
    ElMessage.success(`分类已删除`)
    fetchOptions()
    fetchCategories()
  } catch {
    // cancelled or error
  }
}

function handleRenameCategory(catName: string) {
  renamingCategory.value = catName
  renameNewName.value = ''
  renameDialogVisible.value = true
}

async function handleConfirmRename() {
  if (!renameNewName.value.trim()) {
    ElMessage.warning('请输入新名称')
    return
  }
  try {
    await adminOptionsApi.renameCategory(renamingCategory.value, renameNewName.value.trim())
    ElMessage.success('分类已重命名')
    renameDialogVisible.value = false
    fetchOptions()
    fetchCategories()
  } catch { /* handled */ }
}
</script>

<style scoped lang="scss">
.admin-options-page {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.admin-page-title {
  font-size: 1.6rem;
  color: var(--text-primary);
  letter-spacing: 2px;
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
}

// Category chips
.category-chips {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;

  .chips-label {
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-right: 4px;
  }

  .cat-chip {
    cursor: pointer;
  }
}

// Image
.img-thumb {
  width: 60px;
  height: 45px;
  border-radius: 6px;
  overflow: hidden;
  background: var(--bg-secondary);
  display: flex;
  align-items: center;
  justify-content: center;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  &.placeholder {
    color: var(--text-muted);
    font-size: 1.2rem;
  }
}

.price-cell {
  font-weight: 600;
  color: var(--accent);

  &.free {
    color: var(--text-muted);
    font-weight: 400;
  }
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

// Upload
.upload-area {
  .image-preview {
    position: relative;
    display: inline-block;

    img {
      max-width: 200px;
      max-height: 150px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
    }

    .remove-img-btn {
      position: absolute;
      top: -8px;
      right: -8px;
    }
  }

  .image-uploader {
    .upload-trigger {
      width: 140px;
      height: 100px;
      border: 2px dashed var(--border-color);
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: border-color 0.2s;
      color: var(--text-muted);

      &:hover {
        border-color: var(--accent);
        color: var(--accent);
      }

      .upload-icon {
        font-size: 1.5rem;
        margin-bottom: 4px;
      }

      span {
        font-size: 0.8rem;
      }
    }
  }

  .upload-hint {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: 6px;
  }
}

.rename-old-name {
  font-weight: 600;
  color: var(--accent);
  font-size: 1rem;
}
</style>
