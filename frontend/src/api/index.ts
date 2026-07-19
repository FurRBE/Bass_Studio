import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器：自动携带 Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：统一错误处理
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status
    const detail = error.response?.data?.detail

    switch (status) {
      case 401:
        ElMessage.error(detail || '请先登录')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        break
      case 403:
        ElMessage.error(detail || '没有权限')
        break
      case 404:
        ElMessage.error(detail || '资源不存在')
        break
      case 409:
        ElMessage.error(detail || '资源冲突')
        break
      case 422:
        ElMessage.error(detail || '请求参数错误')
        break
      case 500:
        ElMessage.error(detail || '服务器错误')
        break
      default:
        ElMessage.error(detail || '请求失败')
    }

    return Promise.reject(error)
  }
)

export default api
