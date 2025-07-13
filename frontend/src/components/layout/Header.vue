<template>
  <header class="header">
    <div class="header-left">
      <!-- 移动端菜单按钮 -->
      <button class="mobile-menu-btn" @click="toggleMobileMenu">
        <svg viewBox="0 0 24 24" width="24" height="24">
          <path fill="currentColor" d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
        </svg>
      </button>
      
      <!-- 面包屑导航 -->
      <nav class="breadcrumb">
        <ol class="breadcrumb-list">
          <li class="breadcrumb-item">
            <router-link to="/" class="breadcrumb-link">CatExpense</router-link>
          </li>
          <li class="breadcrumb-separator">
            <svg viewBox="0 0 24 24" width="16" height="16">
              <path fill="currentColor" d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
            </svg>
          </li>
          <li class="breadcrumb-item">
            <span class="breadcrumb-current">{{ currentPageName }}</span>
          </li>
        </ol>
      </nav>
    </div>

    <div class="header-right">
      <!-- 通知按钮 -->
      <button class="header-btn notification-btn" @click="showNotifications">
        <svg viewBox="0 0 24 24" width="20" height="20">
          <path fill="currentColor" d="M12 22c1.1 0 2-.9 2-2h-4c0 1.1.9 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z"/>
        </svg>
        <span class="notification-badge" v-if="notificationCount > 0">{{ notificationCount }}</span>
      </button>

      <!-- 主题切换按钮 -->
      <button class="header-btn theme-btn" @click="toggleTheme">
        <svg v-if="isDarkMode" viewBox="0 0 24 24" width="20" height="20">
          <path fill="currentColor" d="M12 9c1.65 0 3 1.35 3 3s-1.35 3-3 3-3-1.35-3-3 1.35-3 3-3m0-2c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zM2 13h2c.55 0 1-.45 1-1s-.45-1-1-1H2c-.55 0-1 .45-1 1s.45 1 1 1zm18 0h2c.55 0 1-.45 1-1s-.45-1-1-1h-2c-.55 0-1 .45-1 1s.45 1 1 1zM11 2v2c0 .55.45 1 1 1s1-.45 1-1V2c0-.55-.45-1-1-1s-1 .45-1 1zm0 18v2c0 .55.45 1 1 1s1-.45 1-1v-2c0-.55-.45-1-1-1s-1 .45-1 1zM5.99 4.58c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0s.39-1.03 0-1.41L5.99 4.58zm12.37 12.37c-.39-.39-1.03-.39-1.41 0-.39.39-.39 1.03 0 1.41l1.06 1.06c.39.39 1.03.39 1.41 0 .39-.39.39-1.03 0-1.41l-1.06-1.06zm1.06-10.96c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06zM7.05 18.36c.39-.39.39-1.03 0-1.41-.39-.39-1.03-.39-1.41 0l-1.06 1.06c-.39.39-.39 1.03 0 1.41s1.03.39 1.41 0l1.06-1.06z"/>
        </svg>
        <svg v-else viewBox="0 0 24 24" width="20" height="20">
          <path fill="currentColor" d="M9 2c-1.05 0-2.05.16-3 .46 4.06 1.27 7 5.06 7 9.54 0 4.48-2.94 8.27-7 9.54.95.3 1.95.46 3 .46 5.52 0 10-4.48 10-10S14.52 2 9 2z"/>
        </svg>
      </button>

      <!-- 用户菜单 -->
      <div class="user-menu" ref="userMenuRef">
        <button class="user-avatar" @click="toggleUserMenu">
          <img :src="userAvatar" :alt="userName" class="avatar-img">
          <svg viewBox="0 0 24 24" width="16" height="16" class="dropdown-icon">
            <path fill="currentColor" d="M7 10l5 5 5-5z"/>
          </svg>
        </button>
        
        <div class="user-dropdown" v-show="showUserMenu">
          <div class="user-info">
            <div class="user-name">{{ userName }}</div>
            <div class="user-email">{{ userEmail }}</div>
          </div>
          <div class="dropdown-divider"></div>
          <ul class="dropdown-menu">
            <li>
              <router-link to="/profile" class="dropdown-item">
                <svg viewBox="0 0 24 24" width="16" height="16">
                  <path fill="currentColor" d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
                个人资料
              </router-link>
            </li>
            <li>
              <router-link to="/settings" class="dropdown-item">
                <svg viewBox="0 0 24 24" width="16" height="16">
                  <path fill="currentColor" d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
                </svg>
                设置
              </router-link>
            </li>
            <li>
              <button class="dropdown-item" @click="logout">
                <svg viewBox="0 0 24 24" width="16" height="16">
                  <path fill="currentColor" d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
                </svg>
                退出登录
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

// 响应式数据
const showUserMenu = ref(false)
const isDarkMode = ref(false)
const notificationCount = ref(3)
const userMenuRef = ref<HTMLElement>()

// 计算属性
const currentPageName = computed(() => {
  const routeName = route.name as string
  const pageNames: Record<string, string> = {
    'dashboard': 'dashboard',
    'analytics': 'analytics',
    'organization': 'organization',
    'projects': 'projects',
    'transactions': 'transactions',
    'invoices': 'invoices',
    'payments': 'payments',
    'members': 'members',
    'permissions': 'permissions',
    'chat': 'chat',
    'meetings': 'meetings',
    'settings': 'settings',
    'help': 'help'
  }
  return pageNames[routeName] || 'dashboard'
})

const userName = computed(() => authStore.currentUser?.full_name || 'User')
const userEmail = computed(() => authStore.currentUser?.email || 'user@example.com')
const userAvatar = computed(() => `https://ui-avatars.com/api/?name=${encodeURIComponent(userName.value)}&background=10b981&color=fff&size=32`)

// 方法
const toggleMobileMenu = () => {
  // 触发移动端菜单切换事件
  document.dispatchEvent(new CustomEvent('toggle-mobile-menu'))
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  // 这里可以添加主题切换逻辑
}

const showNotifications = () => {
  // 显示通知面板
  console.log('显示通知')
}

const logout = async () => {
  await authStore.logout()
  showUserMenu.value = false
}

// 点击外部关闭用户菜单
const handleClickOutside = (event: MouseEvent) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target as Node)) {
    showUserMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.header {
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: fixed;
  top: 0;
  left: 240px;
  right: 0;
  z-index: 50;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.mobile-menu-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.breadcrumb-list {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 8px;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
}

.breadcrumb-link {
  color: #6b7280;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s ease;
}

.breadcrumb-link:hover {
  color: #111827;
}

.breadcrumb-separator {
  color: #d1d5db;
  display: flex;
  align-items: center;
}

.breadcrumb-current {
  color: #111827;
  font-size: 14px;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-btn {
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
  position: relative;
}

.header-btn:hover {
  background: #f3f4f6;
  color: #111827;
}

.notification-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #ef4444;
  color: white;
  font-size: 10px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
  line-height: 1;
}

.user-menu {
  position: relative;
}

.user-avatar {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.user-avatar:hover {
  background: #f3f4f6;
}

.avatar-img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.dropdown-icon {
  color: #6b7280;
  transition: transform 0.2s ease;
}

.user-avatar:hover .dropdown-icon {
  color: #111827;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  min-width: 200px;
  z-index: 100;
}

.user-info {
  padding: 12px 16px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 2px;
}

.user-email {
  font-size: 12px;
  color: #6b7280;
}

.dropdown-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 0;
}

.dropdown-menu {
  list-style: none;
  margin: 0;
  padding: 8px 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 16px;
  color: #374151;
  text-decoration: none;
  font-size: 14px;
  border: none;
  background: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background: #f3f4f6;
  color: #111827;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header {
    left: 0;
    padding: 0 16px;
  }
  
  .mobile-menu-btn {
    display: block;
  }
  
  .breadcrumb {
    display: none;
  }
}
</style> 