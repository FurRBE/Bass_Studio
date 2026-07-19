<template>
  <DefaultLayout>
    <div class="not-found-page">
      <h1>404</h1>
      <p>页面不存在</p>
      <router-link to="/">
        <el-button type="primary">返回首页</el-button>
      </router-link>
    </div>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue'
</script>

<style scoped lang="scss">
.not-found-page {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  background: var(--bg-primary);

  h1 {
    font-size: 6rem;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: 8px;
  }

  p {
    color: var(--text-muted);
    font-size: 1.1rem;
    margin-bottom: 16px;
  }
}
</style>
