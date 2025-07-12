import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import LoginView from '../views/Login.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView, // We will change this to a layout component later
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/About.vue'),
      meta: { requiresAuth: true },
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
    // Redirect to home if already logged in
    return { name: 'home' }
  }
})

export default router

