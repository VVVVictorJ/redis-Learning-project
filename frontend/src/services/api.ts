import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
})

// 请求拦截器 - 添加token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token过期或无效，清除本地存储
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      // 避免在已经在登录页面时重复跳转
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// 认证API
export const authApi = {
  login: async (email: string, password: string) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/login/access-token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  register: async (userData: { email: string; password: string; full_name: string }) => {
    const response = await api.post('/users/', userData)
    return response.data
  },

  getCurrentUser: async () => {
    const response = await api.get('/users/me')
    return response.data
  }
}

// Expense API
export const expenseApi = {
  // 获取当前用户的所有expenses
  getMyExpenses: async (skip = 0, limit = 100) => {
    const response = await api.get(`/expenses/me?skip=${skip}&limit=${limit}`)
    return response.data
  },

  // 创建新expense
  createExpense: async (expense: { description: string; amount: number }) => {
    const response = await api.post('/expenses/', expense)
    return response.data
  },

  // 更新expense
  updateExpense: async (expenseId: number, expense: { description?: string; amount?: number }) => {
    const response = await api.put(`/expenses/${expenseId}`, expense)
    return response.data
  },

  // 删除expense
  deleteExpense: async (expenseId: number) => {
    const response = await api.delete(`/expenses/${expenseId}`)
    return response.data
  }
}

export default api 