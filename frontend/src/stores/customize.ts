import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { BassOption, OrderItem } from '@/types'

export const useCustomizeStore = defineStore('customize', () => {
  const selections = ref<Record<string, BassOption>>({})
  const basePrice = 5000

  const totalPrice = computed(() => {
    let total = basePrice
    for (const opt of Object.values(selections.value)) {
      total += opt.price
    }
    return total
  })

  const selectedCount = computed(() => Object.keys(selections.value).length)

  const configuration = computed<OrderItem[]>(() => {
    return Object.entries(selections.value).map(([category, option]) => ({
      option_id: option.id,
      category,
      name: option.name,
      price: option.price,
    }))
  })

  function selectOption(category: string, option: BassOption) {
    selections.value = {
      ...selections.value,
      [category]: option,
    }
  }

  function clearSelection(category: string) {
    const newSelections = { ...selections.value }
    delete newSelections[category]
    selections.value = newSelections
  }

  function resetAll() {
    selections.value = {}
  }

  return {
    selections,
    basePrice,
    totalPrice,
    selectedCount,
    configuration,
    selectOption,
    clearSelection,
    resetAll,
  }
})
