import api from './index'
import type {
  AdminOptionListResponse,
  BassOptionWithStatus,
  CategoryItem,
  CreateOptionRequest,
  UpdateOptionRequest,
} from '@/types'

export const adminOptionsApi = {
  /** 获取选项列表（管理员，含分页/筛选） */
  list(params?: {
    page?: number
    page_size?: number
    category?: string
    is_active?: boolean
  }) {
    return api.get<AdminOptionListResponse>('/admin/options', { params })
  },

  /** 新增选项 */
  create(data: CreateOptionRequest) {
    return api.post<BassOptionWithStatus>('/admin/options', data)
  },

  /** 更新选项 */
  update(id: number, data: UpdateOptionRequest) {
    return api.put<BassOptionWithStatus>(`/admin/options/${id}`, data)
  },

  /** 删除选项 */
  delete(id: number) {
    return api.delete(`/admin/options/${id}`)
  },

  /** 上传图片 */
  uploadImage(file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return api.post<{ image_url: string; message: string }>(
      '/admin/options/upload-image',
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    )
  },

  /** 获取所有分类 */
  getCategories() {
    return api.get<CategoryItem[]>('/admin/options/categories')
  },

  /** 重命名分类 */
  renameCategory(oldName: string, newName: string) {
    return api.put<{ old_name: string; new_name: string; updated_count: number }>(
      `/admin/options/categories/${encodeURIComponent(oldName)}/rename`,
      { new_name: newName },
    )
  },
}
