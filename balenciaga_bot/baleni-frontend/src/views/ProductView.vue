<template>
  <main v-if="product" class="main-outline">
    <div class="path">
      <ul class="nav-list">
        <li><router-link class="catalog-text" :to="{ name: 'catalog' }">Каталог</router-link></li>
        <li>{{ product.category_name }}</li>
        <li>{{ product.name }}</li>
      </ul>
    </div>

    <div class="product-template">
      <div class="left-part">
        <div class="image-container">
          <img v-if="currentImage" :src="currentImage" class="image" />
          <div class="overlay">
            <div class="arrow-left" @click="prevImage">&lt;</div>
            <div class="dots">
              <div
                v-for="(img, i) in product.images"
                :key="img.id"
                class="dot"
                :class="{ 'dot-active': i === imageIndex }"
                @click="imageIndex = i"
              ></div>
            </div>
            <div class="arrow-right" @click="nextImage">&gt;</div>
          </div>
        </div>
      </div>

      <div class="right-part">
        <h2>{{ product.name }}</h2>
        <p v-html="formattedDesc"></p>
        <p class="price">{{ product.price }}$</p>

        <div class="size">
          <p>Размер:</p>
          <ul class="nav-list">
            <li
              v-for="s in product.sizes"
              :key="s"
              class="size-li"
              :class="{ selected: selectedSize === s }"
              @click="selectedSize = s"
            >{{ s }}</li>
            <p v-if="!product.sizes?.length">Нету размеров</p>
          </ul>
        </div>

        <div class="buy" @click="addToCart">
          <div class="buy-text">Положить в корзину</div>
          <img src="/static/cart.png" class="icon" width="35" height="35" />
        </div>
      </div>
    </div>

    <div class="similar">
      <div class="name"><h2>Похожие</h2></div>
      <div class="list">
        <router-link
          v-for="item in similar"
          :key="item.id"
          :to="{ name: 'product', params: { id: item.id } }"
        >
          <div class="product">
            <img :src="item.images?.[0]?.image" :alt="item.name" />
            <div class="product-info">
              <p>{{ item.name }}</p>
              <div class="price">{{ item.price }}$</div>
            </div>
          </div>
        </router-link>
        <p v-if="!similar.length" class="error-similar">Нет похожих товаров.</p>
      </div>
    </div>
  </main>

  <main v-else-if="loading" class="main-outline">
    <div class="loading">Загрузка...</div>
  </main>

  <main v-else class="main-outline">
    <div class="loading">Товар не найден</div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { productsApi } from '@/api'
import { useCartStore } from '@/stores/cart'
import { useProductHover } from '@/composables/useProductHover'
import { usePricePulse } from '@/composables/usePricePulse'

const route = useRoute()
const cart = useCartStore()

const product = ref(null)
const similar = ref([])
const loading = ref(true)
const imageIndex = ref(0)
const selectedSize = ref(null)

const currentImage = computed(() => {
  const img = product.value?.images?.[imageIndex.value]?.image
  return img ? `/${img}` : null
})

const formattedDesc = computed(() =>
  product.value?.desc?.replace(/\n/g, '<br>') || ''
)

function prevImage() {
  if (!product.value?.images?.length) return
  imageIndex.value =
    (imageIndex.value - 1 + product.value.images.length) % product.value.images.length
}
function nextImage() {
  if (!product.value?.images?.length) return
  imageIndex.value = (imageIndex.value + 1) % product.value.images.length
}

function addToCart() {
  if (!selectedSize.value && product.value?.sizes?.length) {
    alert('Выберите размер')
    return
  }
  cart.add(product.value, selectedSize.value, 1)
  alert('Товар добавлен в корзину')
}

async function loadProduct() {
  loading.value = true
  imageIndex.value = 0
  selectedSize.value = null

  try {
    const id = route.params.id
    const { data } = await productsApi.detail(id)
    product.value = data

    if (data.category) {
      const { data: all } = await productsApi.list({ category: data.category })
      similar.value = all.filter((p) => p.id !== data.id).slice(0, 3)
    }

    useProductHover()
    usePricePulse()
  } catch {
    product.value = null
  } finally {
    loading.value = false
  }
}

onMounted(loadProduct)
watch(() => route.params.id, loadProduct)
</script>