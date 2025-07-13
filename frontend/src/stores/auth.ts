import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import http from '@/utils/http'
import type { User, UserCreate } from '@/schemas/user'
import type { Token } from '@/schemas/token'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const currentUser = ref<User | null>(null)

  const isLoggedIn = computed(() => !!token.value && !!currentUser.value)

  function setToken(accessToken: string) {
    token.value = accessToken
    localStorage.setItem('access_token', accessToken)
    http.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`
  }

  function clearToken() {
    token.value = null
    currentUser.value = null
    localStorage.removeItem('access_token')
    delete http.defaults.headers.common['Authorization']
  }

  async function login(formData: FormData) {
    const response = await http.post<Token>('/login/access-token', formData)
    setToken(response.data.access_token)
    await fetchCurrentUser()
    await router.push('/dashboard')
  }

  async function register(userData: UserCreate) {
    await http.post<User>('/users/', userData)
    // Optional: automatically log in after registration
    const formData = new FormData()
    formData.append('username', userData.email)
    formData.append('password', userData.password)
    await login(formData)
  }

  async function fetchCurrentUser() {
    if (!token.value) {
      return
    }
    try {
      const response = await http.get<User>('/users/me')
      currentUser.value = response.data
    } catch (error) {
      console.error('Failed to fetch user, logging out.', error)
      logout()
    }
  }

  function logout() {
    clearToken()
    router.push('/login')
  }

  // Set token on initial load if it exists
  if (token.value) {
    http.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  return {
    token,
    currentUser,
    isLoggedIn,
    login,
    register,
    logout,
    fetchCurrentUser,
  }
}) 