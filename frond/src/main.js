import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

// === PINIA PERSISTENCE ===
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

// === TOASTIFICATION (para notificaciones en tiempo real) ===
import Toast from "vue-toastification"
import "vue-toastification/dist/index.css"

import App from './App.vue'
import router from './router/index'

const app = createApp(App)

// === CONFIGURACIÓN GLOBAL ===
app.config.devtools = false // Desactivas las devtools como querías

// === PINIA ===
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate) // ← Activa la persistencia en todos tus stores
app.use(pinia)

// === ROUTER ===
app.use(router)

// === TOASTIFICATION (configuración bonita y funcional) ===
app.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 5,
  newestOnTop: true,
  position: "top-right",
  timeout: 4000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
  rtl: false
})

app.mount('#app')