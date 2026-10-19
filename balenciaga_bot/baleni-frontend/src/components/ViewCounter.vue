<template>
  <div class="view-counter">ПРОСМОТРОВ ЗА СЕССИЮ: {{ count }}</div>
</template>

<script setup>
import { ref } from 'vue'

const key = 'balenciaga_views'
const count = ref(parseInt(sessionStorage.getItem(key) || '0', 10) + 1)
sessionStorage.setItem(key, count.value)
</script>

<style scoped>
.view-counter {
  text-align: center;
  padding: 10px 0 6px;
  font-size: 12px;
  letter-spacing: 2px;
  color: #aaa;
}
</style>