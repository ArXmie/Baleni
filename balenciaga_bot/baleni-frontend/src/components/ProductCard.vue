<template>
  <router-link :to="{ name: 'product', params: { id: product.id } }" class="product-link">
    <div class="product">
      <img :src="imageSrc" :alt="product.name" />
      <div class="product-info">
        <b>{{ product.name }}</b>
        <div class="price">{{ product.price }}$</div>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  product: { type: Object, required: true },
})

const imageSrc = computed(() => {
  const img = props.product.images?.[0]?.image
  return img || '/static/Men-Track-Trail-Laces-Sneaker.webp'
})
</script>