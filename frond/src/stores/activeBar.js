// src/stores/activeBar.js
import { defineStore } from 'pinia'; 
import { piniaPersistCookie } from '@/src/plugins/pinia-persist-cookie';
export const useActiveBarStore = defineStore('activeBar', {
  state: () => ({
    id: null,
    name: '',
    location: '',
    image: '',
  }),

  actions: {
    setBar(barData) {
      this.id = barData.id ?? null;
      this.name = barData.name ?? '';
      this.location = barData.location ?? '';
      this.image = barData.image ?? '';
    },

    clearBar() {
      this.id = null;
      this.name = '';
      this.location = '';
      this.image = '';
      // Gracias al persist con cookies, también se borra automáticamente de la cookie
    }
  },

  // PERSISTE TODO EN COOKIES SEGURAS (nunca más localStorage)
  persist: {
    key: 'activeBar_pinia',               // nombre único en cookies
    storage: piniaPersistCookie.storage,  // tu sistema de cookies seguro

    // SIN paths → guarda TODO: id, name, location, image
    // Al recargar la página, el bar seleccionado sigue activo
  },
});