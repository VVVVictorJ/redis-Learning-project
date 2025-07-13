<template>
  <Card>
    <template #header>
      <div class="card-header-content">
        <svg viewBox="0 0 24 24" width="20" height="20" class="header-icon">
          <path fill="currentColor" d="M7 18c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12L8.1 13h7.45c.75 0 1.41-.41 1.75-1.03L21.7 4H5.21l-.94-2H1zm16 16c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/>
        </svg>
        <h3 class="card-title">Recent Transactions</h3>
      </div>
    </template>

    <div class="transactions-content">
      <!-- 活动统计 -->
      <div class="activity-stats">
        <div class="stats-item">
          <div class="stats-label">Recent Activity</div>
          <div class="stats-value">({{ transactions.length }} transactions)</div>
        </div>
        <div class="time-filter">
          <span class="filter-label">This Month</span>
        </div>
      </div>

      <!-- 交易列表 -->
      <div class="transactions-list">
        <div 
          class="transaction-item" 
          v-for="transaction in transactions" 
          :key="transaction.id"
        >
          <div class="transaction-info">
            <div class="transaction-icon" :class="transaction.type">
              <svg viewBox="0 0 24 24" width="16" height="16">
                <path fill="currentColor" :d="getTransactionIcon(transaction.type)"/>
              </svg>
            </div>
            <div class="transaction-details">
              <div class="transaction-title">{{ transaction.title }}</div>
              <div class="transaction-meta">
                <span class="transaction-time">{{ transaction.time }}</span>
              </div>
            </div>
          </div>
          <div class="transaction-amount" :class="transaction.type">
            {{ transaction.type === 'income' ? '+' : '-' }}${{ transaction.amount }}
            <svg viewBox="0 0 24 24" width="16" height="16" class="trend-icon">
              <path fill="currentColor" d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
            </svg>
          </div>
        </div>
      </div>

      <!-- 查看所有交易按钮 -->
      <div class="view-all-section">
        <button class="view-all-btn">
          View All Transactions
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
          </svg>
        </button>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'

interface Transaction {
  id: string
  title: string
  time: string
  amount: string
  type: 'income' | 'expense'
}

const transactions = ref<Transaction[]>([
  {
    id: '1',
    title: 'Apple Store Purchase',
    time: 'Today, 2:45 PM',
    amount: '999.00',
    type: 'expense'
  },
  {
    id: '2',
    title: 'Salary Deposit',
    time: 'Today, 9:00 AM',
    amount: '4,500.00',
    type: 'income'
  },
  {
    id: '3',
    title: 'Netflix Subscription',
    time: 'Yesterday',
    amount: '15.99',
    type: 'expense'
  },
  {
    id: '4',
    title: 'Apple Store Purchase',
    time: 'Today, 2:45 PM',
    amount: '999.00',
    type: 'expense'
  },
  {
    id: '5',
    title: 'Supabase Subscription',
    time: 'Yesterday',
    amount: '15.99',
    type: 'expense'
  },
  {
    id: '6',
    title: 'Vercel Subscription',
    time: 'Yesterday',
    amount: '15.99',
    type: 'expense'
  }
])

const getTransactionIcon = (type: string) => {
  switch (type) {
    case 'income':
      return 'M7 14l5-5 5 5z'
    case 'expense':
      return 'M7 10l5 5 5-5z'
    default:
      return 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z'
  }
}
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

.transactions-content {
  padding: 0;
}

.activity-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0 20px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #f3f4f6;
}

.stats-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stats-label {
  font-size: 14px;
  color: #6b7280;
}

.stats-value {
  font-size: 12px;
  color: #9ca3af;
}

.time-filter {
  display: flex;
  align-items: center;
}

.filter-label {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.transactions-list {
  margin-bottom: 24px;
}

.transaction-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f9fafb;
}

.transaction-item:last-child {
  border-bottom: none;
}

.transaction-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.transaction-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.transaction-icon.income {
  background: #dcfce7;
  color: #16a34a;
}

.transaction-icon.expense {
  background: #fef2f2;
  color: #dc2626;
}

.transaction-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.transaction-title {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.transaction-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.transaction-time {
  font-size: 12px;
  color: #6b7280;
}

.transaction-amount {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 600;
}

.transaction-amount.income {
  color: #16a34a;
}

.transaction-amount.expense {
  color: #dc2626;
}

.trend-icon {
  color: #9ca3af;
}

.view-all-section {
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.view-all-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  background: #111827;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-all-btn:hover {
  background: #1f2937;
}
</style> 