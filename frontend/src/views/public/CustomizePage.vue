<template>
  <DefaultLayout>
    <div class="customize-page">
      <div class="container">
        <div class="customize-header">
          <h1>定制你的贝斯</h1>
          <p>从基础配置开始，打造属于你的专属乐器</p>
        </div>

        <div class="customize-layout">
          <!-- 左侧：配置选项 -->
          <div class="options-panel">
            <div
              v-for="cat in categories"
              :key="cat.category"
              class="category-section"
            >
              <div class="category-header">
                <h3>{{ CATEGORY_LABELS[cat.category] || cat.category }}</h3>
                <span v-if="store.selections[cat.category]" class="selected-badge">
                  已选择: {{ store.selections[cat.category].name.split(' / ')[0] }}
                </span>
              </div>
              <div class="options-grid">
                <div
                  v-for="opt in cat.options"
                  :key="opt.id"
                  class="option-card"
                  :class="{
                    selected: store.selections[cat.category]?.id === opt.id,
                  }"
                  @click="store.selectOption(cat.category, opt)"
                >
                  <div class="option-image" v-if="opt.image_url">
                    <img :src="opt.image_url" :alt="opt.name" />
                  </div>
                  <div class="option-name">{{ opt.name }}</div>
                  <div class="option-desc" v-if="opt.description">{{ opt.description }}</div>
                  <div class="option-price">
                    <span v-if="opt.price > 0">+¥{{ opt.price.toLocaleString() }}</span>
                    <span v-else class="included">已包含</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 右侧：配置摘要 -->
          <div class="summary-panel">
            <div class="summary-card">
              <h3>你的配置</h3>
              <div class="summary-base">
                <span>基础价格</span>
                <span class="price">¥{{ store.basePrice.toLocaleString() }}</span>
              </div>

              <el-divider style="border-color: #2a2a2a;" />

              <div class="summary-items" v-if="store.selectedCount > 0">
                <div
                  v-for="(opt, cat) in store.selections"
                  :key="cat"
                  class="summary-item"
                >
                  <div class="summary-item-info">
                    <span class="summary-item-cat">{{ CATEGORY_LABELS[cat] || cat }}</span>
                    <span class="summary-item-name">{{ opt.name }}</span>
                  </div>
                  <span v-if="opt.price > 0" class="summary-item-price">
                    +¥{{ opt.price.toLocaleString() }}
                  </span>
                  <span v-else class="summary-item-price included">-</span>
                </div>
              </div>
              <div v-else class="summary-empty">
                <p>请在左侧选择配置选项</p>
              </div>

              <el-divider style="border-color: #2a2a2a;" />

              <div class="summary-total">
                <span>总价</span>
                <span class="total-price">¥{{ store.totalPrice.toLocaleString() }}</span>
              </div>

              <el-button
                type="primary"
                size="large"
                class="submit-order-btn"
                :disabled="store.selectedCount === 0"
                :loading="submittingOrder"
                @click="handleSubmitOrder"
              >
                提交订单
              </el-button>

              <el-button
                v-if="store.selectedCount > 0"
                size="small"
                class="reset-btn"
                text
                @click="store.resetAll()"
              >
                清空所有选择
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 收货地址弹窗 -->
    <el-dialog
      v-model="showAddressDialog"
      title="填写收货信息"
      width="520px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        ref="addressFormRef"
        :model="addressForm"
        :rules="addressRules"
        label-width="80px"
        label-position="top"
      >
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="收件人姓名" prop="recipient_name">
              <el-input v-model="addressForm.recipient_name" placeholder="请输入收件人姓名" maxlength="100" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="recipient_phone">
              <el-input v-model="addressForm.recipient_phone" placeholder="请输入联系电话" maxlength="30" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="详细地址" prop="address_line1">
          <el-input v-model="addressForm.address_line1" placeholder="街道、门牌号" maxlength="200" />
        </el-form-item>

        <el-form-item label="地址补充" prop="address_line2">
          <el-input v-model="addressForm.address_line2" placeholder="公寓、楼层等（选填）" maxlength="200" />
        </el-form-item>

        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="城市" prop="city">
              <el-input v-model="addressForm.city" placeholder="城市" maxlength="100" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="省份/州" prop="state">
              <el-input v-model="addressForm.state" placeholder="省份或州" maxlength="100" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="邮编" prop="zip_code">
              <el-input v-model="addressForm.zip_code" placeholder="邮政编码" maxlength="20" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注">
          <el-input
            v-model="addressForm.notes"
            type="textarea"
            :rows="2"
            placeholder="如有特殊需求请在此说明（选填）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showAddressDialog = false">返回修改</el-button>
        <el-button type="primary" :loading="submittingOrder" @click="confirmOrder">
          确认下单
        </el-button>
      </template>
    </el-dialog>
  </DefaultLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import { optionsApi } from '@/api/options'
import { ordersApi } from '@/api/orders'
import { useAuthStore } from '@/stores/auth'
import { useCustomizeStore } from '@/stores/customize'
import { CATEGORY_LABELS } from '@/types'
import type { OptionsByCategory } from '@/types'

const router = useRouter()
const authStore = useAuthStore()
const store = useCustomizeStore()
const categories = ref<OptionsByCategory[]>([])
const submittingOrder = ref(false)

const showAddressDialog = ref(false)
const addressFormRef = ref<FormInstance>()
const addressForm = reactive({
  recipient_name: '',
  recipient_phone: '',
  address_line1: '',
  address_line2: '',
  city: '',
  state: '',
  zip_code: '',
  notes: '',
})

const addressRules: FormRules = {
  recipient_name: [{ required: true, message: '请输入收件人姓名', trigger: 'blur' }],
  recipient_phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  address_line1: [{ required: true, message: '请输入详细地址', trigger: 'blur' }],
  city: [{ required: true, message: '请输入城市', trigger: 'blur' }],
  zip_code: [{ required: true, message: '请输入邮编', trigger: 'blur' }],
}

onMounted(async () => {
  try {
    const res = await optionsApi.getAll()
    categories.value = res.data
  } catch {
    // 错误已在拦截器中处理
  }
})

async function handleSubmitOrder() {
  if (!authStore.isLoggedIn) {
    ElMessage.warning('请先登录后再提交订单')
    router.push({ name: 'login', query: { redirect: '/customize' } })
    return
  }

  showAddressDialog.value = true
}

async function confirmOrder() {
  if (!addressFormRef.value) return
  await addressFormRef.value.validate(async (valid) => {
    if (!valid) return
    submittingOrder.value = true
    try {
      const res = await ordersApi.create({
        total_price: store.totalPrice,
        configuration: store.configuration,
        shipping_address: {
          recipient_name: addressForm.recipient_name,
          recipient_phone: addressForm.recipient_phone,
          address_line1: addressForm.address_line1,
          address_line2: addressForm.address_line2,
          city: addressForm.city,
          state: addressForm.state,
          zip_code: addressForm.zip_code,
          notes: addressForm.notes,
        },
      })

      ElMessage.success('订单提交成功！')
      store.resetAll()
      showAddressDialog.value = false
      router.push(`/orders/${res.data.order_id}`)
    } catch {
      // 错误已在拦截器中处理
    } finally {
      submittingOrder.value = false
    }
  })
}
</script>

<style scoped lang="scss">
.customize-page {
  min-height: 100vh;
  background: var(--bg-primary);
  padding-bottom: 80px;
}

.customize-header {
  text-align: center;
  padding: 48px 0 40px;

  h1 {
    font-size: 2rem;
    color: var(--text-primary);
    letter-spacing: 2px;
    margin-bottom: 8px;
  }

  p {
    color: var(--text-muted);
  }
}

.customize-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 32px;
  align-items: start;
}

// Options
.category-section {
  margin-bottom: 32px;
}

.category-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);

  h3 {
    font-size: 1.1rem;
    color: var(--text-primary);
    letter-spacing: 1px;
  }

  .selected-badge {
    font-size: 0.8rem;
    color: var(--accent);
    background: rgba(200, 164, 92, 0.1);
    padding: 4px 12px;
    border-radius: 20px;
  }
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}

.option-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--accent);
    background: var(--bg-card-hover);
  }

  &.selected {
    border-color: var(--accent);
    background: rgba(200, 164, 92, 0.08);
    box-shadow: 0 0 0 1px var(--accent);
  }

  .option-image {
    width: 100%;
    height: 120px;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 10px;
    background: var(--bg-secondary);

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }

  .option-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
  }

  .option-desc {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin-bottom: 8px;
    line-height: 1.4;
  }

  .option-price {
    font-size: 0.85rem;
    color: var(--accent);
    font-weight: 600;

    .included {
      color: var(--text-muted);
      font-weight: 400;
    }
  }
}

// Summary
.summary-panel {
  position: sticky;
  top: 84px;
}

.summary-card {
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

.summary-base {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-secondary);
  font-size: 0.9rem;

  .price {
    color: var(--text-primary);
    font-weight: 600;
  }
}

.summary-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;

  .summary-item-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .summary-item-cat {
    color: var(--text-muted);
    font-size: 0.75rem;
  }

  .summary-item-name {
    color: var(--text-secondary);
  }

  .summary-item-price {
    color: var(--accent);
    font-weight: 600;
    white-space: nowrap;

    &.included {
      color: var(--text-muted);
      font-weight: 400;
    }
  }
}

.summary-empty {
  text-align: center;
  padding: 20px 0;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;

  span:first-child {
    font-size: 0.95rem;
    color: var(--text-secondary);
  }

  .total-price {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent);
  }
}

.submit-order-btn {
  width: 100%;
  margin-bottom: 8px;
}

.reset-btn {
  width: 100%;
  color: var(--text-muted) !important;
}

@media (max-width: 1024px) {
  .customize-layout {
    grid-template-columns: 1fr;
  }

  .summary-panel {
    position: static;
  }
}

@media (max-width: 640px) {
  .options-grid {
    grid-template-columns: 1fr;
  }
}
</style>
