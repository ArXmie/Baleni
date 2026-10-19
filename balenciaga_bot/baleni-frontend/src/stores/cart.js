import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])

  const total = computed(() =>
    items.value.reduce((sum, i) => sum + Number(i.price) * i.amount, 0)
  )

  function add(product, size, amount = 1) {
    const existing = items.value.find(
      (i) => i.productId === product.id && i.size === size
    )
    if (existing) existing.amount += amount
    else items.value.push({
      productId: product.id,
      name: product.name,
      price: product.price,
      size,
      amount,
    })
  }

  function remove(productId, size) {
    items.value = items.value.filter(
      (i) => !(i.productId === productId && i.size === size)
    )
  }

  function clear() {
    items.value = []
  }

  return { items, total, add, remove, clear }
})