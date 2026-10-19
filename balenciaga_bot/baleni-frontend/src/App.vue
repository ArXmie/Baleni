<template>
  <div class="app-layout">
    <SiteHeader />
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
    <footer class="footer-1"></footer>
    <ScrollTopButton />
    <ViewCounter />
  </div>
</template>

<script setup>
import SiteHeader from '@/components/SiteHeader.vue'
import ScrollTopButton from '@/components/ScrollTopButton.vue'
import ViewCounter from '@/components/ViewCounter.vue'
</script>