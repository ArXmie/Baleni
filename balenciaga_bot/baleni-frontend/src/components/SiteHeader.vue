<template>
  <div class="div-width">
    <img src="/static/balenciaga-banner.png" alt="banner" />
  </div>

  <header class="site-header">
    <div class="container">
      <div class="header-row">
        <div class="catalog">
          <router-link class="catalog-text" :to="{ name: 'catalog' }">
            Каталог
          </router-link>
        </div>

        <div class="logo">
          <img src="/static/logo.svg" alt="Логотип сайта" />
        </div>

        <div class="actions">
          <router-link :to="{ name: 'search' }" class="search">
            <img src="/static/search.png" height="34" />
          </router-link>

          <router-link :to="{ name: 'cart' }" class="cart-link">
            <img src="/static/cart.png" alt="Корзина" />
            <span v-if="cart.count" class="cart-count">{{ cart.count }}</span>
          </router-link>

          <UserMenu v-if="auth.isAuthenticated" />
          <router-link v-else class="login-text" :to="{ name: 'login' }">
            Войти
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { watch } from 'vue'
import { useCartStore } from '@/stores/cart'
import UserMenu from './UserMenu.vue'

const auth = useAuthStore()
const cart = useCartStore()

watch(
  () => auth.isAuthenticated,
  (logged) => {
    if (!logged) return cart.reset()
    cart.fetch().catch((e) => {
      if (e.response?.status === 401) auth.logout()
    })
  },
  { immediate: true }
)
</script>