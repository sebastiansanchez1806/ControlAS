// stores/gestorPrincipal.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { piniaPersistCookie } from '@/src/plugins/pinia-persist-cookie'

export const useGestorPrincipalStore = defineStore('gestorPrincipal', () => {
  // Todo el estado se maneja con ref como antes
  const gestor = ref(null) // { id, nombre, correo, token, ... }

  const login = (data) => {
    gestor.value = data
    // ¡Ya no necesitas hacer nada manual! Pinia + cookie lo guarda automáticamente
  }

  const logout = () => {
    gestor.value = null
    // ¡También se borra automáticamente de la cookie!
  }

  const isLoggedIn = () => !!gestor.value

  // Bonus: función útil para verificar si hay sesión activa
  const hasSession = () => !!gestor.value

  return {
    gestor,
    login,
    logout,
    isLoggedIn,
    hasSession
  }
}, {
  // ¡¡AQUÍ ESTÁ LA MAGIA: PERSISTE TODO EN COOKIES SEGURAS!!
  persist: {
    key: 'gestor_principal',              // nombre único en cookies
    storage: piniaPersistCookie.storage,  // ← usa tu sistema de cookies (NO localStorage)

    // SIN paths → persiste TODO el estado (incluido el token si lo tienes dentro de gestor)
  },
})