import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/Login.vue'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/',
      component: DefaultLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/dashboard'
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('../views/Dashboard.vue'),
        },
        {
          path: 'analytics',
          name: 'analytics',
          component: () => import('../views/About.vue'), // 暂时使用About页面
        },
        {
          path: 'organization',
          name: 'organization',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'projects',
          name: 'projects',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'transactions',
          name: 'transactions',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'invoices',
          name: 'invoices',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'payments',
          name: 'payments',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'members',
          name: 'members',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'permissions',
          name: 'permissions',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'chat',
          name: 'chat',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'meetings',
          name: 'meetings',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('../views/About.vue'),
        },
        {
          path: 'help',
          name: 'help',
          component: () => import('../views/About.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  // Try to fetch user info if token exists but user info is missing
  if (authStore.token && !authStore.currentUser) {
    await authStore.fetchCurrentUser()
  }

  const requiresAuth = to.meta.requiresAuth
  const isLoggedIn = !!authStore.currentUser

  if (requiresAuth && !isLoggedIn) {
    // Redirect to login page
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.name === 'login' && isLoggedIn) {
    // Redirect to dashboard if already logged in
    return { name: 'dashboard' }
  }
})

export default router

