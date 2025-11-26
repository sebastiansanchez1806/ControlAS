// stores/counter.js (o donde lo tengas)
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { piniaPersistCookie } from '@/plugins/pinia-persist-cookie' // Ajusta la ruta si necesario

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)

  const doubleCount = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function decrement() {
    count.value--
  }

  function reset() {
    count.value = 0
  }

  return { 
    count, 
    doubleCount, 
    increment, 
    decrement, 
    reset 
  }
}, {
  // PERSISTE TODO EN COOKIES SEGURAS (nunca más en localStorage)
  persist: {
    key: 'counter_pinia',                 // nombre único en cookies
    storage: piniaPersistCookie.storage,  // usa tu sistema de cookies

    // SIN paths = persiste TODO (en este caso solo "count")
    // Al recargar la página, el contador mantiene su valor
  },
})