// stores/admin.js
import { defineStore } from 'pinia';
import { piniaPersistCookie } from '@/src/plugins/pinia-persist-cookie';
export const useAdminStore = defineStore('admin', {
  state: () => ({
    id: null,
    nombre: '',
    telefono: '',
    foto: null,
    bar_id: null,
    dueno_id: null,
    bar_nombre: '',
  }),

  actions: {
    setAdmin(data) {
      this.id = data.id;
      this.nombre = data.nombre || '';
      this.telefono = data.telefono || '';
      this.foto = data.foto || null;
      this.bar_id = data.bar_id || null;
      this.dueno_id = data.dueno_id || null;
      this.bar_nombre = data.bar_nombre || '';
    },

    logout() {
      this.id = null;
      this.nombre = '';
      this.telefono = '';
      this.foto = null;
      this.bar_id = null;
      this.dueno_id = null;
      this.bar_nombre = '';
      // La cookie se borra automáticamente gracias al persist
    }
  },

  // PERSISTE TODO EN COOKIES SEGURAS (como el resto de tus stores)
  persist: {
    key: 'admin_pinia',                   // nombre único en cookies
    storage: piniaPersistCookie.storage,  // tu sistema de cookies seguro

    // SIN paths → guarda absolutamente TODO: id, nombre, teléfono, foto, bar_id, dueno_id, bar_nombre
    // Al recargar la página, el admin sigue logueado con todos sus datos
  },
});