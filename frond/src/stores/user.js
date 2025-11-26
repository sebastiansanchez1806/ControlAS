// src/stores/user.js
import { defineStore } from 'pinia';
import axios from 'axios';
import { API_BASE_URL } from '../config/api';
import { piniaPersistCookie } from '@/src/plugins/pinia-persist-cookie';
export const useUserStore = defineStore('user', {
  state: () => ({
    id: null,
    nombre: '',
    correo: '',
    tipo: '',
    telefono: '',
    imagen: null,
    isLoggedIn: false,
  }),

  actions: {
    setDueno(data) {
      this.id = data.id;
      this.nombre = data.nombre || '';
      this.correo = data.correo || '';
      this.tipo = data.tipo || '';
      this.telefono = data.telefono || '';
      this.imagen = data.imagen || null;
      this.isLoggedIn = true;
    },

    logout() {
      this.id = null;
      this.nombre = '';
      this.correo = '';
      this.tipo = '';
      this.telefono = '';
      this.imagen = null;
      this.isLoggedIn = false;
    },

    // === TUS ACCIONES QUEDAN EXACTAMENTE IGUALES ===
    async verifyPassword(password) {
      try {
        if (!this.id) throw new Error('ID de usuario no encontrado en el store.');
        const response = await axios.post(`${API_BASE_URL}/dueno/${this.id}/verify-password`, { password });
        return { success: true, message: response.data.message };
      } catch (error) {
        console.error('Error al verificar la contraseña:', error);
        return { success: false, message: error.response?.data?.detail || 'Error al verificar la contraseña.' };
      }
    },

    async updateUserData(updatedData) {
      try {
        const response = await axios.put(`${API_BASE_URL}/dueno/${this.id}`, updatedData);
        if (response.status === 200) {
          this.nombre = response.data.nombre;
          this.correo = response.data.correo;
          this.telefono = response.data.telefono;
          return { success: true, message: 'Datos actualizados con éxito.' };
        }
      } catch (error) {
        console.error('Error al actualizar los datos:', error);
        return { success: false, message: error.response?.data?.detail || 'Error al actualizar los datos.' };
      }
    },

    async updateUserPassword(passwordData) {
      try {
        const response = await axios.put(`${API_BASE_URL}/dueno/${this.id}/password`, passwordData);
        if (response.status === 200) {
          return { success: true, message: 'Contraseña actualizada con éxito.' };
        }
      } catch (error) {
        console.error('Error al actualizar la contraseña:', error);
        return { success: false, message: error.response?.data?.detail || 'Error al actualizar la contraseña.' };
      }
    },

    async updateUserPhoto(photoUrl) {
      try {
        const response = await axios.put(`${API_BASE_URL}/dueno/${this.id}/photo`, { photo_url: photoUrl });
        if (response.status === 200) {
          this.imagen = response.data.photoUrl;
          return { success: true, message: 'Imagen de perfil actualizada con éxito.' };
        }
      } catch (error) {
        console.error('Error al actualizar la foto:', error);
        return { success: false, message: error.response?.data?.detail || 'Error al actualizar la foto.' };
      }
    },
  },

  // ¡¡AQUÍ ESTÁ LA CLAVE: PERSISTS TODO EN COOKIES SEGURAS!!
  persist: {
    key: 'user_pinia',                    // nombre único en cookies
    storage: piniaPersistCookie.storage,  // ← usa tu plugin de cookies (NO localStorage)

    // SIN paths = persiste absolutamente TODO lo que hay en state
    // ¡¡EXACTAMENTE lo que pediste!!
  },
});