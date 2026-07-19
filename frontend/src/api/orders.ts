import api from './index'
import type { CreateOrderRequest, OrderDetail, OrderListResponse } from '@/types'

export const ordersApi = {
  create(data: CreateOrderRequest) {
    return api.post<{ message: string; order_id: number }>('/orders', data)
  },

  getMyOrders(page = 1, pageSize = 10) {
    return api.get<OrderListResponse>('/orders/me', {
      params: { page, page_size: pageSize },
    })
  },

  getOrderDetail(orderId: number) {
    return api.get<OrderDetail>(`/orders/${orderId}`)
  },
}
