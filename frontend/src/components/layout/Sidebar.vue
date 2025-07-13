<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <div class="logo">
        <svg viewBox="0 0 24 24" width="24" height="24" class="logo-icon">
          <path fill="#10b981" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        </svg>
        <span class="logo-text">CatExpense</span>
      </div>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section">
        <h3 class="nav-section-title">OVERVIEW</h3>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/dashboard" class="nav-link" :class="{ active: $route.path === '/dashboard' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
              </svg>
              <span>Expense</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/analytics" class="nav-link" :class="{ active: $route.path === '/analytics' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z"/>
              </svg>
              <span>Analytics</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/organization" class="nav-link" :class="{ active: $route.path === '/organization' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
              <span>Organization</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/projects" class="nav-link" :class="{ active: $route.path === '/projects' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
              </svg>
              <span>Projects</span>
            </router-link>
          </li>
        </ul>
      </div>

      <div class="nav-section">
        <h3 class="nav-section-title">FINANCE</h3>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/transactions" class="nav-link" :class="{ active: $route.path === '/transactions' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M7 18c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12L8.1 13h7.45c.75 0 1.41-.41 1.75-1.03L21.7 4H5.21l-.94-2H1zm16 16c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
              </svg>
              <span>Transactions</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/invoices" class="nav-link" :class="{ active: $route.path === '/invoices' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 2 2h8c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
              </svg>
              <span>Invoices</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/payments" class="nav-link" :class="{ active: $route.path === '/payments' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z"/>
              </svg>
              <span>Payments</span>
            </router-link>
          </li>
        </ul>
      </div>

      <div class="nav-section">
        <h3 class="nav-section-title">TEAM</h3>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/members" class="nav-link" :class="{ active: $route.path === '/members' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M16 4c0-1.11.89-2 2-2s2 .89 2 2-.89 2-2 2-2-.89-2-2zm4 18v-6h2.5l-2.54-7.63A1.5 1.5 0 0 0 18.5 7.5h-3A1.5 1.5 0 0 0 14.04 8.37L11.5 16H14v6h6zM12.5 11.5c.83 0 1.5-.67 1.5-1.5s-.67-1.5-1.5-1.5S11 9.17 11 10s.67 1.5 1.5 1.5zM5.5 6c1.11 0 2-.89 2-2s-.89-2-2-2-2 .89-2 2 .89 2 2 2zm2.5 16v-7H6.5l2.5-7.5H7.5L5 15v7h3z"/>
              </svg>
              <span>Members</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/permissions" class="nav-link" :class="{ active: $route.path === '/permissions' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
              </svg>
              <span>Permissions</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/chat" class="nav-link" :class="{ active: $route.path === '/chat' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4l4 4 4-4h4c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
              </svg>
              <span>Chat</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/meetings" class="nav-link" :class="{ active: $route.path === '/meetings' }">
              <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
              </svg>
              <span>Meetings</span>
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <div class="sidebar-footer">
      <ul class="nav-list">
        <li class="nav-item">
          <router-link to="/settings" class="nav-link" :class="{ active: $route.path === '/settings' }">
            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
            </svg>
            <span>Settings</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link to="/help" class="nav-link" :class="{ active: $route.path === '/help' }">
            <svg class="nav-icon" viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z"/>
            </svg>
            <span>Help</span>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
// 组件逻辑可以在这里添加
</script>

<style scoped>
.sidebar {
  width: 240px;
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  flex-shrink: 0;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
}

.nav-section {
  margin-bottom: 32px;
}

.nav-section-title {
  font-size: 11px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0 0 12px 20px;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-item {
  margin-bottom: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 20px;
  color: #6b7280;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  border-radius: 0;
}

.nav-link:hover {
  background: #f3f4f6;
  color: #111827;
}

.nav-link.active {
  background: #f3f4f6;
  color: #111827;
  border-right: 3px solid #10b981;
}

.nav-icon {
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 20px 0;
  border-top: 1px solid #e5e7eb;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar.open {
    transform: translateX(0);
  }
}
</style> 