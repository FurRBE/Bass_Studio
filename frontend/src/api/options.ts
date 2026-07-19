import api from './index'
import type { OptionsByCategory } from '@/types'

export const optionsApi = {
  getAll() {
    return api.get<OptionsByCategory[]>('/options')
  },

  getByCategory(category: string) {
    return api.get<OptionsByCategory>(`/options/${category}`)
  },
}
