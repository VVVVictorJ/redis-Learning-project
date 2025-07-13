<template>
  <Card>
    <template #header>
      <div class="card-header-content">
        <svg viewBox="0 0 24 24" width="20" height="20" class="header-icon">
          <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
        </svg>
        <h3 class="card-title">Accounts</h3>
      </div>
    </template>

    <div class="accounts-content">
      <!-- 总余额 -->
      <div class="total-balance">
        <div class="balance-label">Total Balance</div>
        <div class="balance-amount">${{ totalBalance }}</div>
      </div>

      <!-- 账户列表 -->
      <div class="accounts-list">
        <div class="account-section-title">Your Accounts</div>
        <div class="account-item" v-for="account in accounts" :key="account.id">
          <div class="account-info">
            <div class="account-icon" :style="{ backgroundColor: account.color }">
              <svg viewBox="0 0 24 24" width="16" height="16">
                <path fill="white" :d="account.icon"/>
              </svg>
            </div>
            <div class="account-details">
              <div class="account-name">{{ account.name }}</div>
              <div class="account-type">{{ account.type }}</div>
            </div>
          </div>
          <div class="account-balance">${{ account.balance }}</div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="account-actions">
        <button class="action-btn primary">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
          </svg>
          Add
        </button>
        <button class="action-btn secondary">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm4.59-12.42L10 14.17l-2.59-2.58L6 13l4 4 8-8-1.41-1.42z"/>
          </svg>
          Send
        </button>
        <button class="action-btn secondary">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
          Top-up
        </button>
        <button class="action-btn secondary">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 11h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/>
          </svg>
          More
        </button>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Card from '@/components/ui/Card.vue'

interface Account {
  id: string
  name: string
  type: string
  balance: string
  color: string
  icon: string
}

const accounts = ref<Account[]>([
  {
    id: '1',
    name: 'Main Savings',
    type: 'Personal savings',
    balance: '8,459.45',
    color: '#10b981',
    icon: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'
  },
  {
    id: '2',
    name: 'Checking Account',
    type: 'Daily expenses',
    balance: '2,850.00',
    color: '#3b82f6',
    icon: 'M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z'
  },
  {
    id: '3',
    name: 'Investment Portfolio',
    type: 'Stock & ETFs',
    balance: '15,230.80',
    color: '#8b5cf6',
    icon: 'M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6z'
  },
  {
    id: '4',
    name: 'Credit Card',
    type: 'Pending charges',
    balance: '1,200.00',
    color: '#ef4444',
    icon: 'M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z'
  },
  {
    id: '5',
    name: 'Savings Account',
    type: 'Emergency fund',
    balance: '3,000.00',
    color: '#10b981',
    icon: 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'
  }
])

const totalBalance = computed(() => {
  const total = accounts.value.reduce((sum, account) => {
    const balance = parseFloat(account.balance.replace(',', ''))
    return sum + balance
  }, 0)
  return total.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
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

.accounts-content {
  padding: 0;
}

.total-balance {
  padding: 0 0 20px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #f3f4f6;
}

.balance-label {
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 8px;
}

.balance-amount {
  font-size: 32px;
  font-weight: 700;
  color: #111827;
}

.account-section-title {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 16px;
}

.accounts-list {
  margin-bottom: 24px;
}

.account-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f9fafb;
}

.account-item:last-child {
  border-bottom: none;
}

.account-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.account-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.account-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.account-name {
  font-size: 14px;
  font-weight: 500;
  color: #111827;
}

.account-type {
  font-size: 12px;
  color: #6b7280;
}

.account-balance {
  font-size: 14px;
  font-weight: 600;
  color: #111827;
}

.account-actions {
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
</style> 