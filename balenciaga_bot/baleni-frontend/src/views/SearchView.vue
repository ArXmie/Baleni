<template>
  <main class="main-outline">
    <h1 class="page-title">ПОИСК</h1>

    <div v-if="query" class="search-info">
      <p v-if="count > 0">Найдено товаров: <strong>{{ count }}</strong></p>
      <p v-else>По запросу "<strong>{{ query }}</strong>" ничего не найдено</p>
    </div>

    <div class="search-section">
      <div class="search-box">
        <input
          v-model="query"
          type="text"
          placeholder="Поиск"
          @keyup.enter="performSearch"
        />
        <button class="search-button" @click="performSearch">
          <img src="/static/search2.png" height="20" />
        </button>
      </div>
      <div class="filter">
        <button class="filter-btn" @click="showFilter = true">
          <img src="/static/filter.png" height="20" />
        </button>
      </div>
    </div>

    <FilterModal
      :visible="showFilter"
      :price-from="priceFrom"
      :price-to="priceTo"
      @close="showFilter = false"
      @apply="onApplyFilters"
    />

    <div class="objects">
      <template v-if="products.length">
        <router-link
          v-for="p in products"
          :key="p.id"
          :to="{ name: 'product', params: { id: p.id } }"
        >
          <button type="button" class="object-btn">
            <div class="object">
              <div class="object-info">
                <img
                  class="object-img"
                  :src="p.images?.[0]?.image || '/static/Men-Track-Trail-Laces-Sneaker.webp'"
                  :alt="p.name"
                />
                <div class="object-name">{{ p.name }}</div>
              </div>
              <div class="flex-price">
                <div class="price">{{ p.price }}$</div>
              </div>
            </div>
          </button>
        </router-link>
      </template>
      <p v-else-if="query">По запросу "{{ query }}" товары не найдены</p>
      <p v-else>Введите запрос для поиска товаров</p>
    </div>
  </main>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productsApi } from '@/api'
import FilterModal from '@/components/FilterModal.vue'
import { usePricePulse } from '@/composables/usePricePulse'

const route = useRoute()
const router = useRouter()

const query = ref(route.query.q || '')
const priceFrom = ref(route.query.price_from || '')
const priceTo = ref(route.query.price_to || '')
const products = ref([])
const count = ref(0)
const showFilter = ref(false)

async function fetchProducts() {
  const params = {}
  if (query.value) params.search = query.value
  if (priceFrom.value) params.price__gte = priceFrom.value
  if (priceTo.value) params.price__lte = priceTo.value

  const { data } = await productsApi.list(params)
  products.value = data
  count.value = data.length
  usePricePulse()
}

function performSearch() {
  if (!query.value.trim()) {
    alert('Введите запрос для поиска')
    return
  }
  router.push({ name: 'search', query: {
    q: query.value,
    price_from: priceFrom.value || undefined,
    price_to: priceTo.value || undefined,
  }})
}

function onApplyFilters({ priceFrom: pf, priceTo: pt }) {
  priceFrom.value = pf
  priceTo.value = pt
  performSearch()
}

onMounted(fetchProducts)
watch(() => route.query, (q) => {
  query.value = q.q || ''
  priceFrom.value = q.price_from || ''
  priceTo.value = q.price_to || ''
  fetchProducts()
})
</script>