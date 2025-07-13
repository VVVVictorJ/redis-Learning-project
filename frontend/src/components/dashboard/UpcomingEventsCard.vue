<template>
  <Card>
    <template #header>
      <div class="card-header-content">
        <svg viewBox="0 0 24 24" width="20" height="20" class="header-icon">
          <path fill="currentColor" d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
        </svg>
        <h3 class="card-title">Upcoming Events</h3>
      </div>
    </template>

    <div class="events-content">
      <div class="events-grid">
        <div 
          class="event-item" 
          v-for="event in events" 
          :key="event.id"
        >
          <div class="event-header">
            <div class="event-icon" :class="event.status">
              <svg viewBox="0 0 24 24" width="16" height="16">
                <path fill="currentColor" :d="getEventIcon(event.status)"/>
              </svg>
            </div>
            <div class="event-status" :class="event.status">
              {{ event.status }}
            </div>
          </div>

          <div class="event-content">
            <h4 class="event-title">{{ event.title }}</h4>
            <p class="event-description">{{ event.description }}</p>
            
            <div class="event-progress">
              <div class="progress-header">
                <span class="progress-label">Progress</span>
                <span class="progress-value">{{ event.progress }}%</span>
              </div>
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: event.progress + '%' }"
                  :class="event.status"
                ></div>
              </div>
            </div>

            <div class="event-meta">
              <div class="event-target">
                <span class="target-amount">${{ event.target }}</span>
                <span class="target-label">target</span>
              </div>
              <div class="event-date">
                <svg viewBox="0 0 24 24" width="14" height="14">
                  <path fill="currentColor" d="M19 3h-1V1h-2v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V8h14v11zM7 10h5v5H7z"/>
                </svg>
                <span class="date-text">Target: {{ event.targetDate }}</span>
              </div>
            </div>

            <div class="event-actions">
              <button class="action-link">
                View Details
                <svg viewBox="0 0 24 24" width="14" height="14">
                  <path fill="currentColor" d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Card from '@/components/ui/Card.vue'

interface Event {
  id: string
  title: string
  description: string
  progress: number
  target: string
  targetDate: string
  status: 'in-progress' | 'pending' | 'completed'
}

const events = ref<Event[]>([
  {
    id: '1',
    title: 'Emergency Fund',
    description: '3 months of expenses saved',
    progress: 65,
    target: '15,000',
    targetDate: 'Dec 2024',
    status: 'in-progress'
  },
  {
    id: '2',
    title: 'Stock Portfolio',
    description: 'Tech sector investment plan',
    progress: 30,
    target: '50,000',
    targetDate: 'Jun 2024',
    status: 'pending'
  },
  {
    id: '3',
    title: 'Debt Repayment',
    description: 'Student loan payoff plan',
    progress: 45,
    target: '25,000',
    targetDate: 'Mar 2025',
    status: 'in-progress'
  }
])

const getEventIcon = (status: string) => {
  switch (status) {
    case 'in-progress':
      return 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'
    case 'pending':
      return 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z'
    case 'completed':
      return 'M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z'
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

.events-content {
  padding: 0;
}

.events-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
}

.event-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 20px;
  background: #ffffff;
  transition: all 0.2s ease;
}

.event-item:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.event-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.event-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.event-icon.in-progress {
  background: #dbeafe;
  color: #2563eb;
}

.event-icon.pending {
  background: #fef3c7;
  color: #d97706;
}

.event-icon.completed {
  background: #dcfce7;
  color: #16a34a;
}

.event-status {
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
  padding: 2px 8px;
  border-radius: 12px;
}

.event-status.in-progress {
  background: #dbeafe;
  color: #2563eb;
}

.event-status.pending {
  background: #fef3c7;
  color: #d97706;
}

.event-status.completed {
  background: #dcfce7;
  color: #16a34a;
}

.event-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.event-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.event-description {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.event-progress {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-label {
  font-size: 14px;
  color: #374151;
  font-weight: 500;
}

.progress-value {
  font-size: 14px;
  color: #111827;
  font-weight: 600;
}

.progress-bar {
  height: 8px;
  background: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-fill.in-progress {
  background: #2563eb;
}

.progress-fill.pending {
  background: #d97706;
}

.progress-fill.completed {
  background: #16a34a;
}

.event-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.event-target {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.target-amount {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
}

.target-label {
  font-size: 12px;
  color: #6b7280;
}

.event-date {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #6b7280;
}

.date-text {
  font-size: 12px;
}

.event-actions {
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.action-link {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  color: #2563eb;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s ease;
}

.action-link:hover {
  color: #1d4ed8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .events-grid {
    grid-template-columns: 1fr;
  }
}
</style> 