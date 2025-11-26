<template>
  <div class="app-container">
    <!-- Header -->
    <header class="header">
      <h1 class="app-title">Gestión de Dueños</h1>
      <button @click="logout" class="btn-logout">Salir</button>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Crear Dueño Button -->
      <button @click="openCreateModal" class="btn-create">
        + Crear Dueño
      </button>

      <!-- Search Bar -->
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por nombre o correo..."
          class="search-input"
        />
      </div>

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

          <!-- CAMPO CANTIDAD BARES BIEN ENVUELTO -->
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

          <!-- CAMPO BARES DESHABILITADO BIEN ENVUELTO -->
          <div class="form-group">
      <label>Cantidad de Bares (puedes modificar manualmente)</label>
  <input
    v-model.number="editingDueno.cantidad_bares"
    type="number"
    min="0"
    class="input-editable"
  />
  <small style="color: #28a745; margin-top: 5px; display: block; font-weight: 600;">
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
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useGestorPrincipalStore } from '@/stores/gestorPrincipal'
import { API_BASE_URL } from '@/config/api'
import axios from 'axios'
import Swal from 'sweetalert2'

// Router y Store
const router = useRouter()
const gestorStore = useGestorPrincipalStore()

// Datos reactivos
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
    await fetchDuenos() // recargar lista
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
// Cargar dueños al iniciar
onMounted(async () => {
  await fetchDuenos()
})

// Métodos
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
    cantidad_bares: 0,  // ✅ Valor por defecto explícito
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
    // ✅ Asegúrate de que cantidad_bares sea un número
    const payload = {
      ...newDueno.value,
      cantidad_bares: Number(newDueno.value.cantidad_bares) || 0
    }
    
    console.log('📤 Enviando:', payload)  // DEBUG
    
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


// LOGOUT SEGURO DEL GESTOR PRINCIPAL (DIEGO)
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
      // Borra TODO: gestor principal, dueños, etc.
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
.bares-count {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 1rem;
  display: inline-block;
  min-width: 40px;
  text-align: center;
}
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Header */
.header {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.app-title {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.btn-logout {
  background: white;
  color: #1e3c72;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-logout:hover {
  background: #f0f0f0;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Main Content */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.btn-create {
  background: #2a5298;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  margin-bottom: 2rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-create:hover {
  background: #1e3c72;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* Search */
.search-container {
  margin-bottom: 2rem;
}

.search-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #2a5298;
  box-shadow: 0 0 0 3px rgba(42, 82, 152, 0.1);
}

/* Cards Grid */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.admin-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.admin-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.card-image {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: #f0f0f0;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 1.5rem;
}

.card-content h3 {
  color: #1e3c72;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.card-content p {
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 0.95rem;
}

.status-badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-inactive {
  background: #f8d7da;
  color: #721c24;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: #f8f9fa;
}

.btn-enter,
.btn-edit {
  flex: 1;
  padding: 0.7rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-enter {
  background: #2a5298;
  color: white;
}

.btn-enter:hover {
  background: #1e3c72;
}

.btn-edit {
  background: white;
  color: #2a5298;
  border: 2px solid #2a5298;
}

.btn-edit:hover {
  background: #2a5298;
  color: white;
}

.no-results {
  text-align: center;
  padding: 3rem;
  color: #666;
  font-size: 1.2rem;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(3px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-content h2 {
  color: #1e3c72;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
}

.form-group input {
  width: 100%;
  padding: 0.8rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #2a5298;
  box-shadow: 0 0 0 3px rgba(42, 82, 152, 0.1);
}

.input-disabled {
  background: #f0f0f0;
  cursor: not-allowed;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 0.8rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-weight: 500;
}

/* Toggle Button */
.toggle-container {
  margin-top: 0.5rem;
}

.toggle-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  width: 200px;
  height: 50px;
  border-radius: 25px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 1rem;
  padding: 0 1rem;
}

.toggle-active {
  background: #28a745;
  color: white;
  justify-content: flex-end;
}

.toggle-inactive {
  background: #dc3545;
  color: white;
  justify-content: flex-start;
}

.toggle-slider {
  position: absolute;
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s ease;
  left: 5px;
}

.toggle-active .toggle-slider {
  left: calc(100% - 45px);
}

.toggle-label {
  z-index: 1;
}

/* Modal Actions */
.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-cancel,
.btn-submit {
  flex: 1;
  padding: 0.8rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-cancel {
  background: #6c757d;
  color: white;
}

.btn-cancel:hover {
  background: #5a6268;
}

.btn-submit {
  background: #2a5298;
  color: white;
}

.btn-submit:hover {
  background: #1e3c72;
}

.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* Responsive */
@media (max-width: 768px) {
  .header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .cards-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    padding: 1.5rem;
  }
}
.btn-delete {
  flex: 1;
  padding: 0.7rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  background: #dc3545;
  color: white;
  transition: all 0.3s ease;
}

.btn-delete:hover {
  background: #c82333;
  transform: translateY(-2px);
}

/* Ajuste para que quepan los dos botones */
.card-actions {
  display: flex;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: #f8f9fa;
}
.input-editable {
  border: 2px solid #28a745 !important;
  background: #f8fff8 !important;
}
.input-editable:focus {
  border-color: #1e7e34 !important;
  box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.2) !important;
}
</style>