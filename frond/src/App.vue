<template>
  <router-view />
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { useAdminStore } from '@/stores/admin'
import { useActiveBarStore } from '@/stores/activeBar'
import { useToast } from 'vue-toastification' // ← Asumiendo que usas vue-toastification (recomendado)
import axios from 'axios'

// Stores
const userStore = useUserStore()
const adminStore = useAdminStore()
const activeBarStore = useActiveBarStore()
const toast = useToast()

// Variable para el WebSocket
let socket = null

// Función para conectar el WebSocket
const connectWebSocket = () => {
  if (!activeBarStore.id) return // No hay bar activo → no conectar

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const wsUrl = `${protocol}//${window.location.host}/api/ws/${activeBarStore.id}`

  socket = new WebSocket(wsUrl)

  socket.onopen = () => {
    console.log('✅ WebSocket conectado al bar:', activeBarStore.id)
  }

  socket.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      handleWebSocketMessage(msg)
    } catch (err) {
      console.error('Error parseando mensaje WS:', err)
    }
  }

  socket.onclose = () => {
    console.log('🔌 WebSocket cerrado')
    // Intentar reconectar en 3 segundos si sigue habiendo bar activo
    setTimeout(() => {
      if (activeBarStore.id && (userStore.isLoggedIn || adminStore.bar_id)) {
        connectWebSocket()
      }
    }, 3000)
  }

  socket.onerror = (error) => {
    console.error('Error en WebSocket:', error)
  }
}

// Función central para manejar todos los eventos
const handleWebSocketMessage = (msg) => {
  console.log('📨 Mensaje recibido:', msg.type, msg.data)

  switch (msg.type) {
    // === FACTURAS ===
    case 'nueva_factura':
      toast.success(`🧾 Nueva factura: $${msg.data.total_neto.toLocaleString()} por ${msg.data.admin_nombre}`)
      // Aquí puedes emitir un evento global o recargar facturas
      // Ejemplo: window.location.reload() o usar un event bus
      break

    // === PRODUCTOS ===
    case 'producto_creado':
      toast.success(`✅ Nuevo producto: ${msg.data.nombre}`)
      break

    case 'producto_actualizado':
      toast.info(`✏️ Producto actualizado: ${msg.data.nombre}`)
      break

    case 'producto_eliminado':
      toast.warning(`🗑️ Producto eliminado: ${msg.data.nombre}`)
      break

    // === INVENTARIO ===
    case 'inventario_actualizado':
      const nuevos = msg.data.total_nuevos
      const aumentos = msg.data.total_aumentos
      let texto = ''
      if (nuevos > 0) texto += `${nuevos} nuevo${nuevos > 1 ? 's' : ''} producto${nuevos > 1 ? 's' : ''}`
      if (aumentos > 0) {
        texto += texto ? ' y ' : ''
        texto += `${aumentos} aumento${aumentos > 1 ? 's' : ''} de stock`
      }
      toast.success(`📦 Inventario actualizado: ${texto}`)
      break

    // === TAREAS ===
    case 'nueva_tarea':
      toast.info(`📌 Nueva tarea asignada`)
      break

    case 'tarea_completada':
      toast.success(`✅ Tarea completada`)
      break

    case 'tarea_eliminada':
      toast.warning(`🗑️ Tarea eliminada`)
      break

    // === ADMINISTRADORES ===
    case 'administrador_creado':
      toast.success(`👤 Nuevo administrador: ${msg.data.nombre}`)
      break

    case 'administrador_actualizado':
      toast.info(`✏️ Administrador actualizado: ${msg.data.nombre}`)
      break

    case 'administrador_eliminado':
      toast.warning(`🗑️ Administrador eliminado: ${msg.data.nombre}`)
      break

    // === DUEÑO ===
    case 'dueno_actualizado':
    case 'dueno_foto_actualizada':
      if (userStore.tipo === 'dueno') {
        userStore.nombre = msg.data.nombre || userStore.nombre
        userStore.telefono = msg.data.telefono || userStore.telefono
        userStore.correo = msg.data.correo || userStore.correo
        if (msg.data.imagen) userStore.imagen = msg.data.imagen
        toast.success('👤 Tus datos han sido actualizados')
      }
      break

    // === BAR ===
    case 'bar_eliminado':
      toast.error(`❌ El bar "${msg.data.nombre}" ha sido eliminado`)
      // Redirigir o cerrar sesión
      activeBarStore.clearBar()
      socket?.close()
      // router.push('/login') si quieres
      break

    case 'bar_actualizado':
      // Actualizar datos del bar activo si coincide
      if (activeBarStore.id === msg.data.id) {
        activeBarStore.setBar(msg.data)
      }
      break

    case 'nuevo_bar_creado':
      toast.success(`🏪 Nuevo bar creado: ${msg.data.nombre}`)
      break

    // === OTROS ===
    case 'historial_eliminado':
      toast.info(`📜 Historial limpiado`)
      break

    case 'limpieza_masiva_completada':
      toast.warning(`🧹 Limpieza completa realizada en el bar`)
      break

    default:
      console.log('Evento no manejado:', msg.type)
  }

  // Opcional: emitir evento global para que otros componentes reaccionen
  // window.dispatchEvent(new CustomEvent('ws-message', { detail: msg }))
}

// Observamos cambios en el bar activo o login
watch(
  () => activeBarStore.id,
  (newBarId, oldBarId) => {
    if (socket) {
      socket.close()
      socket = null
    }
    if (newBarId && (userStore.isLoggedIn || adminStore.bar_id)) {
      connectWebSocket()
    }
  }
)

// Al montar la app
onMounted(() => {
  // Si ya hay sesión y bar activo al cargar
  if (activeBarStore.id && (userStore.isLoggedIn || adminStore.bar_id)) {
    connectWebSocket()
  }
})

// Al desmontar (cerrar pestaña/navegador)
onUnmounted(() => {
  if (socket) {
    socket.close()
  }
})
</script>

<style>
/* Tus estilos globales aquí si quieres */
</style>