import { defineStore } from 'pinia'
import { ref } from 'vue'
import { cartApi } from '@/api'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const total = ref('0')
  const count = ref(0)

  function apply(data) {
    items.value = data.items
    total.value = data.total
    count.value = data.count
  }

  function reset() {
    apply({ items: [], total: '0', count: 0 })
  }

  async function fetch() {
    const { data } = await cartApi.get()
    apply(data)
  }

  async function add(product, size, amount = 1) {
    const { data } = await cartApi.add({ product: product.id, size, amount })
    apply(data)
  }

  async function setAmount(id, amount) {
    const { data } = await cartApi.setAmount(id, amount)
    apply(data)
  }

  async function remove(id) {
    const { data } = await cartApi.remove(id)
    apply(data)
  }

  async function clear() {
    const { data } = await cartApi.clear()
    apply(data)
  }

  return { items, total, count, fetch, reset, add, setAmount, remove, clear }
})
