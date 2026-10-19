<template>
  <button
    v-show="visible"
    class="scroll-top-btn"
    @click="scrollTop"
  >↑</button>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const visible = ref(false)

function onScroll() {
  visible.value = window.scrollY > 300
}
function scrollTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => window.addEventListener('scroll', onScroll))
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.scroll-top-btn {
  position: fixed;
  bottom: 120px;
  right: 24px;
  width: 44px;
  height: 44px;
  background: #fff;
  border: 1.2px solid #000;
  font-size: 20px;
  cursor: pointer;
  z-index: 1000;
}
</style>