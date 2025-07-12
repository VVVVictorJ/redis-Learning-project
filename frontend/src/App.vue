<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <el-config-provider>
    <RouterView />
  </el-config-provider>
</template>

<style scoped>
#app {
  width: 100vw;
  height: 100vh;
  padding: 0;
  margin: 0;
}

/* Scoped styles can still be used, but we'll rely on Tailwind for most things. */
</style>
