import api from './index'
import type { LoginRequest, RegisterRequest, TokenResponse, UserInfo } from '@/types'

export const authApi = {
  register(data: RegisterRequest) {
    return api.post<{ message: string; user_id: number }>('/auth/register', data)
  },

  login(data: LoginRequest) {
    return api.post<TokenResponse>('/auth/login', data)
  },

  getMe() {
    return api.get<UserInfo>('/auth/me')
  },
}
