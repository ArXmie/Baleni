<template>
  <div class="user-info" ref="rootEl">
    <span class="user-nickname">{{ auth.nickname }}</span>
    <img
      class="user-avatar"
      src="/static/default-avatar-icon-of-social-media-user-vector.jpg"
      alt="avatar"
      @click.stop="open = !open"
    />
    <div class="dropdown" :class="{ open }">
      <router-link to="#" @click.prevent>Профиль</router-link>
      <a href="#" @click.prevent="handleLogout">Выйти</a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const open = ref(false)
const rootEl = ref(null)

function handleLogout() {
  auth.logout()
  router.push({ name: 'login' })
}

function handleClickOutside(e) {
  if (rootEl.value && !rootEl.value.contains(e.target)) {
    open.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))
</script>