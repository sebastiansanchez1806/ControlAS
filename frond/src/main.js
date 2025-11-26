import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
// 1. Importa el plugin de persistencia
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate' 

import App from './App.vue'
import router from './router/index'
// import Login from './components/login.vue' // No es necesario importarlo aquí si no lo usas directamente en main.js

const app = createApp(App)
const pinia = createPinia() // Crea la instancia de Pinia
app.config.devtools = false;
// 2. Usa el plugin con tu instancia de Pinia
pinia.use(piniaPluginPersistedstate)

app.use(pinia) // Usa la instancia de Pinia con el plugin
app.use(router)

app.mount('#app')
