<template>
  <div class="valka-app">
    <header class="header">
      <div class="header-content">
        <div class="header-left">
          <button class="btn btn-back" @click="goBack">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 12H5M12 19L5 12L12 5" />
            </svg>
            <span>Volver</span>
          </button>
          <div class="logo">
            <h1 class="logo-title" :class="{ 'glitch-active': isGlitching }" data-text="Control AS">
              {{ admin.bar_nombre }}
            </h1>
            <p class="role">ID LOCAL: {{ admin.id }}</p>
          </div>
        </div>

        <div class="header-right">
          <button class="btn btn-tasks" @click="viewTasks">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
              <path d="M15 2H9a2 2 0 0 0-2 2v2a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2z" />
              <path d="M9 12h6M9 16h6" />
            </svg>
            Tareas
            <span v-if="pendingTasks > 0" class="notification-badge">{{ pendingTasks }}</span>
          </button>
        </div>
      </div>
    </header>

    <section class="main-actions">
      <div class="actions-container">
        <button class="btn btn-action btn-accounts" @click="makeCounts">
          <div class="btn-content">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              <line x1="9" y1="9" x2="15" y2="9" />
              <line x1="9" y1="15" x2="15" y2="15" />
            </svg>
            <span>Hacer Cuentas</span>
          </div>
        </button>
        <button v-if="barTipo === 'burdel'" class="btn btn-action btn-add-staff" @click="showAddStaffModal = true">
          <div class="btn-content">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="8.5" cy="7" r="4" />
              <line x1="20" y1="8" x2="20" y2="14" />
              <line x1="23" y1="11" x2="17" y2="11" />
            </svg>
            <span>Agregar Personal</span>
          </div>
        </button>
        <button class="btn btn-action btn-upload-products" @click="openInventoryModal">
          <div class="btn-content">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <path d="M12 18V12"></path>
              <path d="M9 15l3-3 3 3"></path>
            </svg>
            <span>Cargar productos</span>
          </div>
        </button>
      </div>
    </section>

    <!-- =================================== -->
    <!-- SECCIÓN DE PRODUCTOS CON SCROLL INFINITO -->
    <!-- =================================== -->
    <section class="products-section" @scroll="handleScroll">
      <div class="section-header">
        <div class="header-center">
          <div class="welcome-section">
            <h2 class="welcome-title">
              Bienvenido, <span class="admin-name">{{ admin.nombre }}</span>
            </h2>
          </div>
        </div>
        <div class="products-controls">
          <div class="search-container">
            <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2" />
              <path d="M21 21L16.65 16.65" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <input v-model="searchQuery" type="text" placeholder="Buscar productos..." class="search-input" />
          </div>
          <button class="btn btn-filter" :class="{ active: showOutOfStock }" @click="toggleOutOfStock">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M3 6L5 6A2 2 0 1 0 7 4H19A2 2 0 0 1 21 6V18A2 2 0 0 1 19 20H7A2 2 0 1 0 5 18V6Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            Solo Agotados
          </button>
        </div>
      </div>

      <!-- Estados de carga y vacío -->
      <div v-if="loading" class="loading-state"><p>Cargando productos...</p></div>
      <div v-else-if="products.length === 0" class="empty-state">
        <p>No hay productos aún.</p>
        <p>Por favor, pida al dueño que los agregue para gestionar el inventario.</p>
      </div>
      <div v-else-if="filteredProducts.length === 0" class="no-results-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#A0AEC0" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <p>No hay coincidencias con esa búsqueda.</p>
      </div>

      <!-- Lista de productos -->
      <div v-else class="products-grid">
        <div v-for="product in filteredProducts" :key="product.id" class="product-card" :class="{ 'out-of-stock': product.cantidad === 0 }">
          <div class="product-image">
            <img :src="product.imagen" :alt="product.nombre" />
            <div v-if="product.cantidad === 0" class="stock-badge stock-out">agotado</div>
          </div>
          <div class="product-info">
            <h4 class="product-name">{{ product.nombre }}</h4>
            <div class="product-details">
              <span class="product-price" :class="{ 'price-out-of-stock': product.cantidad === 0 }">
                ${{ formatPrice(product.precio) }}
              </span>
              <span class="product-quantity" :class="{ 'zero': product.cantidad === 0, 'low': product.cantidad < 5 && product.cantidad > 0 }">
                {{ product.cantidad }} unid.
              </span>
            </div>
          </div>
        </div>
        <div v-if="loadingMore" class="loading-more"><p>Cargando más productos...</p></div>
      </div>
    </section>

    <!-- Modal de inventario -->
    <InventoryModal v-if="showInventoryModal" @navigate-out="handleInventoryModalClose" />

    <!-- ================== MODAL AGREGAR PERSONAL ================== -->
    <div v-if="showAddStaffModal" class="modal-overlay" @click="closeAddStaffModal">
      <div class="modal-content modal-dark" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">Agregar Personal</h3>
          <button class="btn btn-close btn-close-dark" @click="closeAddStaffModal">✕</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="addStaff" class="staff-form">

            <!-- FOTO DE PERFIL -->
            <div class="form-row">
              <div class="form-group full-width">
                <label class="form-label">Foto de Perfil *</label>
                <div class="image-upload-container">
                  <div class="image-upload-area image-upload-area-dark" @click="triggerFileInput">
                    <input ref="fileInput" type="file" @change="handleImageUpload" accept="image/*" class="file-input-hidden" />
                    <div v-if="!newStaff.imagePreview" class="upload-placeholder upload-placeholder-dark">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#A0AEC0">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2" />
                        <circle cx="8.5" cy="8.5" r="1.5" stroke="currentColor" stroke-width="2" />
                        <path d="M21 15L16 10L5 21" stroke="currentColor" stroke-width="2" />
                      </svg>
                      <span>Seleccionar Imagen</span>
                    </div>
                    <div v-else class="image-preview">
                      <img :src="newStaff.imagePreview" alt="Preview" />
                      <div class="image-overlay"><span>Cambiar</span></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- NOMBRE Y FECHA INGRESO -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Nombre Completo *</label>
                <input v-model="newStaff.nombre" type="text" required class="form-input form-input-dark" />
              </div>
              <div class="form-group">
                <label class="form-label">Fecha de Ingreso</label>
                <input v-model="newStaff.fecha_agregado_local" type="text" readonly class="form-input form-input-dark readonly readonly-dark" />
              </div>
            </div>

            <!-- TELÉFONO Y AGREGADO POR -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Teléfono *</label>
                <input v-model="newStaff.telefono" type="tel" required class="form-input form-input-dark" />
              </div>
              <div class="form-group">
                <label class="form-label">Agregado por</label>
                <input :value="admin.nombre" type="text" readonly class="form-input form-input-dark readonly readonly-dark" />
              </div>
            </div>

            <!-- DOCUMENTO -->
            <div class="form-row">
              <div class="form-group full-width">
                <label class="form-label">Documento *</label>
                <input v-model="newStaff.documento" type="text" required class="form-input form-input-dark" @input="filterDocumento" />
              </div>
            </div>

            <!-- ====== NUEVOS CAMPOS OBLIGATORIOS: EXAMEN MÉDICO ====== -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">Fecha del Examen Médico *</label>
                <input v-model="newStaff.fecha_examen" type="date" required class="form-input form-input-dark" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group full-width">
                <label class="form-label">Foto del Examen Médico (PDF o imagen) *</label>
                <div class="image-upload-container">
                  <div class="image-upload-area image-upload-area-dark" @click="triggerFileInputExamen">
                    <input ref="fileInputExamen" type="file" @change="handleExamenUpload" accept="image/*,application/pdf" class="file-input-hidden" />
                    <div v-if="!newStaff.examenPreview" class="upload-placeholder upload-placeholder-dark">
                      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#A0AEC0">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                      </svg>
                      <span>Subir examen médico</span>
                    </div>
                    <div v-else class="image-preview">
                      <img v-if="isImageExamen" :src="newStaff.examenPreview" alt="Examen" />
                      <div v-else class="pdf-preview">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#EC4899" stroke-width="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                          <polyline points="14 2 14 8 20 8"></polyline>
                          <text x="8" y="16" font-size="8" fill="#EC4899">PDF</text>
                        </svg>
                        <span>PDF Cargado</span>
                      </div>
                      <div class="image-overlay"><span>Cambiar</span></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- ====== FIN CAMPOS EXAMEN ====== -->

            <div class="form-actions">
              <button type="button" @click="closeAddStaffModal" class="btn btn-secondary">Cancelar</button>
              <button 
  type="submit" 
  class="btn btn-primary" 
  :disabled="isSubmitting"
>
  <span v-if="isSubmitting">
    <svg class="spinner" width="16" height="16" viewBox="0 0 38 38" stroke="#fff">
      <g fill="none" fill-rule="evenodd">
        <g transform="translate(1 1)" stroke-width="2">
          <circle stroke-opacity=".5" cx="18" cy="18" r="18"/>
          <path d="M36 18c0-9.94-8.06-18-18-18">
            <animateTransform attributeName="transform" type="rotate" from="0 18 18" to="360 18 18" dur="1s" repeatCount="indefinite"/>
          </path>
        </g>
      </g>
    </svg>
    Agregando...
  </span>
  <span v-else>Agregar Personal</span>
</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Modal éxito -->
    <div v-if="showSuccessModal" class="modal-overlay modal-success-overlay" @click="closeSuccessModal">
      <div class="success-modal success-modal-dark" @click.stop>
        <div class="success-header">
          <div class="success-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#A0E9CA" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          </div>
          <h3 class="success-title">Personal Agregado</h3>
        </div>
        <div class="success-body">
          <div class="staff-info-card">
            <div class="staff-avatar">
              <img :src="addedStaff.foto" :alt="addedStaff.nombre" />
            </div>
            <div class="staff-details">
              <h4>{{ addedStaff.nombre }}</h4>
              <p class="staff-detail">Ingresó: {{ new Date(addedStaff.fecha_agregado).toLocaleDateString('es-ES') }}</p>
              <p class="staff-detail">Teléfono: {{ addedStaff.telefono }}</p>
            </div>
          </div>
          <button @click="closeSuccessModal" class="btn btn-primary btn-success">Entendido</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '@/stores/admin'
import axios from 'axios'
import { API_BASE_URL } from '../config/api'
import InventoryModal from './agregar_admin.vue'

// -------------------------------------------------
// Configuración y constantes
// -------------------------------------------------
const LIMIT = 20

// -------------------------------------------------
// Stores y router
// -------------------------------------------------
const adminStore = useAdminStore()
const router = useRouter()
const admin = computed(() => adminStore)
const isSubmitting = ref(false)
// -------------------------------------------------
// Estados generales
// -------------------------------------------------
const pendingTasks = ref(0)
const searchQuery = ref('')
const showOutOfStock = ref(false)
const showAddStaffModal = ref(false)
const showSuccessModal = ref(false)
const showInventoryModal = ref(false)
const barTipo = ref(null)
const isGlitching = ref(false)

// -------------------------------------------------
// Productos + scroll infinito
// -------------------------------------------------
const products = ref([])
const loading = ref(true)
const loadingMore = ref(false)
const hasMore = ref(true)
const currentSkip = ref(0)

const productsSection = ref(null)

// -------------------------------------------------
// Staff modal (agregar personal)
// -------------------------------------------------
const fileInput = ref(null)
const fileInputExamen = ref(null)

const newStaff = ref({
  nombre: '',
  documento: '',
  telefono: '',
  foto: null,
  fecha_agregado_local: new Date().toLocaleDateString('es-ES'),
  imagePreview: null,
  fecha_examen: '',
  foto_examen: null,
  examenPreview: null,
})

const addedStaff = ref({})

const isImageExamen = computed(() => {
  return newStaff.value.foto_examen && newStaff.value.foto_examen.startsWith('data:image')
})

// -------------------------------------------------
// Computed
// -------------------------------------------------
const filteredProducts = computed(() => {
  let filtered = products.value

  if (searchQuery.value) {
    filtered = filtered.filter(p =>
      p.nombre.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (showOutOfStock.value) {
    filtered = filtered.filter(p => p.cantidad === 0)
  }

  return filtered
})

const formatPrice = (price) => new Intl.NumberFormat('es-CO').format(price)

// -------------------------------------------------
// Funciones de carga de productos
// -------------------------------------------------
const fetchProducts = async (reset = false) => {
  if (reset) {
    currentSkip.value = 0
    products.value = []
    hasMore.value = true
  }

  if (!hasMore.value || loadingMore.value) return

  if (reset) loading.value = true
  else loadingMore.value = true

  try {
    const response = await axios.get(
      `${API_BASE_URL}/productos_por_bar/${admin.value.bar_id}`,
      {
        params: { skip: currentSkip.value, limit: LIMIT }
      }
    )

    const nuevos = response.data || []

    if (nuevos.length < LIMIT) hasMore.value = false

    products.value = reset ? nuevos : [...products.value, ...nuevos]
    currentSkip.value += nuevos.length
  } catch (err) {
    console.error('Error cargando productos:', err)
    hasMore.value = false
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

// -------------------------------------------------
// Scroll infinito
// -------------------------------------------------
const handleScroll = (e) => {
  const el = e.target
  const nearBottom = el.scrollHeight - el.scrollTop <= el.clientHeight + 200 // 200px de tolerancia

  if (nearBottom && hasMore.value && !loadingMore.value) {
    fetchProducts()
  }
}

// -------------------------------------------------
// Otras peticiones
// -------------------------------------------------
const fetchBarInfo = async () => {
  try {
    const res = await axios.get(`${API_BASE_URL}/bar_tipo/${admin.value.bar_id}`)
    barTipo.value = res.data.tipo
  } catch (err) {
    console.error('Error obteniendo tipo de bar:', err)
  }
}

const fetchPendingTasks = async () => {
  try {
    // Usamos el ID del admin que ya tienes en el store
    const response = await axios.get(
      `${API_BASE_URL}/tareas_pendientes_count/${admin.value.id}`
    )
    // La respuesta viene como { "pendientes": 5 }
    pendingTasks.value = response.data.pendientes
  } catch (err) {
    console.error('Error cargando tareas pendientes:', err)
    pendingTasks.value = 0  // en caso de error, no mostramos badge
  }
}

// -------------------------------------------------
// Navegación y acciones principales
// -------------------------------------------------
const goBack = () => {
  adminStore.logout()
  router.push('/login')
}

const viewTasks = () => router.push('/tareas')
const makeCounts = () => router.push({ name: 'factura_admin' })
const openInventoryModal = () => (showInventoryModal.value = true)

const handleInventoryModalClose = () => {
  showInventoryModal.value = false
  fetchProducts(true) // recarga completa después de agregar productos
}

const toggleOutOfStock = () => (showOutOfStock.value = !showOutOfStock.value)

// -------------------------------------------------
// Modal agregar personal
// -------------------------------------------------
const triggerFileInput = () => fileInput.value.click()
const triggerFileInputExamen = () => fileInputExamen.value.click()

const handleImageUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (ev) => {
      newStaff.value.imagePreview = ev.target.result
      newStaff.value.foto = ev.target.result
    }
    reader.readAsDataURL(file)
  }
}

const handleExamenUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (ev) => {
      newStaff.value.examenPreview = ev.target.result
      newStaff.value.foto_examen = ev.target.result
    }
    reader.readAsDataURL(file)
  }
}

const filterDocumento = (e) => {
  const value = e.target.value.replace(/\D/g, '')
  newStaff.value.documento = value
  e.target.value = value
}

const addStaff = async () => {
  // Validaciones rápidas (evita incluso intentar si falta algo)
  if (!newStaff.value.foto) return alert('Por favor, sube una foto de perfil.')
  if (!newStaff.value.documento?.trim()) return alert('El documento es obligatorio.')
  if (!newStaff.value.fecha_examen) return alert('La fecha del examen médico es obligatoria.')
  if (!newStaff.value.foto_examen) return alert('Debes subir la foto o PDF del examen médico.')

  // ← BLOQUEO: si ya está enviando, no hace nada
  if (isSubmitting.value) return

  isSubmitting.value = true  // Activar loading y deshabilitar botón

  const payload = {
    nombre: newStaff.value.nombre,
    documento: newStaff.value.documento.trim(),
    telefono: newStaff.value.telefono,
    foto: newStaff.value.foto,
    agregado_por: admin.value.id,
    dueno_id: admin.value.dueno_id,
    fecha_examen: newStaff.value.fecha_examen,
    foto_examen: newStaff.value.foto_examen,
  }

  try {
    const response = await axios.post(`${API_BASE_URL}/mujeres`, payload)
    addedStaff.value = response.data
    showAddStaffModal.value = false
    showSuccessModal.value = true

    // Reset del formulario
    newStaff.value = {
      nombre: '',
      documento: '',
      telefono: '',
      foto: null,
      fecha_agregado_local: new Date().toLocaleDateString('es-ES'),
      imagePreview: null,
      fecha_examen: '',
      foto_examen: null,
      examenPreview: null,
    }
  } catch (error) {
    console.error('Error al agregar personal:', error)
    const mensaje = error.response?.data?.detail || 'Error al crear la mujer'
    alert(mensaje)

    // Si el error es por duplicado (ej: documento ya existe), puedes detectarlo:
    if (error.response?.status === 400 && mensaje.includes('documento')) {
      alert('Ya existe una persona con ese documento.')
    }
  } finally {
    isSubmitting.value = false  // ← SIEMPRE se quita el loading
  }
}
const closeAddStaffModal = () => (showAddStaffModal.value = false)
const closeSuccessModal = () => (showSuccessModal.value = false)

// -------------------------------------------------
// Efecto glitch del logo
// -------------------------------------------------
const toggleGlitch = () => {
  const delay = Math.random() * 5000 + 3000
  setTimeout(() => {
    isGlitching.value = true
    setTimeout(() => {
      isGlitching.value = false
      toggleGlitch()
    }, 1000)
  }, delay)
}

// -------------------------------------------------
// Lifecycle
// -------------------------------------------------
onMounted(() => {
  fetchBarInfo()
  fetchProducts(true)
  fetchPendingTasks()
  toggleGlitch()
  router.afterEach(() => {
    if (router.currentRoute.value.name === 'tu-nombre-de-ruta-aqui') {
      fetchPendingTasks()
    }
  })
})

// No necesitamos remover el listener porque usamos @scroll en el template
</script>

<!-- ================== ESTILOS COMPLETOS (incluye PDF preview) ================== -->
<style scoped>
/* ... todos tus estilos anteriores ... */



/* Responsive: en móvil los campos examen van debajo uno del otro */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr !important;
  }
}
</style>
<style scoped>

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Poppins:wght@700;800&display=swap');
.pdf-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #EC4899;
  font-weight: 600;
  font-size: 14px;
  width: 100%;
  height: 100%;
  background: rgba(236, 72, 153, 0.1);
  border-radius: var(--radius-md);
}

.pdf-preview span {
  margin-top: 8px;
}

/* Aseguramos que el overlay siga funcionando en el examen */
.image-upload-area:hover .image-overlay {
  opacity: 1;
}
body {
    font-family: 'Montserrat', sans-serif;
    background-color: #0F172A;
    color: #E5E7EB;
    line-height: 1.6;
}

.valka-app {
    --spacing-xs: 0.5rem;
    --spacing-sm: 1rem;
    --spacing-md: 1rem;
    --spacing-lg: 1rem;
    --spacing-xl: 3rem;
    --spacing-2xl: 4rem;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    
    background: radial-gradient(circle at 50% 120%, rgba(0, 0, 0, 0.9) 0%, #0f1012 100%);
    min-height: 100vh;
}

.btn {
    padding: 0.75rem 1.25rem;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    transition: all 0.2s ease;
    border: 1px solid transparent;
    text-decoration: none;
    white-space: nowrap;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-primary {
    background: #EC4899;
    color: #FFFFFF;
    border-color: #BE185D;
}

.btn-primary:hover {
    background: #BE185D;
}

.btn-secondary {
    background: #2D3748;
    color: #A0AEC0;
    border-color: #4A5568;
}

.btn-secondary:hover {
    background: #4A5568;
    color: #FFFFFF;
}

/* Specific Button Styles */
.btn-back {
    background: rgba(66, 153, 225, 0.1);
    border: 1px solid rgba(66, 153, 225, 0.3);
    color: #63B3ED;
    padding: 0.75rem 1.25rem;
    border-radius: 9999px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-back:hover {
    background: rgba(66, 153, 225, 0.2);
    border-color: #63B3ED;
    transform: scale(1.05);
}

.btn-tasks {
    background: rgba(236, 72, 153, 0.1);
    border: 1px solid rgba(236, 72, 153, 0.3);
    color: #EC4899;
    position: relative;
    border-radius: 9999px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-tasks:hover {
    background: rgba(236, 72, 153, 0.2);
    border-color: #EC4899;
    transform: scale(1.05);
}

.btn-filter {
    background: rgba(239, 68, 68, 0.1);
    border-color: rgba(239, 68, 68, 0.3);
    color: #EF4444;
}

.btn-filter.active,
.btn-filter:hover {
    background: rgba(239, 68, 68, 0.2);
    border-color: #EF4444;
}

/* Action Buttons with Gradient */
.btn-action {
    font-size: 1.1rem;
    padding: 1.2rem 2rem;
    border-radius: var(--radius-md);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    min-width: 200px;
    position: relative;
    overflow: hidden;
    z-index: 1;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    border: none;
    font-weight: 700;
}

.btn-action:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.btn-action::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    transition: opacity 0.2s ease-in-out;
    z-index: -1;
}

.btn-action:hover::before {
    opacity: 0.2;
}

.btn-accounts {
    background: #111;
    color: #fff;
    border: 2px solid #ec4899;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    text-shadow: 0 0 3px #ec4899;
    box-shadow: 0 0 10px #ec4899, 0 0 20px #be185d;
    cursor: pointer;
    transition: 0.3s ease;
}

.btn-accounts:hover {
    background-color: #ec4899;
    color: #111;
    box-shadow: 0 0 20px #ec4899, 0 0 30px #be185d;
}


.btn-add-staff {
    background: transparent;
    color: #3bcef6;
    border: 2px solid #3bd4f6;
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: bold;
    position: relative;
    overflow: hidden;
    transition: color 0.3s ease;
    cursor: pointer;
}

.btn-add-staff::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: linear-gradient(100deg, #63cded, #3bf6f6);
    z-index: 0;
    transform: translateY(100%);
    transition: transform 0.3s ease;
}

.btn-add-staff:hover::before {
    transform: translateY(0%);
}

.btn-add-staff span {
    position: relative;
    z-index: 1;
}

.btn-add-staff:hover {
    color: white;
}


.btn-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    justify-content: center;
}

/* ==================================== */
/* === Header Section === */
/* ==================================== */

.header {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(15px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: var(--spacing-md) 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
}

.header-left {
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
}

.logo-title {
    font-family: 'Poppins', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #E2E8F0;
    margin: 0;
    position: relative;
    transition: all 0.2s ease;
    text-shadow: 1px 0 #63B3ED, -1px 0 #EC4899;
}

/* Glitch Triggered by Class (new) */
.logo-title.glitch-active {
    animation: s-glitch 0.5s infinite alternate;
}

@keyframes s-glitch {
    0% { transform: translate(1px, 1px); }
    100% { transform: translate(-1px, -1px); }
}

.logo-title::before,
.logo-title::after {
    content: attr(data-text);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    text-shadow: 0;
    opacity: 0;
    transition: opacity 0.2s ease;
}

/* Glitch Triggered by Class (new) */
.logo-title.glitch-active::before {
    opacity: 1;
    color: #63B3ED;
    animation: glitch-before 1s linear infinite alternate;
}
.logo-title.glitch-active::after {
    opacity: 1;
    color: #EC4899;
    animation: glitch-after 1s linear infinite alternate;
}

@keyframes glitch-before {
    0% { transform: translate(1px, 1px); }
    100% { transform: translate(-1px, -1px); }
}

@keyframes glitch-after {
    0% { transform: translate(-1px, -1px); }
    100% { transform: translate(1px, 1px); }
}

.logo-subtitle {
    font-size: 0.9rem;
    color: #A0AEC0;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.welcome-section {
    text-align: center;
    background: linear-gradient(145deg, rgba(236, 72, 153, 0.05), rgba(99, 179, 237, 0.05));
    padding: 0.40rem 1rem;
    border-radius: var(--radius-md);
    border: 1px solid;
    border-image: linear-gradient(145deg, #EC4899, #63B3ED) 1;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
    margin-bottom:20px;
}

.welcome-section:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(0,0,0,0.3);
}

.welcome-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #E2E8F0;
    margin: 0 0 0.25rem 0;
    letter-spacing: 1px;
    text-shadow: 0 0 5px rgba(255,255,255,0.5);
    position: relative;
    overflow: hidden;
    display: inline-block;
}

.welcome-title::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    height: 2px;
    background: linear-gradient(to right, transparent, #EC4899, transparent);
    opacity: 0.8;
}

.admin-name {
    color: #EC4899;
    font-weight: 800;
}

.role {
    color: #A0AEC0;
    font-size: 0.70rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.notification-badge {
    background: #EF4444;
    color: #FFFFFF;
    border-radius: 50%;
    width: 22px;
    height: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 600;
    position: absolute;
    top: -8px;
    right: -8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* ==================================== */
/* === Main Actions Section === */
/* ==================================== */

.main-actions {
    padding: var(--spacing-xl) var(--spacing-lg);
    max-width: 1400px;
    margin: 0 auto;
}

.actions-container {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    flex-wrap: wrap;
}

.btn-content {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    justify-content: center;
}

/* ==================================== */
/* === Products Section === */
/* ==================================== */

.products-section {
    padding: var(--spacing-lg) var(--spacing-lg);
    max-width: 1400px;
    margin: 0 auto;
}

.section-header {
    margin-bottom: var(--spacing-lg);
}

.section-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #ffffff;
    text-align: center;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: var(--spacing-lg);
    background: linear-gradient(90deg, #ff7eb3, #ff758c);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}


.products-controls {
    display: flex;
    gap: var(--spacing-sm);
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: var(--spacing-lg);
}

.search-container {
    position: relative;
    flex: 1;
    max-width: 400px;
}

.search-input {
    width: 100%;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #E2E8F0;
    padding: 0.75rem 1rem 0.75rem 3rem;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    transition: all 0.2s ease;
}

.search-input::placeholder {
    color: #A0AEC0;
}

.search-input:focus {
    outline: none;
    border-color: #63B3ED;
    background: rgba(255, 255, 255, 0.08);
}

.search-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: #A0AEC0;
}

/* Products Grid */
.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: var(--spacing-md);
}

.product-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--radius-md);
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    border-color: rgba(236, 72, 153, 0.3);
}

.product-card.out-of-stock {
    border-color: rgba(239, 68, 68, 0.4);
    opacity: 0.8;
}

.product-image {
    position: relative;
    height: 200px;
    overflow: hidden;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.product-image img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
    transform: scale(1.05);
}

.stock-badge {
    position: absolute;
    top: 0.75rem;
    right: 0.75rem;
    padding: 0.25rem 0.75rem;
    border-radius: var(--radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
    color: #FFFFFF;
}

.stock-badge.stock-out {
    background: #EF4444;
}

.stock-badge.stock-low {
    background: #F59E0B;
}

.product-info {
    padding: 1.25rem;
}

.product-name {
    font-size: 1.2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.5rem;
}

.product-details {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
}

.product-price {
    font-size: 1.5rem;
    font-weight: 800;
    color: #48BB78;
}

.product-price.price-out-of-stock {
    color: #EF4444;
}

.product-quantity {
    font-size: 1rem;
    color: #A0AEC0;
    font-weight: 600;
}

.product-quantity.zero {
    color: #EF4444;
}

.product-quantity.low {
    color: #F59E0B;
}

/* Empty States */
.empty-state,
.no-results-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: var(--spacing-xl);
    min-height: 400px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px dashed rgba(255, 255, 255, 0.1);
    border-radius: var(--radius-lg);
    margin-top: var(--spacing-lg);
}

.empty-state p,
.no-results-state p {
    font-size: 1.2rem;
    color: #A0AEC0;
    margin-bottom: var(--spacing-sm);
}

.empty-state .btn {
    margin-top: var(--spacing-sm);
}

.no-results-state svg {
    margin-bottom: var(--spacing-md);
}

/* ==================================== */
/* === Modal Styles === */
/* ==================================== */

.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.75);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(4px);
    overflow-y: auto;
    padding: var(--spacing-lg);
    animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.modal-content {
    background: #FFFFFF;
    border-radius: var(--radius-lg);
    width: 100%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    color: #1F2937;
    transform: translateY(-20px);
    animation: slideIn 0.3s ease-out forwards;
}

@keyframes slideIn {
    from { transform: translateY(-50px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.modal-content.modal-dark {
    background-color: #1A202C;
    color: #E2E8F0;
    border: 1px solid #4A5568;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-md) var(--spacing-lg);
    border-bottom: 1px solid #E5E7EB;
}

.modal-content.modal-dark .modal-header {
    border-bottom-color: #4A5568;
}

.modal-title {
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0;
}

.modal-content.modal-dark .modal-title {
    color: #E2E8F0;
}

.btn-close {
    background: transparent;
    border: none;
    color: #A0AEC0;
    padding: 0.5rem;
    border-radius: var(--radius-sm);
    transition: all 0.2s ease;
}

.btn-close:hover {
    background: #F3F4F6;
    color: #1F2937;
    transform: rotate(90deg);
}

.modal-content.modal-dark .btn-close {
    color: #A0AEC0;
}

.modal-content.modal-dark .btn-close:hover {
    background: #4A5568;
    color: #E2E8F0;
}

.modal-body {
    padding: var(--spacing-lg);
}

/* Form Styles */
.staff-form {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-sm);
}

.form-group.full-width {
    grid-column: 1 / -1;
}

.form-label {
    display: block;
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.modal-content.modal-dark .form-label {
    color: #A0AEC0;
}

.form-input {
    width: 100%;
    background: #F9FAFB;
    border: 1px solid #D1D5DB;
    color: #1F2937;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    transition: all 0.2s ease;
}

.form-input:focus {
    outline: none;
    border-color: #63B3ED;
    box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
    background: #FFFFFF;
}

.form-input.readonly {
    background: #F3F4F6;
    color: #A0AEC0;
    cursor: not-allowed;
}

.modal-content.modal-dark .form-input {
    background-color: #2D3748;
    border-color: #4A5568;
    color: #E2E8F0;
}

.modal-content.modal-dark .form-input::placeholder {
    color: #718096;
}

.modal-content.modal-dark .form-input:focus {
    border-color: #667EEA;
    box-shadow: 0 0 0 3px rgba(86, 136, 222, 0.2);
    background-color: #4A5568;
}

.modal-content.modal-dark .form-input.readonly {
    background-color: #4A5568;
    color: #A0AEC0;
}

.image-upload-container {
    display: flex;
    justify-content: center;
}

.image-upload-area {
    width: 150px;
    height: 150px;
    border: 2px dashed #D1D5DB;
    border-radius: var(--radius-md);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.image-upload-area:hover {
    border-color: #63B3ED;
    background: rgba(66, 153, 225, 0.02);
}

.modal-content.modal-dark .image-upload-area {
    border-color: #4A5568;
}

.modal-content.modal-dark .image-upload-area:hover {
    border-color: #667EEA;
    background: rgba(86, 136, 222, 0.05);
}

.upload-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    color: #A0AEC0;
    text-align: center;
    padding: 1rem;
}

.modal-content.modal-dark .upload-placeholder {
    color: #718096;
}

.upload-placeholder svg {
    color: #A0AEC0;
}

.image-preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: var(--radius-md);
}

.image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    font-weight: 600;
    opacity: 0;
    transition: opacity 0.2s ease;
    border-radius: var(--radius-md);
}

.image-upload-area:hover .image-overlay {
    opacity: 1;
}

.form-actions {
    display: flex;
    gap: var(--spacing-sm);
    justify-content: flex-end;
    padding-top: var(--spacing-md);
    border-top: 1px solid #E5E7EB;
}

.modal-content.modal-dark .form-actions {
    border-top-color: #4A5568;
}

/* === Success Modal (Redesigned) === */

.modal-success-overlay {
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.3s ease-out;
}

.success-modal-dark {
    background: #1a1a2e; /* Darker background */
    border-radius: var(--radius-lg);
    max-width: 450px;
    width: 90%;
    padding: var(--spacing-lg);
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
    overflow: hidden;
    animation: popIn 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

@keyframes popIn {
    from {
        transform: scale(0.8) translateY(-50px);
        opacity: 0;
    }
    to {
        transform: scale(1) translateY(0);
        opacity: 1;
    }
}

.success-modal-dark::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 50% 0, rgba(147, 51, 234, 0.2) 0%, transparent 70%);
    z-index: -1;
}

.success-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-md);
}

.success-icon {
    background: linear-gradient(135deg, #a0e9ca, #63cded);
    border-radius: 50%;
    padding: 0.5rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 64px;
    height: 64px;
    box-shadow: 0 0 15px rgba(160, 233, 202, 0.5);
}

.success-icon svg {
    color: #1a1a2e;
    stroke: #1a1a2e;
    stroke-width: 2;
}

.success-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #E5E7EB;
    text-shadow: 0 0 5px rgba(255,255,255,0.2);
    margin: 0;
}

.success-body {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.staff-info-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(5px);
    border-radius: var(--radius-md);
    padding: var(--spacing-md);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.staff-info-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
}

.staff-avatar img {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 50%;
    border: 4px solid #EC4899;
    box-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
    margin-bottom: var(--spacing-sm);
}

.staff-details {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.staff-details h4 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #EC4899;
    margin: 0 0 0.5rem 0;
}

.staff-detail {
    color: #A0AEC0;
    font-size: 0.95rem;
    font-weight: 500;
    margin: 0.25rem 0;
}

.btn-success {
    background: linear-gradient(90deg, #EC4899, #63B3ED);
    color: #fff;
    font-weight: 700;
    padding: 1rem 2rem;
    border: none;
    border-radius: var(--radius-sm);
    margin-top: var(--spacing-md);
    box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
    transition: all 0.3s ease;
}

.btn-success:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 6px 20px rgba(236, 72, 153, 0.5);
}


/* ==================================== */
/* === Footer === */
/* ==================================== */

.footer {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(15px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: var(--spacing-2xl);
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-lg);
    padding: var(--spacing-xl) var(--spacing-lg) var(--spacing-lg);
    max-width: 1400px;
    margin: 0 auto;
}

.footer-logo {
    color: #EC4899;
    margin-bottom: var(--spacing-sm);
    font-size: 1.1rem;
    font-weight: 600;
}

.footer-section p {
    color: #A0AEC0;
    margin: 0.5rem 0;
    font-size: 0.9rem;
}

.footer-bottom {
    text-align: center;
    padding: var(--spacing-md);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    color: #A0AEC0;
    font-size: 0.9rem;
}

/* ==================================== */
/* === Responsive Design === */
/* ==================================== */
@media (max-width: 1024px) {
    .header-content {
        flex-wrap: wrap;
        gap: var(--spacing-sm);
    }

    .header-center {
        order: 3;
        flex-basis: 100%;
    }
}

@media (max-width: 768px) {
    .header-content {
        flex-direction: column;
        text-align: center;
    }
    .form-row {
    grid-template-columns: 1fr !important;
    }

    .header-left,
    .header-right {
        justify-content: center;
    }
    
    .header-left {
        width: 100%;
        justify-content: space-between;
    }
    
    .btn-back {
        padding: 0.5rem 1rem;
    }
    
    .btn-back span {
        display: none;
    }

    .actions-container {
        flex-direction: column;
        align-items: center;
    }

    .products-controls {
        flex-direction: column;
        gap: var(--spacing-sm);
    }

    .search-container {
        max-width: 100%;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    .modal-overlay {
        padding: var(--spacing-sm);
    }

    .modal-body {
        padding: var(--spacing-md);
    }

    .form-actions {
        flex-direction: column-reverse;
    }

    .btn-primary,
    .btn-secondary {
        width: 100%;
    }
    
    .staff-info-card {
        flex-direction: column;
        align-items: center;
    }
    
    .welcome-title {
        font-size: 1.5rem;
    }
    
    .logo-title {
        font-size: 2rem;
    }
}

@media (max-width: 480px) {
    .products-section,
    .main-actions {
        padding: var(--spacing-md) var(--spacing-sm);
    }

    .header-content {
        padding: 0 var(--spacing-sm);
    }

    .products-grid {
        grid-template-columns: 1fr;
    }
    
    .logo-title {
        font-size: 1.8rem;
    }
    
    .btn-back,
    .btn-tasks {
        padding: 0.6rem;
        gap: 0.5rem;
    }
}

/* ==================================== */
/* === Scrollbar Styling === */
/* ==================================== */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb {
    background: #EC4899;
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: #BE185D;
}

/* ==================================== */
/* === New Button Style (Products) - Border Reveal/Halo V2 === */
/* ==================================== */

/* Estilo para el botón de Cargar Productos (Estado Normal) */
.btn-upload-products {
    background: transparent;
    color: #E5E7EB; 
    /* ¡BORDE MÁS GRUESO Y VISIBLE! */
    border: 3px solid rgba(255, 255, 255, 0.7); 
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: bold;
    position: relative;
    overflow: hidden;
    /* Transición en el color del texto y la transformación */
    transition: all 0.4s ease-in-out; 
    cursor: pointer;
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.15); /* Sombra base sutil */
    z-index: 1; 
}

/* El elemento ::before será el halo o el fondo que se mueve */
.btn-upload-products::before {
    content: '';
    position: absolute;
    top: -50%; 
    left: -50%;
    width: 200%; 
    height: 200%;
    /* Un gradiente más definido para el halo */
    background: conic-gradient(transparent, rgba(255, 255, 255, 0.25), transparent 40%, transparent);
    z-index: 0;
    transform: rotate(0deg);
    transition: background 0.4s, opacity 0.4s;
    /* Añadimos la animación de rotación, pero solo se activa en hover */
}

/* El elemento ::after: El borde blanco que se revela */
.btn-upload-products::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    /* Borde grueso que oculta el borde real */
    border: 3px solid transparent; 
    border-radius: 10px;
    z-index: 3; 
    transition: border-color 0.4s ease-in-out;
}

/* Estado Hover: Los cambios de estilo */
.btn-upload-products:hover {
    color: #FFFFFF; 
    transform: scale(1.05); /* Se agranda un poco más */
    /* Resplandor más fuerte y brillante */
    box-shadow: 0 0 10px #FFFFFF, 0 0 30px rgba(255, 255, 255, 0.5);
    /* El borde real se vuelve invisible */
    border-color: transparent; 
}

/* Estado Hover: Animación del ::before (El halo gira) */
.btn-upload-products:hover::before {
    /* Giro más rápido y continuo */
    transform: rotate(360deg); 
    /* Hacemos el gradiente más visible y sólido */
    background: conic-gradient(transparent, #FFFFFF, transparent 40%, transparent);
    transition: transform 1.5s linear, background 0.4s; 
}

/* Estado Hover: Animación del ::after (El borde se revela) */
.btn-upload-products:hover::after {
    /* Se revela un borde sólido blanco */
    border-color: #FFFFFF;
}

/* Asegura que el contenido (span y svg) esté por encima */
.btn-upload-products .btn-content {
    position: relative;
    z-index: 2; 
    /* Animación extra: rotación sutil del contenido */
    transition: transform 0.4s ease-in-out;
}

/* Rotación sutil del contenido al hacer hover */
.btn-upload-products:hover .btn-content {
    transform: rotate(1deg);
}
.spinner {
  animation: spin 1s linear infinite;
  vertical-align: middle;
  margin-right: 8px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>