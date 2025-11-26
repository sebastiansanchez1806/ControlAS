// src/plugins/pinia-persist-cookie.js
import Cookies from 'js-cookie'

export const piniaPersistCookie = {
  key: 'pinia',

  /**
   * CONFIGURACIÓN PERFECTA Y DEFINITIVA
   * → En desarrollo (vite serve): secure = false → funciona en cualquier IP local
   * → En producción (vite build + HTTPS): secure = true + SameSite=None → seguro y correcto
   */
  get cookieOptions() {
    const isProduction = import.meta.env.PROD

    return {
      expires: 30,                  // 30 días de duración
      path: '/',
      secure: isProduction,         // ← FALSE en desarrollo → SOLUCIONA TU PROBLEMA
      sameSite: isProduction ? 'None' : 'Lax'  // Lax en dev, None en prod (obligatorio con secure)
    }
  },

  storage: {
    // Leer cookie
    getItem: (key) => {
      const value = Cookies.get(key)
      if (!value) return null
      try {
        return JSON.parse(value)
      } catch (err) {
        console.warn(`[pinia-persist-cookie] Error al parsear la cookie "${key}"`, err)
        return null
      }
    },

    // Guardar cookie
    setItem: (key, value) => {
      Cookies.set(key, JSON.stringify(value), piniaPersistCookie.cookieOptions)
    },

    // Eliminar cookie
    removeItem: (key) => {
      Cookies.remove(key, { path: '/' })
    }
  }
}