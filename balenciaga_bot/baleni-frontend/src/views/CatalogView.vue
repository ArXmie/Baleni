<template>
  <main class="main-outline">
    <h1 class="page-title">КАТАЛОГ</h1>

    <div v-if="loading" class="loading">Загрузка...</div>

    <div v-else class="catalog-list">
      <div v-for="group in catalog" :key="group.category.id" class="catalog-category">
        <div class="catalog-name">{{ group.category.category }}</div>
        <div class="products">
          <ProductCard
            v-for="product in group.products"
            :key="product.id"
            :product="product"
          />
        </div>
        <div class="arrow">
          <img src="/static/arrow.png" alt=">" />
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { categoriesApi, productsApi } from '@/api'
import ProductCard from '@/components/ProductCard.vue'
import { useProductHover } from '@/composables/useProductHover'
import { usePricePulse } from '@/composables/usePricePulse'

const catalog = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data: categories } = await categoriesApi.list()
    const { data: products } = await productsApi.list()

    catalog.value = categories.map((cat) => ({
      category: cat,
      products: products.filter((p) => p.category === cat.id).slice(0, 2),
    }))
  } finally {
    loading.value = false
    useProductHover()
    usePricePulse()
  }
})
</script>