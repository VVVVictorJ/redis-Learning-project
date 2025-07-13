<template>
  <div class="login-container">
    <!-- 左侧背景区域 -->
    <div class="left-section">
      <div class="background-overlay">
        <div class="content">
          <div class="logo">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            <h1>CAT EXPENSE</h1>
          </div>
          <div class="social-icons">
            <div class="social-icon facebook">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </div>
            <div class="social-icon twitter">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </div>
            <div class="social-icon google">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
            </div>
          </div>
          <div class="signup-text">
            <p>Don't have an account?</p>
            <a href="#" @click="activeTab = 'register'">Signup</a>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧登录表单区域 -->
    <div class="right-section">
      <div class="login-card">
        <div class="brand-logo">
          <div class="logo-icon">
            <svg viewBox="0 0 24 24" width="40" height="40">
              <path fill="#4A90E2" d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.22.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/>
            </svg>
          </div>
          <h2>CAT EXPENSE</h2>
        </div>

        <el-tabs v-model="activeTab" class="login-tabs">
          <el-tab-pane label="登录" name="login">
            <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" @submit.prevent="handleLogin" class="login-form">
              <el-form-item prop="email">
                <el-input 
                  v-model="loginForm.email" 
                  placeholder="User Name" 
                  size="large"
                  class="custom-input"
                />
              </el-form-item>
              <el-form-item prop="password">
                <el-input 
                  v-model="loginForm.password" 
                  type="password" 
                  placeholder="Password" 
                  show-password 
                  size="large"
                  class="custom-input"
                />
              </el-form-item>
              <el-form-item>
                <div class="remember-me">
                  <el-checkbox v-model="rememberMe">Remember Me</el-checkbox>
                </div>
              </el-form-item>
              <el-form-item>
                <el-button 
                  type="primary" 
                  native-type="submit" 
                  :loading="loading" 
                  size="large"
                  class="login-button"
                >
                  LOGIN
                </el-button>
              </el-form-item>
              <div class="forgot-password">
                <a href="#">Forgot Password?</a>
              </div>
            </el-form>
          </el-tab-pane>
          
          <el-tab-pane label="注册" name="register">
            <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules" @submit.prevent="handleRegister" class="login-form">
              <el-form-item prop="email">
                <el-input 
                  v-model="registerForm.email" 
                  placeholder="Email" 
                  size="large"
                  class="custom-input"
                />
              </el-form-item>
              <el-form-item prop="password">
                <el-input 
                  v-model="registerForm.password" 
                  type="password" 
                  placeholder="Password" 
                  show-password 
                  size="large"
                  class="custom-input"
                />
              </el-form-item>
              <el-form-item prop="fullName">
                <el-input 
                  v-model="registerForm.fullName" 
                  placeholder="Full Name (Optional)" 
                  size="large"
                  class="custom-input"
                />
              </el-form-item>
              <el-form-item>
                <el-button 
                  type="primary" 
                  native-type="submit" 
                  :loading="loading" 
                  size="large"
                  class="login-button"
                >
                  REGISTER
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const activeTab = ref('login')
const loading = ref(false)
const rememberMe = ref(false)

// Login Form
const loginFormRef = ref<FormInstance>()
const loginForm = reactive({
  email: '',
  password: '',
})
const loginRules = reactive<FormRules>({
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
})

// Register Form
const registerFormRef = ref<FormInstance>()
const registerForm = reactive({
  email: '',
  password: '',
  fullName: '',
})
const registerRules = reactive<FormRules>({
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 8, message: '密码长度不能少于8位', trigger: 'blur' }],
})

const handleLogin = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const formData = new FormData()
        formData.append('username', loginForm.email)
        formData.append('password', loginForm.password)
        await authStore.login(formData)
        ElMessage.success('登录成功')
      } catch (error) {
        ElMessage.error('登录失败，请检查邮箱或密码')
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await authStore.register({
          email: registerForm.email,
          password: registerForm.password,
          full_name: registerForm.fullName || undefined,
        })
        ElMessage.success('注册成功，已自动登录')
      } catch (error) {
        ElMessage.error('注册失败，该邮箱可能已被使用')
        console.error(error)
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* 左侧背景区域 */
.left-section {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><pattern id="cat-pattern" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="1000" height="1000" fill="url(%23cat-pattern)"/></svg>');
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.background-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.content {
  text-align: center;
  color: white;
}

.logo {
  margin-bottom: 60px;
}

.logo svg {
  margin-bottom: 20px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.logo h1 {
  font-size: 32px;
  font-weight: 300;
  margin: 0;
  letter-spacing: 2px;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 60px;
}

.social-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.social-icon:hover {
  transform: scale(1.1);
}

.social-icon.facebook {
  background-color: #3b5998;
}

.social-icon.twitter {
  background-color: #1da1f2;
}

.social-icon.google {
  background-color: #dd4b39;
}

.social-icon svg {
  color: white;
}

.signup-text {
  font-size: 16px;
}

.signup-text p {
  margin: 0 0 10px 0;
  opacity: 0.9;
}

.signup-text a {
  color: white;
  text-decoration: underline;
  font-weight: 500;
  cursor: pointer;
}

.signup-text a:hover {
  opacity: 0.8;
}

/* 右侧登录表单区域 */
.right-section {
  flex: 1;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.brand-logo {
  text-align: center;
  margin-bottom: 40px;
}

.logo-icon {
  margin-bottom: 15px;
}

.brand-logo h2 {
  color: #4A90E2;
  font-size: 28px;
  font-weight: 600;
  margin: 0;
  letter-spacing: 1px;
}

.login-tabs {
  border: none;
}

.login-tabs :deep(.el-tabs__header) {
  margin-bottom: 30px;
}

.login-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.login-tabs :deep(.el-tabs__item) {
  font-size: 16px;
  font-weight: 500;
  color: #999;
}

.login-tabs :deep(.el-tabs__item.is-active) {
  color: #4A90E2;
}

.login-tabs :deep(.el-tabs__active-bar) {
  background-color: #4A90E2;
}

.login-form {
  margin-top: 20px;
}

.custom-input :deep(.el-input__wrapper) {
  border-radius: 8px;
  border: 1px solid #e1e8ed;
  box-shadow: none;
  padding: 12px 16px;
  background-color: #f8f9fa;
}

.custom-input :deep(.el-input__wrapper:hover) {
  border-color: #4A90E2;
}

.custom-input :deep(.el-input__wrapper.is-focus) {
  border-color: #4A90E2;
  box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.1);
}

.custom-input :deep(.el-input__inner) {
  color: #333;
  font-size: 14px;
  background-color: transparent;
}

.custom-input :deep(.el-input__inner::placeholder) {
  color: #999;
}

.remember-me {
  margin: 10px 0;
}

.remember-me :deep(.el-checkbox__label) {
  color: #666;
  font-size: 14px;
}

.login-button {
  width: 100%;
  height: 48px;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1px;
  margin-top: 10px;
}

.login-button:hover {
  background: linear-gradient(135deg, #357ABD 0%, #2E6DA4 100%);
}

.forgot-password {
  text-align: center;
  margin-top: 20px;
}

.forgot-password a {
  color: #4A90E2;
  text-decoration: none;
  font-size: 14px;
}

.forgot-password a:hover {
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
  }
  
  .left-section {
    flex: 0 0 200px;
  }
  
  .logo h1 {
    font-size: 24px;
  }
  
  .social-icons {
    margin-bottom: 30px;
  }
  
  .right-section {
    flex: 1;
    padding: 20px;
  }
}
</style> 