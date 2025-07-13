<template>
  <div class="dashboard">
    <div class="dashboard-grid">
      <!-- 支出卡片 -->
      <div class="dashboard-section full-width">
        <div class="card-container">
          <ExpenseCard />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ExpenseCard from '@/components/dashboard/ExpenseCard.vue'
</script>

<style scoped>
.dashboard {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.card-container {
  width: 90%;
  max-width: 1000px;
  margin: 0 auto;
}

/* 响应式设计 */
@media (min-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr 1fr;
  }
  
  .full-width {
    grid-column: 1 / -1;
  }
}
</style>
