// ========== 用户 ==========
export interface UserInfo {
  id: number
  username: string
  email: string
  is_admin: boolean
  created_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  confirm_password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

// ========== 配置选项 ==========
export interface BassOption {
  id: number
  category: string
  name: string
  description: string
  price: number
  image_url?: string | null
}

export interface BassOptionWithStatus extends BassOption {
  is_active: boolean
  created_at: string
}

export interface OptionsByCategory {
  category: string
  options: BassOption[]
}

// Admin
export interface AdminOptionListResponse {
  total: number
  page: number
  page_size: number
  items: BassOptionWithStatus[]
}

export interface CreateOptionRequest {
  category: string
  name: string
  description?: string
  price: number
  image_url?: string | null
  is_active?: boolean
}

export interface UpdateOptionRequest {
  category?: string
  name?: string
  description?: string
  price?: number
  image_url?: string | null
  is_active?: boolean
}

export interface CategoryItem {
  name: string
  count: number
}

// ========== 订单 ==========
export interface OrderItem {
  option_id: number
  category: string
  name: string
  price: number
}

export interface ShippingAddress {
  recipient_name: string
  recipient_phone: string
  address_line1: string
  address_line2: string
  city: string
  state: string
  zip_code: string
  notes: string
}

export interface CreateOrderRequest {
  total_price: number
  configuration: OrderItem[]
  shipping_address?: ShippingAddress
}

export interface OrderDetail {
  id: number
  user_id: number
  username?: string
  total_price: number
  status: string
  configuration: OrderItem[]
  shipping_address?: ShippingAddress | null
  created_at: string
  updated_at: string
}

export interface OrderListItem {
  id: number
  user_id: number
  username?: string
  total_price: number
  status: string
  configuration?: OrderItem[]
  shipping_address?: ShippingAddress | null
  created_at: string
  updated_at: string
}

export interface OrderListResponse {
  total: number
  page: number
  page_size: number
  items: OrderListItem[]
}

// ========== 管理员 ==========
export interface DashboardStats {
  total_users: number
  total_orders: number
  pending_orders: number
  completed_orders: number
  total_options: number
}

export interface AdminUserItem {
  id: number
  username: string
  email: string
  is_admin: boolean
  created_at: string
}

export interface AdminUserListResponse {
  total: number
  page: number
  page_size: number
  items: AdminUserItem[]
}

// ========== 分类中文映射 ==========
export const CATEGORY_LABELS: Record<string, string> = {
  body: '琴体木材',
  neck: '琴颈木材',
  fingerboard: '指板材质',
  pickup: '拾音器',
  bridge: '琴桥',
  finish: '颜色/漆面',
  strings: '弦数',
  handedness: '左右手',
}

// ========== 订单状态中文映射 ==========
export const ORDER_STATUS_LABELS: Record<string, string> = {
  pending: '待确认',
  confirmed: '已确认',
  production: '制作中',
  completed: '已完成',
  cancelled: '已取消',
}

export const ORDER_STATUS_COLORS: Record<string, string> = {
  pending: 'warning',
  confirmed: 'primary',
  production: 'info',
  completed: 'success',
  cancelled: 'danger',
}
