<template>
  <router-view v-if="standalone" />
  <div v-else class="app-layout">
    <SiteHeader />
    <router-view />
    <footer class="footer-1"></footer>
    <ScrollTopButton />
    <ViewCounter />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SiteHeader from '@/components/SiteHeader.vue'
import ScrollTopButton from '@/components/ScrollTopButton.vue'
import ViewCounter from '@/components/ViewCounter.vue'

const route = useRoute()
const standalone = computed(() => !!route.meta.standalone)
</script>
