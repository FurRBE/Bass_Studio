import api from './index'
import type {
  AdminUserListResponse,
  DashboardStats,
  OrderDetail,
  OrderListResponse,
} from '@/types'

export const adminApi = {
  getDashboard() {
    return api.get<DashboardStats>('/admin/dashboard')
  },

  getUsers(page = 1, pageSize = 10, search?: string) {
    return api.get<AdminUserListResponse>('/admin/users', {
      params: { page, page_size: pageSize, search },
    })
  },

  deleteUser(userId: number) {
    return api.delete(`/admin/users/${userId}`)
  },

  getOrders(page = 1, pageSize = 10, status?: string) {
    return api.get<OrderListResponse>('/admin/orders', {
      params: { page, page_size: pageSize, status },
    })
  },

  getOrderDetail(orderId: number) {
    return api.get<OrderDetail>(`/admin/orders/${orderId}`)
  },

  updateOrderStatus(orderId: number, status: string) {
    return api.put(`/admin/orders/${orderId}/status`, { status })
  },
}
