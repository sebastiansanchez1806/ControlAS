<template>
  <div class="app-container">
    <!-- Header -->
    <header class="header">
      <h1 class="app-title">Gestión de Dueños</h1>
      
      <div class="header-actions">
        <!-- Search Bar en Header -->
        <div class="search-container-header">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por nombre o correo..."
            class="search-input"
          />
        </div>
        
        <!-- Grupo de botones configuración y crear (juntos en mobile) -->
        <div class="buttons-group">
          <!-- Botón de configuración -->
          <button @click="toggleSettingsMenu" class="settings-btn" :class="{ active: isSettingsMenuOpen }">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
          </button>
          
          <!-- Botón Crear Dueño en Header -->
          <button @click="openCreateModal" class="btn-create-header">
            + Crear Dueño
          </button>
        </div>

        <button @click="logout" class="btn-logout">Salir</button>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Cards Grid -->
      <div class="cards-grid">
        <div
          v-for="dueno in filteredDuenos"
          :key="dueno.id"
          class="admin-card"
        >
          <div class="card-image">
            <img
              :src="dueno.imagen || 'https://via.placeholder.com/150'"
              :alt="dueno.nombre"
            />
          </div>
          <div class="card-content">
            <h3>{{ dueno.nombre }}</h3>
            <p><strong>ID:</strong> {{ dueno.id }}</p>
            <p><strong>Teléfono:</strong> {{ dueno.telefono }}</p>
            <p><strong>Correo:</strong> {{ dueno.correo }}</p>
            <p>
              <strong>Bares:</strong>
              <span class="bares-count">{{ dueno.cantidad_bares }}</span>
            </p>
            <p>
              <strong>Estado:</strong>
              <span
                :class="[
                  'status-badge',
                  dueno.estado === 'activo' ? 'status-active' : 'status-inactive'
                ]"
              >
                {{ dueno.estado || 'inactivo' }}
              </span>
            </p>
          </div>
          <div class="card-actions">
            <button @click="openBaresModal(dueno)" class="btn-enter">Entrar</button>
            <button @click="openEditModal(dueno)" class="btn-edit">Editar</button>
            <button @click="confirmDelete(dueno)" class="btn-delete">Eliminar</button>
          </div>
        </div>
      </div>

      <!-- No results message -->
      <div v-if="filteredDuenos.length === 0" class="no-results">
        No se encontraron dueños
      </div>
    </main>

    <!-- Modal Menu de Configuración -->
    <transition name="modal">
      <div v-if="isSettingsMenuOpen" class="modal-overlay" @click.self="toggleSettingsMenu">
        <div class="options-modal">
          <div class="modal-header">
            <h3>Configuración</h3>
            <button @click="toggleSettingsMenu" class="close-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="options-body">
            <button 
              v-for="option in settingsOptions" 
              :key="option.id"
              @click="handleSettingsOptionClick(option.id)"
              class="menu-option"
            >
              <component :is="option.icon" />
              <span>{{ option.label }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="arrow-icon">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal de Actualización de Configuración -->
    <transition name="modal">
      <div v-if="activeSettingsModal" class="modal-overlay" @click.self="closeSettingsModal">
        <div class="modal-content settings-modal">
          <div class="modal-header">
            <h3>{{ getSettingsModalTitle() }}</h3>
            <button @click="closeSettingsModal" class="close-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <!-- Mensaje de error -->
            <div v-if="settingsError" class="alert alert-error">{{ settingsError }}</div>

            <!-- Campo para nuevo nombre -->
            <div v-if="activeSettingsModal === 'name'" class="form-group">
              <label>Nuevo nombre</label>
              <input 
                v-model="settingsNewValue" 
                type="text" 
                placeholder="Ingresa tu nuevo nombre"
                class="form-input"
                @keyup.enter="handleSettingsSubmit"
              />
            </div>

            <!-- Campo para nuevo correo -->
            <div v-if="activeSettingsModal === 'email'" class="form-group">
              <label>Nuevo correo</label>
              <input 
                v-model="settingsNewValue" 
                type="email" 
                placeholder="Ingresa tu nuevo correo"
                class="form-input"
                @keyup.enter="handleSettingsSubmit"
              />
            </div>

            <!-- Campos para nueva contraseña -->
            <div v-if="activeSettingsModal === 'password'">
              <div class="form-group">
                <label>Nueva contraseña</label>
                <input 
                  v-model="settingsNewValue" 
                  type="password" 
                  placeholder="Ingresa tu nueva contraseña"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label>Confirmar contraseña</label>
                <input 
                  v-model="settingsConfirmValue" 
                  type="password" 
                  placeholder="Confirma tu nueva contraseña"
                  class="form-input"
                  @keyup.enter="handleSettingsSubmit"
                />
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="closeSettingsModal" class="btn btn-secondary">Cancelar</button>
            <button @click="handleSettingsSubmit" :disabled="settingsLoading" class="btn btn-primary">
              {{ settingsLoading ? 'Guardando...' : 'Actualizar' }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal Crear Dueño -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="closeCreateModal">
      <div class="modal-content" @click.stop>
        <h2>Crear Nuevo Dueño</h2>
        <form @submit.prevent="createDueno">
          <div class="form-group">
            <label>Nombre</label>
            <input v-model="newDueno.nombre" type="text" required />
          </div>
          <div class="form-group">
            <label>Teléfono</label>
            <input v-model="newDueno.telefono" type="tel" required />
          </div>
          <div class="form-group">
            <label>Correo Electrónico</label>
            <input v-model="newDueno.correo" type="email" required />
          </div>
          <div class="form-group">
            <label>Contraseña</label>
            <input v-model="newDueno.contraseña" type="password" required />
          </div>

          <div class="form-group">
            <label>Cantidad de Bares (inicial)</label>
            <input
              v-model.number="newDueno.cantidad_bares"
              type="number"
              min="0"
              placeholder="Ej: 2"
            />
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeCreateModal" class="btn-cancel">
              Cancelar
            </button>
            <button type="submit" :disabled="isLoading" class="btn-submit">
              {{ isLoading ? 'Creando...' : 'Crear Dueño' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar Dueño -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal-content" @click.stop>
        <h2>Editar Dueño</h2>
        <form @submit.prevent="updateDueno">
          <div class="form-group">
            <label>Nombre</label>
            <input v-model="editingDueno.nombre" type="text" required />
          </div>
          <div class="form-group">
            <label>Teléfono</label>
            <input v-model="editingDueno.telefono" type="tel" required />
          </div>
          <div class="form-group">
            <label>Correo Electrónico</label>
            <input v-model="editingDueno.correo" type="email" required />
          </div>

          <div class="form-group">
            <label>Cantidad de Bares (puedes modificar manualmente)</label>
            <input
              v-model.number="editingDueno.cantidad_bares"
              type="number"
              min="0"
              class="input-editable"
            />
            <small style="color: #00ff7f; margin-top: 5px; display: block; font-weight: 600;">
              Puedes cambiarlo aquí o dejar que se actualice automáticamente con los bares reales
            </small>
          </div>

          <div class="form-group">
            <label>Estado</label>
            <div class="toggle-container">
              <button
                type="button"
                @click="toggleStatus"
                :class="[
                  'toggle-button',
                  editingDueno.estado === 'activo' ? 'toggle-active' : 'toggle-inactive'
                ]"
              >
                <span class="toggle-slider"></span>
                <span class="toggle-label">
                  {{ editingDueno.estado === 'activo' ? 'Activo' : 'Inactivo' }}
                </span>
              </button>
            </div>
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeEditModal" class="btn-cancel">
              Cancelar
            </button>
            <button type="submit" class="btn-submit">
              Guardar Cambios
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Locales del Dueño -->
    <div v-if="showBaresModal" class="modal-overlay" @click.self="closeBaresModal">
      <div class="modal-content modal-bares" @click.stop>
        <h2>Locales de {{ selectedDueno?.nombre }}</h2>

        <div v-if="isLoadingBares" class="loading">
          Cargando locales...
        </div>

        <div v-else-if="baresDelDueno.length === 0" class="no-results">
          Este dueño aún no tiene locales registrados
        </div>

        <div v-else class="bares-list">
          <div v-for="bar in baresDelDueno" :key="bar.id" class="bar-item">
            <div class="bar-image">
              <img :src="bar.imagen || 'https://via.placeholder.com/100'" :alt="bar.nombre" />
            </div>
            <div class="bar-info">
              <h4>{{ bar.nombre }}</h4>
              <p><strong>ID:</strong> {{ bar.id }}</p>
              <p><strong>Ubicación:</strong> {{ bar.ubicacion }}</p>
              <p><strong>Tipo:</strong> {{ bar.tipo === 'burdel' ? 'Burdel' : 'Bar' }}</p>
            </div>
            <div class="bar-action">
              <button @click="entrarAlLocal(bar.id)" class="btn-enter-small">
                Entrar
              </button>
            </div>
          </div>
        </div>

        <div class="modal-actions">
          <button @click="closeBaresModal" class="btn-cancel">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { useGestorPrincipalStore } from '@/stores/gestorPrincipal'
import { API_BASE_URL } from '@/config/api'
import axios from 'axios'
import Swal from 'sweetalert2'

// Router y Store
const router = useRouter()
const gestorStore = useGestorPrincipalStore()

// Datos reactivos generales
const showCreateModal = ref(false)
const showEditModal = ref(false)
const isLoading = ref(false)
const searchQuery = ref('')
const errorMessage = ref('')
const duenos = ref([])
const newDueno = ref({
  nombre: '',
  telefono: '',
  correo: '',
  contraseña: '',
  cantidad_bares: 0,
  estado: 'activo'
})
const editingDueno = ref(null)

// Variables para el modal de bares
const showBaresModal = ref(false)
const selectedDueno = ref(null)
const baresDelDueno = ref([])
const isLoadingBares = ref(false)

// Variables para configuración
const isSettingsMenuOpen = ref(false)
const activeSettingsModal = ref(null)
const settingsNewValue = ref('')
const settingsConfirmValue = ref('')
const settingsError = ref('')
const settingsLoading = ref(false)
const currentPassword = ref('')
const currentGestorData = ref({
  nombre: '',
  correo: ''
})

// Iconos SVG para configuración
const UserIcon = () => h('svg', {
  xmlns: 'http://www.w3.org/2000/svg',
  width: 20,
  height: 20,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 2,
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('path', { d: 'M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2' }),
  h('circle', { cx: 12, cy: 7, r: 4 })
])

const MailIcon = () => h('svg', {
  xmlns: 'http://www.w3.org/2000/svg',
  width: 20,
  height: 20,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 2,
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('rect', { width: 20, height: 16, x: 2, y: 4, rx: 2 }),
  h('path', { d: 'm22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7' })
])

const LockIcon = () => h('svg', {
  xmlns: 'http://www.w3.org/2000/svg',
  width: 20,
  height: 20,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 2,
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('rect', { width: 18, height: 11, x: 3, y: 11, rx: 2, ry: 2 }),
  h('path', { d: 'M7 11V7a5 5 0 0 1 10 0v4' })
])

const settingsOptions = [
  { id: 'name', label: 'Actualizar nombre', icon: UserIcon },
  { id: 'email', label: 'Actualizar correo', icon: MailIcon },
  { id: 'password', label: 'Actualizar contraseña', icon: LockIcon }
]

// Filtros
const filteredDuenos = computed(() => {
  if (!searchQuery.value) return duenos.value
  const query = searchQuery.value.toLowerCase().trim()
  return duenos.value.filter(d =>
    d.nombre.toLowerCase().includes(query) ||
    d.correo.toLowerCase().includes(query) ||
    d.telefono.includes(query)
  )
})

// Cargar datos al iniciar
onMounted(async () => {
  await fetchDuenos()
  await loadGestorData()
})

const loadGestorData = async () => {
  try {
    const response = await axios.get('/api/gestor_principal')
    currentGestorData.value = {
      nombre: response.data.nombre,
      correo: response.data.correo
    }
  } catch (err) {
    console.error('Error cargando datos del gestor:', err)
  }
}

// Métodos de configuración
const toggleSettingsMenu = () => {
  isSettingsMenuOpen.value = !isSettingsMenuOpen.value
}

const handleSettingsOptionClick = async (optionId) => {
  const { value: password } = await Swal.fire({
    title: 'Verificación de seguridad',
    input: 'password',
    inputLabel: 'Ingresa tu contraseña actual',
    inputPlaceholder: 'Contraseña actual',
    showCancelButton: true,
    confirmButtonText: 'Continuar',
    cancelButtonText: 'Cancelar',
    inputValidator: (value) => {
      if (!value) return '¡Debes ingresar tu contraseña actual!'
    }
  })

  if (!password) return

  currentPassword.value = password
  activeSettingsModal.value = optionId
  isSettingsMenuOpen.value = false
  resetSettingsForm()
}

const closeSettingsModal = () => {
  activeSettingsModal.value = null
  resetSettingsForm()
}

const resetSettingsForm = () => {
  settingsNewValue.value = ''
  settingsConfirmValue.value = ''
  settingsError.value = ''
  settingsLoading.value = false
}

const getSettingsModalTitle = () => {
  const titles = {
    name: 'Actualizar Nombre',
    email: 'Actualizar Correo',
    password: 'Actualizar Contraseña'
  }
  return titles[activeSettingsModal.value] || ''
}

const handleSettingsSubmit = async () => {
  settingsError.value = ''
  settingsLoading.value = true

  if (!settingsNewValue.value.trim()) {
    settingsError.value = 'Debes ingresar el nuevo valor'
    settingsLoading.value = false
    return
  }

  // Validaciones frontend
  if (activeSettingsModal.value === 'password') {
    if (settingsNewValue.value !== settingsConfirmValue.value) {
      settingsError.value = 'Las contraseñas no coinciden'
      settingsLoading.value = false
      return
    }
    if (settingsNewValue.value.length < 6) {
      settingsError.value = 'La contraseña debe tener al menos 6 caracteres'
      settingsLoading.value = false
      return
    }
  }

  if (activeSettingsModal.value === 'email') {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(settingsNewValue.value)) {
      settingsError.value = 'Ingresa un correo electrónico válido'
      settingsLoading.value = false
      return
    }
  }

  try {
    let response

    if (activeSettingsModal.value === 'password') {
      response = await axios.put('/api/gestor_principal/password', {
        current_password: currentPassword.value,
        new_password: settingsNewValue.value
      })
    } else {
      const payload = {}
      if (activeSettingsModal.value === 'name') payload.nombre = settingsNewValue.value
      if (activeSettingsModal.value === 'email') payload.correo = settingsNewValue.value

      response = await axios.put('/api/gestor_principal/update', payload, {
        params: { current_password: currentPassword.value }
      })

      if (activeSettingsModal.value === 'name') currentGestorData.value.nombre = settingsNewValue.value
      if (activeSettingsModal.value === 'email') currentGestorData.value.correo = settingsNewValue.value
    }

    closeSettingsModal()

    Swal.fire({
      icon: 'success',
      title: '¡Actualización exitosa!',
      text: response.data.message || 'Los cambios se han guardado correctamente',
      confirmButtonText: 'Perfecto',
      confirmButtonColor: '#ff69b4',
      timer: 3000,
      timerProgressBar: true
    })

  } catch (err) {
    const msg = err.response?.data?.detail || 'Error al guardar los cambios'
    settingsError.value = msg
  } finally {
    settingsLoading.value = false
  }
}

// Métodos de dueños
const confirmDelete = (dueno) => {
  Swal.fire({
    title: `¿Eliminar a ${dueno.nombre}?`,
    text: "Esta acción no se puede deshacer",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Sí, eliminar',
    cancelButtonText: 'Cancelar'
  }).then((result) => {
    if (result.isConfirmed) {
      deleteDueno(dueno.id)
    }
  })
}

const deleteDueno = async (id) => {
  try {
    await axios.delete(`${API_BASE_URL}/duenos/${id}`)
    await fetchDuenos()
    Swal.fire({
      title: '¡Eliminado!',
      text: 'El dueño ha sido eliminado correctamente',
      icon: 'success',
      timer: 2000,
      timerProgressBar: true,
      showConfirmButton: false
    })
  } catch (error) {
    console.error(error)
    Swal.fire(
      'Error',
      error.response?.data?.detail || 'No se pudo eliminar el dueño',
      'error'
    )
  }
}

const fetchDuenos = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/duenos`)
    duenos.value = response.data
  } catch (error) {
    Swal.fire('Error', 'No se pudieron cargar los dueños', 'error')
  }
}

const openCreateModal = () => {
  showCreateModal.value = true
  errorMessage.value = ''
  newDueno.value = { 
    nombre: '', 
    telefono: '', 
    correo: '', 
    contraseña: '', 
    cantidad_bares: 0,
    estado: 'activo' 
  }
}

const closeCreateModal = () => {
  showCreateModal.value = false
  errorMessage.value = ''
}

const createDueno = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const payload = {
      ...newDueno.value,
      cantidad_bares: Number(newDueno.value.cantidad_bares) || 0
    }
    
    await axios.post(`${API_BASE_URL}/duenos`, payload)
    await fetchDuenos()
    closeCreateModal()
    Swal.fire('¡Éxito!', 'Dueño creado correctamente', 'success')
  } catch (error) {
    const detalle = error.response?.data?.detail || ''
    if (detalle.includes('nombre')) errorMessage.value = 'Ya existe un dueño con ese nombre.'
    else if (detalle.includes('correo')) errorMessage.value = 'Este correo ya está registrado.'
    else errorMessage.value = detalle || 'Error al crear el dueño.'
  } finally {
    isLoading.value = false
  }
}

const openEditModal = (dueno) => {
  editingDueno.value = { ...dueno }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  editingDueno.value = null
}

const toggleStatus = () => {
  if (editingDueno.value) {
    editingDueno.value.estado = editingDueno.value.estado === 'activo' ? 'inactivo' : 'activo'
  }
}

const updateDueno = async () => {
  if (!editingDueno.value) return

  try {
    await axios.put(`${API_BASE_URL}/duenos/${editingDueno.value.id}`, editingDueno.value)
    await fetchDuenos()
    closeEditModal()
    Swal.fire('¡Actualizado!', 'Dueño modificado correctamente', 'success')
  } catch (error) {
    const detalle = error.response?.data?.detail || ''
    if (detalle.includes('nombre')) errorMessage.value = 'Ya existe otro dueño con ese nombre.'
    else if (detalle.includes('correo')) errorMessage.value = 'Este correo ya está en uso.'
    else errorMessage.value = detalle || 'Error al guardar cambios.'
  }
}

const openBaresModal = async (dueno) => {
  selectedDueno.value = dueno
  showBaresModal.value = true
  isLoadingBares.value = true
  baresDelDueno.value = []

  try {
    const response = await axios.get(`${API_BASE_URL}/bares/dueno/${dueno.id}`)
    baresDelDueno.value = response.data.bares || []
  } catch (error) {
    console.error('Error cargando bares:', error)
    Swal.fire('Error', 'No se pudieron cargar los locales de este dueño', 'error')
    baresDelDueno.value = []
  } finally {
    isLoadingBares.value = false
  }
}

const closeBaresModal = () => {
  showBaresModal.value = false
  selectedDueno.value = null
  baresDelDueno.value = []
}

const entrarAlLocal = (barId) => {
  closeBaresModal()
  router.push(`/info_locales/${barId}`)
}

const logout = () => {
  Swal.fire({
    title: '¿Cerrar sesión?',
    text: 'Vas a salir del panel de gestor principal',
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#d33',
    cancelButtonColor: '#3085d6',
    confirmButtonText: 'Sí, salir',
    cancelButtonText: 'Cancelar'
  }).then((result) => {
    if (result.isConfirmed) {
      gestorStore.logout()
      localStorage.clear()
      Swal.fire('¡Sesión cerrada!', '', 'success').then(() => {
        router.push('/login_gestor_principal_diego')
      })
    }
  })
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* ========== SETTINGS BUTTON ========== */
.settings-btn {
  background: #fff;
  border: 2px solid #000;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #000;
  flex-shrink: 0;
}

.settings-btn:hover {
  background: #ff69b4;
  border-color: #ff69b4;
  color: #fff;
  transform: rotate(90deg);
}

.settings-btn.active {
  background: #000;
  color: #fff;
}

/* ========== OPTIONS MODAL ========== */
.options-modal {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 3px solid #000;
  animation: scaleIn 0.3s ease;
}

.menu-option {
  width: 100%;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  border: 2px solid #000;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #000;
  font-size: 15px;
  text-align: left;
  font-weight: 600;
  min-height: 60px;
}

.menu-option span {
  flex: 1;
  line-height: 1.3;
}

.arrow-icon {
  opacity: 0.5;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.menu-option:hover {
  background: #ff69b4;
  color: #fff;
  border-color: #ff69b4;
  transform: translateX(8px);
}

.menu-option:hover .arrow-icon {
  opacity: 1;
  transform: translateX(4px);
}

.options-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* ========== SETTINGS MODAL ========== */
.settings-modal {
  max-width: 500px;
}

.alert {
  padding: 12px 14px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
  line-height: 1.4;
}

.alert-error {
  background: #ffe0e0;
  color: #c00;
  border: 2px solid #c00;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #000;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #4169e1;
  box-shadow: 0 0 0 3px rgba(65, 105, 225, 0.1);
}

.btn {
  padding: 14px 20px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid #000;
  min-height: 48px;
  flex: 1;
  max-width: 150px;
}

.btn-secondary {
  background: #fff;
  color: #000;
}

.btn-secondary:hover {
  background: #f5f5f5;
}

.btn-primary {
  background: #ff69b4;
  color: #fff;
  border-color: #ff69b4;
}

.btn-primary:hover {
  background: #ff1493;
  border-color: #ff1493;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ========== ANIMATIONS ========== */
@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-enter-active, .modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-from .options-modal,
.modal-enter-from .modal-content {
  transform: scale(0.9);
}

/* ========== SIN RESULTADOS ========== */
.no-results {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.3rem;
  font-weight: 500;
}

/* ========== MODAL OVERLAY ========== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  backdrop-filter: blur(8px);
  animation: fadeInOverlay 0.3s ease-out;
}

@keyframes fadeInOverlay {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* ========== MODAL CONTENIDO ========== */
.modal-content {
  background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
  border-radius: 20px;
  padding: 2.5rem;
  width: 90%;
  max-width: 550px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 20, 147, 0.3);
  border: 2px solid rgba(255, 20, 147, 0.2);
  animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-content h2 {
  color: #ffffff;
  margin-bottom: 2rem;
  font-size: 1.8rem;
  text-align: center;
  font-weight: 800;
  background: linear-gradient(135deg, #ff1493, #00bfff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.modal-header {
  padding: 20px;
  border-bottom: 2px solid #000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 10;
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  color: #000;
  line-height: 1.2;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: #000;
  transition: all 0.2s ease;
  min-width: 40px;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.close-btn:hover {
  color: #ff69b4;
  background: rgba(255, 105, 180, 0.1);
  transform: rotate(90deg);
}

.modal-body {
  padding: 20px;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 2px solid #000;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  position: sticky;
  bottom: 0;
  background: #fff;
  border-radius: 0 0 16px 16px;
}

/* ========== SCROLLBAR PERSONALIZADO ========== */
.modal-content::-webkit-scrollbar,
.bares-list::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track,
.bares-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
}

.modal-content::-webkit-scrollbar-thumb,
.bares-list::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #ff1493, #00bfff);
  border-radius: 10px;
}

/* ========== FORM GROUP ========== */
.form-group {
  margin-bottom: 1.8rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.7rem;
  color: #00bfff;
  font-weight: 600;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input {
  width: 100%;
  padding: 1rem 1.2rem;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  font-size: 1rem;
  color: white;
  transition: all 0.3s ease;
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-group input:focus {
  outline: none;
  border-color: #ff1493;
  background: rgba(0, 0, 0, 0.6);
  box-shadow: 0 0 0 3px rgba(255, 20, 147, 0.2), 0 0 20px rgba(255, 20, 147, 0.2);
}

.form-group small {
  color: #00ff7f;
  margin-top: 0.5rem;
  display: block;
  font-weight: 600;
  font-size: 0.85rem;
}

.input-editable {
  border: 2px solid #00ff7f !important;
  background: rgba(0, 255, 127, 0.1) !important;
}

.input-editable:focus {
  border-color: #00ff7f !important;
  box-shadow: 0 0 0 3px rgba(0, 255, 127, 0.2) !important;
}

/* ========== ERROR MESSAGE ========== */
.error-message {
  background: linear-gradient(135deg, rgba(255, 20, 147, 0.2), rgba(255, 20, 147, 0.1));
  color: #ff69b4;
  padding: 1rem 1.2rem;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  font-weight: 600;
  border: 2px solid rgba(255, 20, 147, 0.4);
  box-shadow: 0 0 15px rgba(255, 20, 147, 0.2);
}

/* ========== TOGGLE BUTTON ========== */
.toggle-container {
  margin-top: 0.8rem;
}

.toggle-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  width: 220px;
  height: 55px;
  border-radius: 30px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  font-weight: 700;
  font-size: 1.05rem;
  padding: 0 1.2rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.toggle-active {
  background: linear-gradient(135deg, #00ff7f, #00cc66);
  color: #000;
  justify-content: flex-end;
  box-shadow: 0 6px 20px rgba(0, 255, 127, 0.5);
}

.toggle-inactive {
  background: linear-gradient(135deg, #ff1493, #dc143c);
  color: white;
  justify-content: flex-start;
  box-shadow: 0 6px 20px rgba(255, 20, 147, 0.5);
}

.toggle-slider {
  position: absolute;
  width: 45px;
  height: 45px;
  background: white;
  border-radius: 50%;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  left: 5px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.toggle-active .toggle-slider {
  left: calc(100% - 50px);
}

.toggle-label {
  z-index: 1;
  font-weight: 800;
}

/* ========== ACCIONES DE MODAL ========== */
.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2.5rem;
}

.btn-cancel,
.btn-submit {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.btn-cancel {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn-cancel:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.btn-submit {
  background: linear-gradient(135deg, #ff1493, #ff69b4);
  color: white;
  box-shadow: 0 6px 20px rgba(255, 20, 147, 0.5);
}

.btn-submit:hover {
  background: linear-gradient(135deg, #ff69b4, #ff1493);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 20, 147, 0.7);
}

.btn-submit:disabled {
  background: rgba(255, 255, 255, 0.2);
  cursor: not-allowed;
  opacity: 0.5;
  transform: none;
  box-shadow: none;
}

/* ========== MODAL DE BARES ========== */
.modal-bares {
  max-width: 850px;
  max-height: 88vh;
  width: 92%;
}

.modal-bares h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
}

.bares-list {
  overflow-y: auto;
  max-height: 58vh;
  padding-right: 12px;
}

.bar-item {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(15, 52, 96, 0.6));
  border-radius: 16px;
  padding: 1.3rem;
  margin-bottom: 1.2rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 20, 147, 0.2);
  backdrop-filter: blur(10px);
}

.bar-item:hover {
  transform: translateX(8px);
  box-shadow: 0 10px 30px rgba(255, 20, 147, 0.4);
  border-color: rgba(255, 20, 147, 0.5);
}

.bar-image {
  flex-shrink: 0;
  width: 100px;
  height: 100px;
  border-radius: 12px;
  overflow: hidden;
  margin-right: 1.5rem;
  background: linear-gradient(135deg, #1a1a2e, #0f3460);
  border: 2px solid rgba(255, 20, 147, 0.3);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.bar-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.bar-item:hover .bar-image img {
  transform: scale(1.1);
}

.bar-info {
  flex: 1;
}

.bar-info h4 {
  margin: 0 0 0.8rem 0;
  color: #ff1493;
  font-size: 1.4rem;
  font-weight: 700;
}

.bar-info p {
  margin: 0.5rem 0;
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
}

.bar-info strong {
  color: #00bfff;
  font-weight: 600;
}

.bar-action {
  margin-left: 1.2rem;
}

.btn-enter-small {
  background: linear-gradient(135deg, #00bfff, #0080ff);
  color: white;
  border: none;
  padding: 0.9rem 1.8rem;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 4px 15px rgba(0, 191, 255, 0.4);
}

.btn-enter-small:hover {
  background: linear-gradient(135deg, #0080ff, #00bfff);
  transform: scale(1.08) translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 191, 255, 0.6);
}

/* ========== LOADING ========== */
.loading {
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.2rem;
  font-weight: 500;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
  color: #ffffff;
}

/* ========== HEADER STICKY ========== */
.header {
  background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
  padding: 1.5rem 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 20px rgba(255, 20, 147, 0.3);
  border-bottom: 2px solid rgba(255, 20, 147, 0.2);
  backdrop-filter: blur(10px);
  position: sticky;
  top: 0;
  z-index: 100;
  gap: 2rem;
}

.app-title {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ff1493, #00bfff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 1.5px;
  text-shadow: 0 0 30px rgba(255, 20, 147, 0.5);
  white-space: nowrap;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  flex: 1;
  justify-content: flex-end;
}

.buttons-group {
  display: flex;
  gap: 1.2rem;
  align-items: center;
}

/* ========== SEARCH EN HEADER ========== */
.search-container-header {
  flex: 1;
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 0.9rem 1.5rem;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(255, 20, 147, 0.3);
  border-radius: 25px;
  font-size: 0.95rem;
  color: white;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.search-input:focus {
  outline: none;
  border-color: #ff1493;
  background: rgba(0, 0, 0, 0.6);
  box-shadow: 0 0 0 4px rgba(255, 20, 147, 0.2), 0 0 20px rgba(255, 20, 147, 0.3);
  transform: translateY(-2px);
}

/* ========== BOTÓN CREAR EN HEADER ========== */
.btn-create-header {
  background: linear-gradient(135deg, #00bfff, #0080ff);
  color: white;
  border: none;
  padding: 0.9rem 1.8rem;
  border-radius: 25px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(0, 191, 255, 0.5);
  text-transform: uppercase;
  letter-spacing: 1px;
  white-space: nowrap;
}

.btn-create-header:hover {
  background: linear-gradient(135deg, #0080ff, #00bfff);
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 6px 20px rgba(0, 191, 255, 0.7);
}

.btn-create-header:active {
  transform: translateY(-1px) scale(1.02);
}

/* ========== BOTÓN LOGOUT ========== */
.btn-logout {
  background: linear-gradient(135deg, #ff1493, #ff69b4);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.2);
  padding: 0.9rem 1.8rem;
  border-radius: 25px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  text-transform: uppercase;
  letter-spacing: 1px;
  box-shadow: 0 4px 15px rgba(255, 20, 147, 0.4);
  white-space: nowrap;
}

.btn-logout:hover {
  background: linear-gradient(135deg, #ff69b4, #ff1493);
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 6px 20px rgba(255, 20, 147, 0.6);
  border-color: rgba(255, 255, 255, 0.4);
}

/* ========== CONTENIDO PRINCIPAL ========== */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2.5rem 2rem;
}

/* ========== GRID DE CARDS ========== */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== CARD DE DUEÑO ========== */
.admin-card {
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(15, 52, 96, 0.9) 100%);
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 20, 147, 0.2);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  position: relative;
}

.admin-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ff1493, #00bfff, #ff1493);
  background-size: 200% 100%;
  animation: shimmer 3s linear infinite;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 1;
}

.admin-card:hover::before {
  opacity: 1;
}

@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.admin-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 15px 40px rgba(255, 20, 147, 0.4), 0 0 0 1px rgba(255, 20, 147, 0.4);
}

.card-image {
  width: 100%;
  height: 220px;
  overflow: hidden;
  background: linear-gradient(135deg, #1a1a2e, #0f3460);
  position: relative;
}

.card-image::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.5) 100%);
  pointer-events: none;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.admin-card:hover .card-image img {
  transform: scale(1.1);
}

.card-content {
  padding: 1.8rem;
}

.card-content h3 {
  color: #ffffff;
  margin-bottom: 1.2rem;
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ff1493, #ff69b4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.card-content p {
  margin-bottom: 0.8rem;
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
  line-height: 1.6;
}

.card-content strong {
  color: #00bfff;
  font-weight: 600;
}

/* ========== CONTADOR DE BARES ========== */
.bares-count {
  background: linear-gradient(135deg, #ff1493, #ff69b4);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-weight: 800;
  font-size: 1.05rem;
  display: inline-block;
  min-width: 45px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(255, 20, 147, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

/* ========== BADGES DE ESTADO ========== */
.status-badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: 2px solid;
}

.status-active {
  background: linear-gradient(135deg, rgba(0, 255, 127, 0.2), rgba(0, 255, 127, 0.1));
  color: #00ff7f;
  border-color: #00ff7f;
  box-shadow: 0 0 15px rgba(0, 255, 127, 0.3);
}

.status-inactive {
  background: linear-gradient(135deg, rgba(255, 20, 147, 0.2), rgba(255, 20, 147, 0.1));
  color: #ff1493;
  border-color: #ff1493;
  box-shadow: 0 0 15px rgba(255, 20, 147, 0.3);
}

/* ========== ACCIONES DE CARD ========== */
.card-actions {
  display: flex;
  gap: 0.8rem;
  padding: 1.2rem 1.8rem;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

.card-actions button {
  flex: 1;
  padding: 0.9rem 1rem;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-enter {
  background: linear-gradient(135deg, #00ff7f, #00cc66);
  color: #000;
  box-shadow: 0 4px 15px rgba(0, 255, 127, 0.4);
}

.btn-enter:hover {
  background: linear-gradient(135deg, #00cc66, #00ff7f);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 255, 127, 0.6);
}

.btn-edit {
  background: rgba(0, 191, 255, 0.15);
  color: #00bfff;
  border: 2px solid #00bfff;
  box-shadow: 0 4px 15px rgba(0, 191, 255, 0.3);
}

.btn-edit:hover {
  background: linear-gradient(135deg, #00bfff, #0080ff);
  color: white;
  border-color: transparent;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 191, 255, 0.6);
}

.btn-delete {
  background: linear-gradient(135deg, #ff1493, #dc143c);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 20, 147, 0.4);
}

.btn-delete:hover {
  background: linear-gradient(135deg, #dc143c, #ff1493);
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(255, 20, 147, 0.6);
}

/* ========== RESPONSIVE DESIGN ========== */
@media (max-width: 1200px) {
  .header {
    padding: 1.3rem 2rem;
  }
  
  .search-container-header {
    max-width: 300px;
  }
}

@media (max-width: 1024px) {
  .cards-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }
  
  .header {
    flex-wrap: wrap;
    gap: 1.5rem;
  }
  
  .app-title {
    font-size: 1.8rem;
  }
  
  .header-actions {
    flex-wrap: wrap;
    width: 100%;
    gap: 1rem;
  }
  
  .search-container-header {
    max-width: 100%;
    flex: 1 1 100%;
    order: 3;
  }
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1.2rem;
    text-align: center;
    padding: 1.5rem;
  }

  .app-title {
    font-size: 1.6rem;
    width: 100%;
  }

  .header-actions {
    flex-direction: column;
    width: 100%;
    gap: 1rem;
  }
  
  .buttons-group {
    width: 100%;
    flex-direction: row;
    justify-content: center;
  }
  
  .search-container-header {
    max-width: 100%;
    order: -1;
  }

  .btn-create-header,
  .btn-logout {
    width: 100%;
    padding: 1rem 1.5rem;
  }

  .settings-btn {
    width: 48px;
    height: 48px;
  }

  .main-content {
    padding: 2rem 1.2rem;
  }

  .cards-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .card-actions {
    flex-direction: column;
    gap: 0.8rem;
  }

  .card-actions button {
    width: 100%;
  }

  .modal-content {
    width: 95%;
    padding: 2rem 1.5rem;
    max-height: 95vh;
  }

  .modal-content h2 {
    font-size: 1.5rem;
  }

  .modal-actions {
    flex-direction: column;
    gap: 1rem;
  }

  .btn-cancel,
  .btn-submit {
    width: 100%;
  }

  .modal-bares {
    width: 95%;
    max-height: 92vh;
  }

  .bares-list {
    max-height: 55vh;
  }

  .bar-item {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }

  .bar-image {
    margin-right: 0;
    margin-bottom: 1.2rem;
    width: 120px;
    height: 120px;
  }

  .bar-action {
    margin-left: 0;
    margin-top: 1.2rem;
    width: 100%;
  }

  .btn-enter-small {
    width: 100%;
  }

  .toggle-button {
    width: 100%;
    max-width: 220px;
  }

  /* Settings responsive */
  .modal-overlay {
    padding: 0;
    align-items: flex-end;
  }

  .options-modal,
  .settings-modal {
    border-radius: 24px 24px 0 0;
    max-width: 100%;
    width: 100%;
    max-height: 90vh;
    border: none;
    border-top: 3px solid #000;
  }

  .modal-header {
    padding: 18px 16px;
    border-radius: 24px 24px 0 0;
  }

  .modal-header h3 {
    font-size: 18px;
  }

  .options-body {
    padding: 16px;
    gap: 12px;
  }

  .menu-option {
    padding: 16px 18px;
    font-size: 15px;
    gap: 12px;
    min-height: 64px;
  }

  .btn {
    min-height: 52px;
    flex: 1;
    max-width: none;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 1.2rem 1rem;
  }

  .app-title {
    font-size: 1.4rem;
  }

  .main-content {
    padding: 1.5rem 1rem;
  }

  .btn-create-header,
  .btn-logout {
    font-size: 0.9rem;
    padding: 0.9rem 1.3rem;
  }

  .search-input {
    padding: 0.85rem 1.2rem;
    font-size: 0.9rem;
  }

  .card-content {
    padding: 1.5rem;
  }

  .card-content h3 {
    font-size: 1.3rem;
  }

  .modal-content {
    padding: 1.8rem 1.2rem;
  }

  .modal-content h2 {
    font-size: 1.3rem;
  }

  .form-group input {
    padding: 0.9rem 1rem;
    font-size: 0.95rem;
  }

  .settings-btn {
    width: 44px;
    height: 44px;
  }
}
</style>