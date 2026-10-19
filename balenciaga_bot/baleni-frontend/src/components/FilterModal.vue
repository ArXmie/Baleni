<template>
  <div v-if="visible" class="modal" style="display: block" @click.self="$emit('close')">
    <div class="modal-content">
      <p>Фильтры</p>
      <div style="margin-top: 15px">
        <label>Цена от:
          <input v-model.number="localPriceFrom" type="number" placeholder="0" />
        </label><br />
        <label>Цена до:
          <input v-model.number="localPriceTo" type="number" placeholder="100000000" />
        </label>
      </div>
      <button type="button" style="margin-top: 15px" @click="apply">Применить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: Boolean,
  priceFrom: [String, Number],
  priceTo: [String, Number],
})
const emit = defineEmits(['close', 'apply'])

const localPriceFrom = ref(props.priceFrom)
const localPriceTo = ref(props.priceTo)

watch(() => props.priceFrom, (v) => (localPriceFrom.value = v))
watch(() => props.priceTo, (v) => (localPriceTo.value = v))

function apply() {
  emit('apply', { priceFrom: localPriceFrom.value, priceTo: localPriceTo.value })
  emit('close')
}
</script>