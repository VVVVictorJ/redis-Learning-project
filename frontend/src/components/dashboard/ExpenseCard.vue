<template>
  <Card>
    <template #header>
      <div class="card-header-content">
        <svg viewBox="0 0 24 24" width="20" height="20" class="header-icon">
          <path fill="currentColor" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
        </svg>
        <h3 class="card-title">我的支出</h3>
      </div>
    </template>

    <div class="expense-content">
      <!-- 总支出 -->
      <div class="total-expense">
        <div class="expense-label">本月总支出</div>
        <div class="expense-amount">¥{{ totalExpense }}</div>
      </div>

      <!-- 支出统计 -->
      <div class="expense-stats">
        <div class="stat-item">
          <div class="stat-label">支出笔数</div>
          <div class="stat-value">{{ expenses.length }}</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">平均金额</div>
          <div class="stat-value">¥{{ averageExpense }}</div>
        </div>
      </div>

      <!-- 最近支出列表 -->
      <div class="recent-expenses">
        <div class="section-title">最近支出</div>
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        <div v-else-if="expenses.length === 0" class="empty-state">
          <svg viewBox="0 0 24 24" width="48" height="48" class="empty-icon">
            <path fill="#d1d5db" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
          </svg>
          <p>暂无支出记录</p>
          <button class="add-expense-btn" @click="showAddExpenseForm = true">
            添加第一笔支出
          </button>
        </div>
        <div v-else class="expense-list">
          <div class="expense-item" v-for="expense in recentExpenses" :key="expense.id">
            <div class="expense-info">
              <div class="expense-icon" :style="{ backgroundColor: getExpenseColor(expense.amount) }">
                <svg viewBox="0 0 24 24" width="16" height="16">
                  <path fill="white" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                </svg>
              </div>
              <div class="expense-details">
                <div class="expense-description">{{ expense.description || '无描述' }}</div>
                <div class="expense-date">{{ formatDate(expense.date) }}</div>
              </div>
            </div>
            <div class="expense-amount-item">¥{{ expense.amount.toFixed(2) }}</div>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="expense-actions">
        <button class="action-btn primary" @click="showAddExpenseForm = true">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
          </svg>
          添加支出
        </button>
        <button class="action-btn secondary" @click="refreshExpenses">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
          </svg>
          刷新
        </button>
        <button class="action-btn secondary">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M9 11H7v6h2v-6zm4 0h-2v6h2v-6zm4 0h-2v6h2v-6zm2-7h-3l-1-1h-4l-1 1H5v2h14V4z"/>
          </svg>
          统计
        </button>
        <button class="action-btn secondary">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          更多
        </button>
      </div>
    </div>

    <!-- 添加支出弹窗 -->
    <div v-if="showAddExpenseForm" class="expense-modal-overlay" @click="closeModal">
      <div class="expense-modal" @click.stop>
        <div class="modal-header">
          <h4>添加新支出</h4>
          <button class="close-btn" @click="showAddExpenseForm = false">
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="addExpense" class="expense-form">
          <div class="form-group">
            <label for="description">描述</label>
            <input
              id="description"
              v-model="newExpense.description"
              type="text"
              placeholder="请输入支出描述"
              required
            />
          </div>
          <div class="form-group">
            <label for="amount">金额</label>
            <input
              id="amount"
              v-model.number="newExpense.amount"
              type="number"
              step="0.01"
              min="0"
              placeholder="0.00"
              required
            />
          </div>
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="showAddExpenseForm = false">
              取消
            </button>
            <button type="submit" class="submit-btn" :disabled="submitting">
              {{ submitting ? '添加中...' : '添加支出' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Card from '@/components/ui/Card.vue'
import { expenseApi } from '@/services/api'
import type { Expense } from '@/schemas/expense'

interface ExpenseData {
  id: number
  description: string
  amount: number
  date: string
  owner_id: number
}

const expenses = ref<ExpenseData[]>([])
const loading = ref(false)
const showAddExpenseForm = ref(false)
const submitting = ref(false)

const newExpense = ref({
  description: '',
  amount: 0
})

// 计算总支出
const totalExpense = computed(() => {
  const total = expenses.value.reduce((sum, expense) => sum + expense.amount, 0)
  return total.toFixed(2)
})

// 计算平均支出
const averageExpense = computed(() => {
  if (expenses.value.length === 0) return '0.00'
  const average = expenses.value.reduce((sum, expense) => sum + expense.amount, 0) / expenses.value.length
  return average.toFixed(2)
})

// 获取最近的5笔支出
const recentExpenses = computed(() => {
  return expenses.value
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .slice(0, 5)
})

// 根据金额获取颜色
const getExpenseColor = (amount: number) => {
  if (amount > 1000) return '#ef4444' // 红色 - 大额支出
  if (amount > 500) return '#f97316' // 橙色 - 中等支出
  if (amount > 100) return '#eab308' // 黄色 - 小额支出
  return '#10b981' // 绿色 - 微小支出
}

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '今天'
  if (diffDays === 1) return '昨天'
  if (diffDays < 7) return `${diffDays}天前`
  
  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  })
}

// 获取支出数据
const fetchExpenses = async () => {
  try {
    loading.value = true
    const data = await expenseApi.getMyExpenses()
    expenses.value = data
  } catch (error: any) {
    console.error('获取支出数据失败:', error)
    // 如果是401错误，不要重试，让拦截器处理跳转
    if (error.response?.status === 401) {
      return
    }
    // 对于其他错误，设置空数组避免显示错误
    expenses.value = []
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshExpenses = () => {
  fetchExpenses()
}

// 添加新支出
const addExpense = async () => {
  try {
    submitting.value = true
    await expenseApi.createExpense(newExpense.value)
    
    // 重置表单
    newExpense.value = {
      description: '',
      amount: 0
    }
    
    // 关闭弹窗并刷新数据
    showAddExpenseForm.value = false
    await fetchExpenses()
  } catch (error) {
    console.error('添加支出失败:', error)
  } finally {
    submitting.value = false
  }
}

// 关闭弹窗
const closeModal = () => {
  showAddExpenseForm.value = false
}

// 组件挂载时获取数据
onMounted(() => {
  fetchExpenses()
})
</script>

<style scoped>
.card-header-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  color: #6b7280;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.expense-content {
  padding: 0;
}

.total-expense {
  padding: 0 0 20px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #f3f4f6;
}

.expense-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.expense-amount {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
}

.expense-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f3f4f6;
}

.stat-item {
  flex: 1;
}

.stat-label {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 16px;
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 40px 0;
  color: #6b7280;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #f3f4f6;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  margin-bottom: 16px;
}

.empty-state p {
  color: #6b7280;
  margin-bottom: 16px;
}

.add-expense-btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.2s ease;
}

.add-expense-btn:hover {
  background: #2563eb;
}

.expense-list {
  margin-bottom: 24px;
}

.expense-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f9fafb;
}

.expense-item:last-child {
  border-bottom: none;
}

.expense-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.expense-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.expense-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.expense-description {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.expense-date {
  font-size: 12px;
  color: #6b7280;
}

.expense-amount-item {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.expense-actions {
  display: flex;
  gap: 8px;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  flex: 1;
  justify-content: center;
}

.action-btn.primary {
  background: #111827;
  color: white;
}

.action-btn.primary:hover {
  background: #1f2937;
}

.action-btn.secondary {
  background: #f9fafb;
  color: #374151;
  border: 1px solid #e5e7eb;
}

.action-btn.secondary:hover {
  background: #f3f4f6;
}

/* 弹窗样式 */
.expense-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.expense-modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h4 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #111827;
}

.close-btn {
  background: none;
  border: none;
  padding: 4px;
  cursor: pointer;
  color: #6b7280;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.close-btn:hover {
  background: #f3f4f6;
}

.expense-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s ease;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #3b82f6;
}

.form-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.cancel-btn, .submit-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn {
  background: #f9fafb;
  color: #374151;
  border: 1px solid #d1d5db;
}

.cancel-btn:hover {
  background: #f3f4f6;
}

.submit-btn {
  background: #3b82f6;
  color: white;
  border: none;
}

.submit-btn:hover:not(:disabled) {
  background: #2563eb;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style> 