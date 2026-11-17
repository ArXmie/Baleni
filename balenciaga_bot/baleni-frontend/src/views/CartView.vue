<template>
  <main class="main-outline">
    <div class="path">
      <ul class="nav-list">
        <li><router-link class="catalog-text" :to="{ name: 'catalog' }">Каталог</router-link></li>
        <li>Корзина</li>
      </ul>
    </div>

    <div class="cart">
      <h2>Корзина</h2>

      <p v-if="!cart.items.length" class="cart-empty">Корзина пуста.</p>

      <template v-else>
        <div
          v-for="item in cart.items"
          :key="item.id"
          class="cart-item"
        >
          <router-link :to="{ name: 'product', params: { id: item.product } }">
            <img v-if="item.image" :src="imageSrc(item.image)" :alt="item.name" class="cart-img" />
          </router-link>

          <div class="cart-info">
            <b>{{ item.name }}</b>
            <p class="cart-size">Размер: <span class="cart-size-value">{{ item.size || '' }}</span></p>
            <div class="cart-price">{{ item.price }}$</div>
          </div>

          <div class="cart-amount">
            <div class="cart-btn" @click="cart.setAmount(item.id, item.amount - 1)">−</div>
            <div class="cart-num">{{ item.amount }}</div>
            <div class="cart-btn" @click="cart.setAmount(item.id, item.amount + 1)">+</div>
          </div>

          <div class="cart-remove" @click="cart.remove(item.id)">Удалить</div>
        </div>

        <div class="cart-total">
          <span>Итого:</span>
          <span class="cart-total-price">{{ Number(cart.total).toFixed(2) }}$</span>
        </div>

        <div class="cart-actions">
          <div class="buy" @click="cart.clear()">
            <div class="buy-text">Очистить корзину</div>
          </div>
        </div>
      </template>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()

onMounted(() => cart.fetch())

function imageSrc(img) {
  return `/${img}`
}
</script>
