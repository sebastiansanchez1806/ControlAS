<template>
  <div class="invoices-container">
    <div class="header">
      <h1>📋 Historial de Movimientos</h1>
      <p class="subtitle">Se elimina el primer día de cada mes a las 3:00 a.m.</p>
    </div>

    <!-- BUSCADOR -->
    <div class="search-section">
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por ID de factura o fecha (YYYY-MM-DD)..."
          class="search-input"
          @input="filtrarFacturas"
        />
        <span class="search-icon">🔍</span>
      </div>
      <div v-if="searchQuery" class="search-results-info">
        Mostrando {{ facturasFiltradas.length }} de {{ facturas.length }} facturas
      </div>
    </div>

    <div v-if="loading" class="loader-container">
      <div class="spinner"></div>
      <p>Cargando facturas...</p>
    </div>

    <div v-else-if="(searchQuery ? facturasFiltradas : facturas).length === 0" class="empty-state">
      <div class="empty-icon">📭</div>
      <h3>{{ searchQuery ? 'Sin resultados' : 'No hay facturas registradas' }}</h3>
      <p>{{ searchQuery ? 'Intenta con otra búsqueda' : 'Aún no se han registrado movimientos de inventario' }}</p>
    </div>

    <div v-else class="facturas-list">
      <div
        v-for="factura in (searchQuery ? facturasFiltradas : facturas)"
        :key="factura.id"
        class="factura-card"
        @click="verDetalle(factura)"
      >
        <div class="factura-header">
          <div class="factura-info">
            <h3 class="factura-id">#{{ factura.id }}</h3>
            <span :class="['tipo-badge', getTipoBadgeClass(factura.tipo_operacion)]">
              {{ getTipoLabel(factura.tipo_operacion) }}
            </span>
          </div>
          <div class="factura-fecha">
           <span class="fecha">{{ formatSoloFecha(factura.fecha) }}</span>
          </div>
        </div>

        <div class="factura-body">
          <div class="usuario-info">
            <span class="icon">👤</span>
            <span>{{ factura.usuario_nombre || 'Usuario desconocido' }}</span>
          </div>

          <div class="resumen-movimientos">
            <div v-if="factura.total_aumentos > 0" class="movimiento-item aumentos">
              <span class="icon">📈</span>
              <span>{{ factura.total_aumentos }} productos con aumento</span>
            </div>
            <div v-if="factura.total_nuevos > 0" class="movimiento-item nuevos">
              <span class="icon">📦</span>
              <span>{{ factura.total_nuevos }} productos nuevos agregados</span>
            </div>
          </div>

          <div class="factura-footer">
            <span v-if="factura.tiene_factura" class="factura-adjunta">
              📎 Factura adjunta
            </span>
            <button class="btn-ver-detalle">Ver Detalle →</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loadingMore && facturas.length > 0" class="loader-more">
      <div class="spinner small"></div>
      <p>Cargando más facturas...</p>
    </div>

    <div v-if="!hasMore && facturas.length > 0" class="end-message">
      <p>¡Eso es todo! No hay más movimientos.</p>
    </div>

    <!-- MODAL DETALLE -->
    <div v-if="facturaSeleccionada" class="modal-overlay" @click.self="cerrarDetalle">
      <div class="modal-detalle">
        <button class="btn-close" @click="cerrarDetalle">×</button>

        <div class="detalle-header">
          <h2>Factura #{{ facturaSeleccionada.id }}</h2>
          <span :class="['tipo-badge', getTipoBadgeClass(facturaSeleccionada.tipo_operacion)]">
            {{ getTipoLabel(facturaSeleccionada.tipo_operacion) }}
          </span>
        </div>

        <div class="detalle-info">
          <div class="info-row">
            <span class="label">📅 Fecha:</span>
            <span class="value">{{ formatSoloFecha(facturaSeleccionada.fecha) }}</span> 
          </div>
          <div class="info-row">
            <span class="label">👤 Registrado por:</span>
            <span class="value">{{ facturaSeleccionada.usuario_nombre || 'Usuario desconocido' }}</span>
          </div>
        </div>

        <div v-if="detallesAumentos.length > 0" class="seccion-detalle">
          <h3 class="seccion-title">📈 Aumentos ({{ detallesAumentos.length }})</h3>
          <div class="productos-detalle-scroll">
            <div v-for="detalle in detallesAumentos" :key="detalle.id" class="producto-detalle-item">
              <div class="producto-imagen-container">
                <img
                  :src="detalle.imagen_producto || 'https://via.placeholder.com/60'"
                  :alt="detalle.nombre_producto"
                  class="producto-imagen"
                  @error="handleImageError"
                  @click.stop="verPreviewImagen(detalle.imagen_producto)"
                />
                <span class="preview-badge">👁️</span>
              </div>
              <div class="producto-info-detalle">
                <h4>{{ detalle.nombre_producto }}</h4>
                <div class="cantidad-info">
                  <span class="cantidad-badge aumento">+{{ detalle.cantidad }}</span>
                  <span class="cantidad-text">unidades agregadas</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="detallesNuevos.length > 0" class="seccion-detalle">
          <h3 class="seccion-title">📦 Productos Nuevos ({{ detallesNuevos.length }})</h3>
          <div class="productos-detalle-scroll">
            <div v-for="detalle in detallesNuevos" :key="detalle.id" class="producto-detalle-item nuevo">
              <div class="producto-imagen-container">
                <img
                  :src="detalle.imagen_producto || 'https://via.placeholder.com/60'"
                  :alt="detalle.nombre_producto"
                  class="producto-imagen"
                  @error="handleImageError"
                  @click.stop="verPreviewImagen(detalle.imagen_producto)"
                />
              </div>
              <div class="producto-info-detalle">
                <h4>{{ detalle.nombre_producto }}</h4>
                <div class="producto-specs">
                  <span class="spec">💰 {{ formatPrice(detalle.precio_unitario) }}</span>
                  <span class="spec">📊 inicial: {{ detalle.cantidad }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="facturaSeleccionada.tiene_factura" class="seccion-factura">
          <h3 class="seccion-title">📎 Factura Adjunta</h3>
          <div class="factura-adjunta-container">
            <div class="archivo-info">
              <span class="archivo-icon">📄</span>
              <div class="archivo-datos">
                <span class="archivo-nombre">{{ facturaSeleccionada.nombre_archivo }}</span>
                <span class="archivo-tipo">{{ facturaSeleccionada.mime_type }}</span>
              </div>
            </div>
            <button @click="descargarFactura" class="btn-descargar">
              ⬇️ Descargar
            </button>
          </div>
        </div>

        <div v-if="facturaSeleccionada.observaciones" class="seccion-observaciones">
          <h3 class="seccion-title">📝 Observaciones</h3>
          <p>{{ facturaSeleccionada.observaciones }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useActiveBarStore } from '@/stores/activeBar'
import { API_BASE_URL } from '../config/api'

// === NUEVO: Importamos date-fns para manejar fechas y horas correctamente ===
import { format, parseISO } from 'date-fns'
import { es } from 'date-fns/locale'

const emit = defineEmits(['navigate-out'])
const activeBarStore = useActiveBarStore()

// Estado
const loading = ref(true)
const loadingMore = ref(false)
const facturas = ref([])
const facturaSeleccionada = ref(null)
const detallesAumentos = ref([])
const detallesNuevos = ref([])
const hasMore = ref(true)
const lastId = ref(null)

// Búsqueda
const searchQuery = ref('')
const facturasFiltradas = computed(() => {
  if (!searchQuery.value) return facturas.value

  const query = searchQuery.value.toLowerCase()
  return facturas.value.filter(f => {
    const idMatch = f.id.toString().includes(query)
    const fechaMatch = f.fecha.includes(query)
    return idMatch || fechaMatch
  })
})
function formatSoloFecha(fechaISO) {
  if (!fechaISO) return 'Fecha no disponible'

  try {
    // parseISO espera formato ISO completo, pero funciona bien con solo fecha
    const date = parseISO(fechaISO)

    if (isNaN(date.getTime())) {
      return 'Fecha inválida'
    }

    // Formato deseado: 6 enero 2026   ó   06 ene 2026   (elige el que prefieras)
    return format(date, "d 'de' MMMM yyyy", { locale: es })
    // Alternativas populares:
    // "dd/MM/yyyy"          → 06/01/2026
    // "d MMMM yyyy"         → 6 enero 2026
    // "dd 'de' MMMM 'de' yyyy" → 06 de enero de 2026
  } catch (error) {
    console.error('Error formateando fecha:', error, { fechaISO })
    return 'Fecha inválida'
  }
}

onMounted(async () => {
  console.log('Bar ID del store:', activeBarStore.id)

  if (!activeBarStore.id) {
    console.error('No hay bar seleccionado en el store')
    alert('Error: No se detectó el bar. Por favor selecciona un bar primero.')
    loading.value = false
    return
  }

  await cargarFacturas()
  agregarScrollListener()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const handleScroll = () => {
  if (loadingMore.value || !hasMore.value || loading.value) return

  const cercaDelFinal =
    window.innerHeight + window.scrollY >= document.body.offsetHeight - 1200

  if (cercaDelFinal) {
    cargarFacturas()
  }
}

const agregarScrollListener = () => {
  window.addEventListener('scroll', handleScroll)
}

async function cargarFacturas() {
  if (!hasMore.value || loadingMore.value) return

  if (facturas.value.length === 0) {
    loading.value = true
  } else {
    loadingMore.value = true
  }

  try {
    console.log('Cargando facturas... lastId:', lastId.value)

    let url = `${API_BASE_URL}/inventario/facturas/${activeBarStore.id}?limit=20`
    if (lastId.value !== null) {
      url += `&last_id=${lastId.value}`
    }

    const res = await fetch(url)

    if (!res.ok) {
      const errorText = await res.text()
      console.error('Error del servidor:', errorText)
      throw new Error('Error al cargar facturas')
    }

    const data = await res.json()
    console.log('Facturas recibidas:', data.length)

    if (data.length === 0) {
      hasMore.value = false
      return
    }

    facturas.value.push(...data)
    lastId.value = data[data.length - 1].id

    if (data.length < 20) {
      hasMore.value = false
    }
  } catch (error) {
    console.error('Error cargando facturas:', error)
    alert('No se pudieron cargar más facturas')
  } finally {
    loading.value = false
    loadingMore.value = false
    await nextTick()
  }
}

function filtrarFacturas() {
  console.log('Filtrando por:', searchQuery.value)
}

async function verDetalle(factura) {
  facturaSeleccionada.value = factura
  await cargarDetalles(factura.id)
}

async function cargarDetalles(facturaId) {
  try {
    console.log('Cargando detalles de factura:', facturaId)

    const res = await fetch(`${API_BASE_URL}/inventario/factura/${facturaId}/detalles`)

    if (!res.ok) {
      const errorText = await res.text()
      console.error('Error cargando detalles:', errorText)
      throw new Error('Error al cargar detalles')
    }

    const data = await res.json()
    console.log('Detalles recibidos:', data.length, 'productos')

    detallesAumentos.value = data.filter(d => !d.es_nuevo_producto)
    detallesNuevos.value = data.filter(d => d.es_nuevo_producto)

  } catch (error) {
    console.error('Error cargando detalles:', error)
    alert('No se pudieron cargar los detalles de la factura')
  }
}

function cerrarDetalle() {
  facturaSeleccionada.value = null
  detallesAumentos.value = []
  detallesNuevos.value = []
}

async function descargarFactura() {
  try {
    console.log('Descargando factura:', facturaSeleccionada.value.id)

    const res = await fetch(`${API_BASE_URL}/inventario/factura/${facturaSeleccionada.value.id}/descargar`)

    if (!res.ok) {
      const errorText = await res.text()
      console.error('Error descargando:', errorText)
      throw new Error('Error al descargar')
    }

    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = facturaSeleccionada.value.nombre_archivo || 'factura.pdf'
    document.body.appendChild(a)
    a.click()
    window.URL.revokeObjectURL(url)
    document.body.removeChild(a)

    console.log('Factura descargada exitosamente')
  } catch (error) {
    console.error('Error descargando factura:', error)
    alert('No se pudo descargar la factura')
  }
}

function handleImageError(e) {
  console.warn('Error cargando imagen, usando placeholder')
  e.target.src = 'https://via.placeholder.com/60?text=Sin+Imagen'
}

// === FUNCIÓN CORREGIDA CON date-fns (100% confiable para Colombia) ===
function formatDateTime(fechaISO, horaString) {
  if (!fechaISO) return 'Fecha no disponible'

  try {
    let fullIsoString

    if (horaString && typeof horaString === 'string') {
      // Ejemplo: horaString = "11:32 PM" o "03:30 AM"
      const horaLimpia = horaString.trim().toUpperCase()

      const ampmMatch = horaLimpia.match(/(AM|PM)$/)
      let horaBase = ampmMatch ? horaLimpia.replace(/(AM|PM)$/, '').trim() : horaLimpia

      // Añadir segundos si faltan
      if (horaBase.split(':').length === 2) horaBase += ':00'

      if (ampmMatch) {
        let [hours, minutes, seconds] = horaBase.split(':').map(Number)
        const ampm = ampmMatch[0]

        if (ampm === 'PM' && hours !== 12) hours += 12
        if (ampm === 'AM' && hours === 12) hours = 0

        const hours24 = String(hours).padStart(2, '0')
        fullIsoString = `${fechaISO}T${hours24}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
      } else {
        // Formato 24h (por si otro endpoint lo usa)
        fullIsoString = `${fechaISO}T${horaBase}`
      }
    } else {
      // Solo fecha
      fullIsoString = `${fechaISO}T00:00:00`
    }

    const date = parseISO(fullIsoString)

    if (isNaN(date.getTime())) {
      return 'Fecha inválida'
    }

    // Formato final bonito en español y zona horaria de Colombia
    return format(date, "d MMM yyyy - hh:mm a", {
      locale: es,
      timeZone: 'America/Bogota'
    })
  } catch (error) {
    console.error('Error formateando fecha:', error, { fechaISO, horaString })
    return 'Fecha inválida'
  }
}

function formatPrice(price) {
  return `$${Number(price || 0).toLocaleString('es-CO')} COP`
}

function getTipoLabel(tipo) {
  const labels = {
    'aumento_stock': 'Aumento',
    'nuevos_productos': 'Productos Nuevos',
    'ambos': 'Aumento + Nuevos'
  }
  return labels[tipo] || tipo
}

function getTipoBadgeClass(tipo) {
  const classes = {
    'aumento_stock': 'badge-aumento',
    'nuevos_productos': 'badge-nuevos',
    'ambos': 'badge-ambos'
  }
  return classes[tipo] || ''
}

function verPreviewImagen(url) {
  if (url) {
    window.open(url, '_blank')
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.invoices-container {
  min-height: 100vh;
  background: #0a0a0a;
  padding: 1.5rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  position: relative;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
  margin-top: 1rem;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #ff006e 0%, #ff1493 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
}

/* BÚSQUEDA */
.search-section {
  max-width: 1200px;
  margin: 0 auto 2rem;
}

.search-container {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  background: #1a1a1a;
  border: 2px solid #ff006e;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-input:focus {
  outline: none;
  border-color: #ff1493;
  box-shadow: 0 0 15px rgba(255, 0, 110, 0.3);
  background: #222;
}

.search-icon {
  position: absolute;
  left: 1rem;
  font-size: 1.2rem;
  pointer-events: none;
}

.search-results-info {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
  text-align: center;
}

/* LOADER */
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: white;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 0, 110, 0.2);
  border-top-color: #ff006e;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.spinner.small {
  width: 30px;
  height: 30px;
  border-width: 3px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* EMPTY STATE */
.empty-state {
  background: #1a1a1a;
  border-radius: 16px;
  padding: 3rem;
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
  border: 2px solid #ff006e;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.5rem;
  color: #ff006e;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.7);
}

/* LISTA */
.facturas-list {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  gap: 1.5rem;
}

.factura-card {
  background: #1a1a1a;
  border: 2px solid #2a2a2a;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.factura-card:hover {
  border-color: #ff006e;
  box-shadow: 0 0 20px rgba(255, 0, 110, 0.2);
  transform: translateY(-3px);
}

.factura-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #2a2a2a;
  gap: 1rem;
  flex-wrap: wrap;
}

.factura-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.factura-id {
  font-size: 1.5rem;
  color: #ff006e;
  font-weight: bold;
}

.tipo-badge {
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-aumento {
  background: rgba(0, 150, 136, 0.2);
  color: #4db8af;
  border: 1px solid #4db8af;
}

.badge-nuevos {
  background: rgba(156, 39, 176, 0.2);
  color: #ce93d8;
  border: 1px solid #ce93d8;
}

.badge-ambos {
  background: rgba(255, 152, 0, 0.2);
  color: #ffb74d;
  border: 1px solid #ffb74d;
}

.factura-fecha {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.25rem;
  text-align: right;
}

.fecha {
  font-weight: 600;
  color: #ff006e;
  font-size: 0.95rem;
}

.hora {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
}

.factura-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.usuario-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.95rem;
}

.usuario-info .icon {
  font-size: 1.2rem;
}

.resumen-movimientos {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.movimiento-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
  font-size: 0.9rem;
  border-left: 3px solid;
}

.movimiento-item.aumentos {
  background: rgba(0, 150, 136, 0.1);
  color: #4db8af;
  border-left-color: #4db8af;
}

.movimiento-item.nuevos {
  background: rgba(156, 39, 176, 0.1);
  color: #ce93d8;
  border-left-color: #ce93d8;
}

.factura-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.5rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.factura-adjunta {
  color: #ff006e;
  font-weight: 600;
  font-size: 0.9rem;
}

.btn-ver-detalle {
  background: linear-gradient(135deg, #ff006e 0%, #ff1493 100%);
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-ver-detalle:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(255, 0, 110, 0.4);
}

.btn-ver-detalle:active {
  transform: scale(0.98);
}

/* MODAL */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  overflow-y: auto;
}

.modal-detalle {
  background: #1a1a1a;
  border: 2px solid #ff006e;
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem;
  position: relative;
}

.btn-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #ff006e;
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}

.btn-close:hover {
  background: #ff1493;
  transform: rotate(90deg);
}

.detalle-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #2a2a2a;
  flex-wrap: wrap;
}

.detalle-header h2 {
  color: #ff006e;
  font-size: 1.8rem;
}

.detalle-info {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-bottom: 2rem;
  background: #0a0a0a;
  padding: 1rem;
  border-radius: 10px;
  border-left: 4px solid #ff006e;
}

.info-row {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.info-row .label {
  font-weight: 600;
  color: #ff006e;
  min-width: 150px;
}

.info-row .value {
  color: rgba(255, 255, 255, 0.8);
}

.seccion-detalle {
  margin-bottom: 2rem;
}

.seccion-title {
  font-size: 1.3rem;
  color: #ff006e;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #ff006e;
}

.productos-detalle-scroll {
  max-height: 400px;
  overflow-y: auto;
  display: grid;
  gap: 1rem;
  padding-right: 0.5rem;
}

.productos-detalle-scroll::-webkit-scrollbar {
  width: 8px;
}

.productos-detalle-scroll::-webkit-scrollbar-track {
  background: #0a0a0a;
  border-radius: 10px;
}

.productos-detalle-scroll::-webkit-scrollbar-thumb {
  background: #ff006e;
  border-radius: 10px;
}

.productos-detalle-scroll::-webkit-scrollbar-thumb:hover {
  background: #ff1493;
}

.producto-detalle-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #0a0a0a;
  border: 1px solid #2a2a2a;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.producto-detalle-item:hover {
  border-color: #ff006e;
  background: #111;
}

.producto-detalle-item.nuevo {
  border-left: 4px solid #ce93d8;
}

.producto-imagen-container {
  position: relative;
  flex-shrink: 0;
}

.producto-imagen {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid #2a2a2a;
  cursor: pointer;
  transition: all 0.3s ease;
}

.producto-imagen:hover {
  border-color: #ff006e;
}


.producto-info-detalle {
  flex: 1;
  min-width: 0;
}

.producto-info-detalle h4 {
  color: #333;
  margin-bottom: 0.5rem;
  word-wrap: break-word;
}

.cantidad-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.cantidad-badge {
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-weight: 700;
  font-size: 0.9rem;
}

.cantidad-badge.aumento {
  background: #4caf50;
  color: white;
}

.cantidad-text {
  color: #666;
  font-size: 0.9rem;
}

.producto-specs {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.spec {
  background: white;
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
  font-size: 0.85rem;
  color: #555;
  border: 1px solid #ddd;
}

.seccion-factura {
  margin-bottom: 2rem;
}

.factura-adjunta-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff3e0;
  padding: 1rem;
  border-radius: 10px;
  border: 2px dashed #ff9800;
  gap: 1rem;
  flex-wrap: wrap;
}

.archivo-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  min-width: 0;
}

.archivo-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.archivo-datos {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.archivo-nombre {
  font-weight: 600;
  color: #333;
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.archivo-tipo {
  font-size: 0.85rem;
  color: #666;
}

.btn-descargar {
  background: #ff9800;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-descargar:hover {
  background: #f57c00;
  transform: scale(1.05);
}

.seccion-observaciones {
  background: #e3f2fd;
  padding: 1rem;
  border-radius: 10px;
  border-left: 4px solid #2196f3;
}

.seccion-observaciones p {
  color: #555;
  line-height: 1.6;
  word-wrap: break-word;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .invoices-container {
    padding: 1rem;
  }

  .btn-volver {
    position: static;
    margin-bottom: 1rem;
    width: fit-content;
  }

  .header {
    margin-top: 0;
  }

  .header h1 {
    font-size: 1.8rem;
  }

  .factura-header {
    flex-direction: column;
    gap: 1rem;
  }

  .factura-fecha {
    align-items: flex-start;
  }

  .factura-footer {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }

  .modal-detalle {
    padding: 1rem;
    max-height: 95vh;
  }

  .detalle-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .productos-detalle-scroll {
    max-height: 300px;
  }

  .factura-adjunta-container {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-descargar {
    width: 100%;
  }
}
</style>

