<template>
  <div class="layout">
    <!-- 侧边栏 -->
    <Sidebar />
    
    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 头部 -->
      <Header />
      
      <!-- 页面内容 -->
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import Sidebar from '@/components/layout/Sidebar.vue'
import Header from '@/components/layout/Header.vue'
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  margin-left: 240px;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  padding: 24px;
  margin-top: 64px; /* Header height */
  background: #f9fafb;
  min-height: calc(100vh - 64px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }
}
</style> 