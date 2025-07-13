<template>
  <div class="card" :class="cardClasses">
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <h3 class="card-title">{{ title }}</h3>
      </slot>
    </div>
    
    <div class="card-body" :class="bodyClasses">
      <slot />
    </div>
    
    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title?: string
  shadow?: 'none' | 'sm' | 'md' | 'lg'
  padding?: 'none' | 'sm' | 'md' | 'lg'
  rounded?: 'none' | 'sm' | 'md' | 'lg'
  border?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  shadow: 'sm',
  padding: 'md',
  rounded: 'md',
  border: true
})

const cardClasses = computed(() => {
  const classes = ['card']
  
  // Shadow
  switch (props.shadow) {
    case 'none':
      break
    case 'sm':
      classes.push('shadow-sm')
      break
    case 'md':
      classes.push('shadow-md')
      break
    case 'lg':
      classes.push('shadow-lg')
      break
  }
  
  // Rounded
  switch (props.rounded) {
    case 'none':
      break
    case 'sm':
      classes.push('rounded-sm')
      break
    case 'md':
      classes.push('rounded-md')
      break
    case 'lg':
      classes.push('rounded-lg')
      break
  }
  
  // Border
  if (props.border) {
    classes.push('bordered')
  }
  
  return classes
})

const bodyClasses = computed(() => {
  const classes = []
  
  // Padding
  switch (props.padding) {
    case 'none':
      classes.push('p-0')
      break
    case 'sm':
      classes.push('p-sm')
      break
    case 'md':
      classes.push('p-md')
      break
    case 'lg':
      classes.push('p-lg')
      break
  }
  
  return classes
})
</script>

<style scoped>
.card {
  background: white;
  transition: all 0.2s ease;
}

.card.bordered {
  border: 1px solid #e5e7eb;
}

.card.rounded-sm {
  border-radius: 4px;
}

.card.rounded-md {
  border-radius: 8px;
}

.card.rounded-lg {
  border-radius: 12px;
}

.card.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.card.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.card.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.card-header {
  padding: 20px 24px 16px;
  border-bottom: 1px solid #f3f4f6;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.card-body {
  position: relative;
}

.card-body.p-0 {
  padding: 0;
}

.card-body.p-sm {
  padding: 12px;
}

.card-body.p-md {
  padding: 24px;
}

.card-body.p-lg {
  padding: 32px;
}

.card-footer {
  padding: 16px 24px 20px;
  border-top: 1px solid #f3f4f6;
  background: #f9fafb;
}
</style> 