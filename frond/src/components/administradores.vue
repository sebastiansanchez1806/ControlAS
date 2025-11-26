<template>
  <div class="app-wrapper">
    <header class="app-header">
      <div class="neon-border"></div>
      <div class="header-content">
        <button class="back-button" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          Volver
        </button>
        <div class="app-title-container">
          <h1 class="logo glitch" data-text="VALKA">Control AS</h1>
          <div class="tagline">Bar</div>
          <h2 class="admin-formal-title">Administradores de {{ activeBarStore.name }}</h2>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div v-if="!admins || admins.length === 0" class="no-admins-message">
        <h2>{{ activeBarStore.name || 'El bar' }} no tiene administradores.</h2>
        <p>¡Agrega el primero para empezar a gestionar el personal!</p>
        <button class="add-admin-btn large-btn" @click="openAdminModal('add')">
          <span>+</span> Agregar Primer Administrador
        </button>
      </div>

      <div v-else class="admin-management">
        <button class="add-admin-btn" @click="openAdminModal('add')">
          <span>+</span> Nuevo Administrador
        </button>
        <div class="admin-grid">
          <div v-for="admin in admins" :key="admin.id" class="admin-card">
            <div class="admin-avatar">
              <img :src="admin.foto || 'https://placehold.co/150x150?text=NA'" :alt="'Foto de ' + admin.nombre"
                @error="handleImageError" />
              <div class="admin-status"></div>
            </div>
            <div class="admin-info">
              <h3>{{ admin.nombre }}</h3>
              <p class="email">{{ admin.correo || 'Sin correo asignado' }}</p>
              <p class="document">Doc: {{ admin.documento || 'Sin documento' }}</p>
              <p class="phone">{{ formatPhone(admin.telefono) }}</p>
            </div>
            <div class="admin-actions">
              <button class="edit-btn" @click="openAdminModal('edit', admin)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
                </svg>
                Editar
              </button>
              <button class="delete-btn" @click="confirmDeleteAdmin(admin)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                  <line x1="10" y1="11" x2="10" y2="17" />
                  <line x1="14" y1="11" x2="14" y2="17" />
                </svg>
                Eliminar
              </button>
              <button class="tasks-btn" @click="openTaskModal(admin)">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                  <polyline points="10 9 9 9 8 9" />
                </svg>
                Tareas
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal Administrador -->
    <div v-if="showAdminModal" class="modal-overlay">
      <div class="admin-modal">
        <div class="modal-header">
          <h3>{{ adminModalMode === 'add' ? 'Agregar' : 'Editar' }} Administrador</h3>
          <button class="close-modal" @click="closeAdminModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Nombre completo</label>
            <input v-model="currentAdmin.nombre" type="text" placeholder="Nombre del administrador">
          </div>
          <div class="form-group">
            <label>Correo Electrónico</label>
            <input v-model="currentAdmin.correo" type="email" placeholder="ejemplo@dominio.com">
          </div>
          <div class="form-group">
            <label>Documento de Identidad</label>
            <input 
              v-model="currentAdmin.documento" 
              type="text" 
              placeholder="Número de documento"
              @input="currentAdmin.documento = currentAdmin.documento.replace(/[^0-9]/g, '')"
              maxlength="20"
            >
          </div>
          <div class="form-group">
            <label>Teléfono</label>
            <input v-model="currentAdmin.telefono" type="tel" placeholder="Número de teléfono">
          </div>
          <div class="form-group">
            <label>Contraseña</label>
            <div class="password-container">
              <input :type="passwordFieldType" v-model="currentAdmin.contraseña" 
                     :placeholder="adminModalMode === 'add' ? 'Establece una contraseña (mín. 6 caracteres)' : 'Dejar vacío para no cambiar'">
              <button class="toggle-password" type="button" @click="togglePasswordVisibility">
                <svg v-if="passwordFieldType === 'password'" xmlns="http://www.w3.org/2000/svg" width="18" height="18"
                  viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path
                    d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.94 3.19M2 2l22 22">
                  </path>
                </svg>
              </button>
            </div>
          </div>
          <div class="form-group">
            <label>Foto de perfil</label>
            <div class="file-upload-area" :class="{ 'dragging': isDragging }" @dragover.prevent="onDragOver"
              @dragleave.prevent="onDragLeave" @drop.prevent="onDrop" @click="triggerFileUpload">
              <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" style="display: none;">
              <div v-if="!currentAdmin.foto" class="image-placeholder">
                <p>Arrastra una imagen o haz clic para seleccionar</p>
              </div>
              <div v-else class="image-preview">
                <img :src="currentAdmin.foto" alt="Vista previa">
              </div>
            </div>
          </div>
          <button 
            class="save-btn" 
            @click="saveAdmin" 
            :disabled="isAdminLoading"
            :class="{ 'loading': isAdminLoading }"
          >
            <span v-if="!isAdminLoading">
              {{ adminModalMode === 'add' ? 'Agregar Administrador' : 'Guardar Cambios' }}
            </span>
            <div v-else class="spinner"></div>
            <span v-if="isAdminLoading" style="margin-left: 8px;">Guardando...</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de Tareas -->
    <div v-if="showTaskModal" class="modal-overlay">
      <div class="admin-modal large-modal">
        <div class="modal-header">
          <h3>Tareas de {{ selectedAdmin.nombre }}</h3>
          <button class="close-modal" @click="closeTaskModal">×</button>
        </div>
        <div class="modal-body">
          <div class="task-tabs">
            <button @click="activeTaskTab = 'pending'" :class="{ active: activeTaskTab === 'pending' }">
              Pendientes ({{ pendingTasks.length }})
            </button>
            <button @click="activeTaskTab = 'completed'" :class="{ active: activeTaskTab === 'completed' }">
              Completadas ({{ completedTasks.length }})
            </button>
          </div>

          <div class="task-list-container">
            <!-- Banner informativo solo en completadas -->
            <div v-if="activeTaskTab === 'completed'" class="completed-info-banner">
              <p>
                <strong>Información:</strong><br>
                Todas las tareas completadas serán enviadas a tu correo y eliminadas del aplicativo 
                los primeros días de cada mes a las 3:00 am.
              </p>
            </div>

            <!-- Sin tareas -->
            <div v-if="filteredTasks.length === 0" class="no-tasks">
              <p>No hay tareas {{ activeTaskTab === 'pending' ? 'pendientes' : 'completadas' }}</p>
            </div>

            <!-- Lista de tareas -->
            <div v-else>
              <div v-for="task in filteredTasks" :key="task.id" class="task-item">
                <div class="task-checkbox">
                  <input type="checkbox" :checked="task.estado === 'completada'" disabled>
                </div>
                <div class="task-content">
                  <p class="task-title" :class="{ completed: task.estado === 'completada' }">
                    {{ task.descripcion }}
                  </p>

                  <div class="task-meta">
                    <div class="task-dates">
                      <span class="task-date assigned">
                        Asignada: {{ formatDate(task.fecha) }}
                      </span>
                      <span v-if="task.estado === 'completada' && task.fecha_completada" class="task-date completed">
                        ✓ Completada: {{ formatDate(task.fecha_completada) }}
                      </span>
                    </div>

                    <button class="task-delete-btn" @click="confirmDeleteTask(task)">
                      Eliminar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="add-task-form">
            <h4>Agregar Nueva Tarea</h4>
            <div class="form-row">
              <input v-model="newTask.descripcion" type="text" placeholder="Descripción de la tarea"
                :class="{ 'input-error': showTaskValidationErrors && !newTask.descripcion }" ref="taskDescriptionInput">
              <input v-model="newTask.fecha" type="date"
                :class="{ 'input-error': showTaskValidationErrors && !newTask.fecha }">
              <button @click="addTask" class="add-btn" :disabled="!isNewTaskFormValid || isTaskLoading">
                <span v-if="!isTaskLoading">+ Agregar</span>
                <div v-else class="spinner"></div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer class="app-footer">
      <div class="neon-border"></div>
      <div class="footer-content">
        <div class="footer-logo">
          <span class="glitch-small">Control AS</span>
          <p>Bar</p>
        </div>
        <div class="footer-info">
          <p class="copyright">&copy; {{ currentYear }} Control AS. Todos los derechos reservados.</p>
        </div>
        <div class="footer-links">
          <button class="footer-btn" @click="showCredits">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10" />
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
              <line x1="12" y1="17" x2="12" y2="17" />
            </svg>
            Créditos
          </button>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useActiveBarStore } from '@/stores/activeBar';
import axios from 'axios';
import Swal from 'sweetalert2';
import { API_BASE_URL } from '../config/api';

const MIN_PASSWORD_LENGTH = 6; 

export default {
  setup() {
    const activeBarStore = useActiveBarStore();
    const admins = ref([]);
    const showAdminModal = ref(false);
    const showTaskModal = ref(false);
    const adminModalMode = ref('add');
    const activeTaskTab = ref('pending');
    const passwordFieldType = ref('password');
    const isDragging = ref(false);
    const fileInput = ref(null);
    const taskDescriptionInput = ref(null); 
    const currentYear = ref(new Date().getFullYear()); 
    const isTaskLoading = ref(false); 
    const isAdminLoading = ref(false);
    
    const currentAdmin = ref({
      id: null,
      nombre: '',
      correo: '', 
      documento: '',
      telefono: '',
      foto: '',
      contraseña: '',
      bar_id: activeBarStore.id
    });

    const selectedAdmin = ref(null);
    const tasks = ref([]);
    const newTask = ref({ descripcion: '', fecha: '' });
    const showTaskValidationErrors = ref(false); 

    const pendingTasks = computed(() => {
      return tasks.value.filter(task => task.estado === 'pendiente');
    });

    const completedTasks = computed(() => {
      return tasks.value.filter(task => task.estado === 'completada');
    });

    const filteredTasks = computed(() => {
      return activeTaskTab.value === 'pending' ? pendingTasks.value : completedTasks.value;
    });

    const isNewTaskFormValid = computed(() => {
      return newTask.value.descripcion.trim() !== '' && newTask.value.fecha.trim() !== '';
    });

    // --- MÉTODOS API ---

    const fetchAdmins = async (barId) => {
      if (!barId) {
        console.warn("ID del bar es nulo, no se obtendrán administradores.");
        admins.value = [];
        return;
      }
      try {
        const response = await axios.get(`${API_BASE_URL}/administradores/bar/${barId}`);
        admins.value = response.data;
      } catch (error) {
        Swal.fire('Error', 'No se pudieron cargar los administradores.', 'error');
        console.error('Error al obtener administradores:', error);
      }
    };

    const fetchTasks = async (adminId) => {
      try {
        const response = await axios.get(`${API_BASE_URL}/tareas_ver/${adminId}`);
        tasks.value = response.data;
      } catch (error) {
        Swal.fire('Error', 'No se pudieron cargar las tareas.', 'error');
        console.error('Error al obtener tareas:', error);
        tasks.value = [];
      }
    };

    const saveAdmin = async () => {
      const nombre = currentAdmin.value.nombre.trim();
      const correo = currentAdmin.value.correo ? currentAdmin.value.correo.trim() : '';
      const documento = currentAdmin.value.documento.trim();
      const telefono = currentAdmin.value.telefono.trim();
      const password = currentAdmin.value.contraseña.trim();

      const payload = {
        ...currentAdmin.value,
        nombre,
        correo,
        documento,
        telefono,
        contraseña: password
      };

      // VALIDACIONES
      if (adminModalMode.value === 'add') {
        if (!nombre || !telefono || !correo || !documento || !password) {
          Swal.fire('Error', 'Nombre, correo, documento, teléfono y contraseña son requeridos.', 'error');
          return;
        }
        if (password.length < MIN_PASSWORD_LENGTH) {
          Swal.fire('Error', `La contraseña debe tener al menos ${MIN_PASSWORD_LENGTH} caracteres.`, 'error');
          return;
        }
      }

      isAdminLoading.value = true;

      try {
        if (adminModalMode.value === 'add') {
          const response = await axios.post(`${API_BASE_URL}/administradores`, payload);
          admins.value.push(response.data);
          Swal.fire('Éxito', 'Administrador creado correctamente.', 'success');
        } else {
          if (payload.contraseña === '') delete payload.contraseña;
          const response = await axios.put(`${API_BASE_URL}/administradores/${payload.id}`, payload);
          const index = admins.value.findIndex(a => a.id === payload.id);
          if (index !== -1) admins.value[index] = response.data;
          Swal.fire('Éxito', 'Administrador actualizado correctamente.', 'success');
        }
        closeAdminModal();
      } catch (error) {
        Swal.fire('Error', error.response?.data?.detail || 'Ocurrió un error al guardar.', 'error');
        console.error('Error al guardar administrador:', error);
      } finally {
        isAdminLoading.value = false;
      }
    };

    const confirmDeleteAdmin = (admin) => {
      Swal.fire({
        title: '¿Estás seguro?',
        text: `Se eliminará a ${admin.nombre} permanentemente.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        showLoaderOnConfirm: true,
        allowOutsideClick: () => !Swal.isLoading(),
        preConfirm: async () => {
          try {
            await axios.delete(`${API_BASE_URL}/administradores/${admin.id}`);
            await fetchAdmins(activeBarStore.id);
            return { success: true };
          } catch (error) {
            Swal.showValidationMessage(
              error.response?.data?.detail || 'Ocurrió un error al eliminar.'
            );
            return { success: false };
          }
        }
      }).then((result) => {
        if (result.isConfirmed && result.value?.success) {
          Swal.fire('Eliminado', 'El administrador ha sido eliminado.', 'success');
        }
      });
    };

    // --- MÉTODOS UI Y UTILERÍAS ---

    const goBack = () => {
      window.history.back();
    };

    const formatPhone = (phone) => phone ? phone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3') : '';

    const handleImageError = (event) => {
      event.target.src = 'https://placehold.co/150x150?text=Error';
    };

    const togglePasswordVisibility = () => {
      passwordFieldType.value = passwordFieldType.value === 'password' ? 'text' : 'password';
    };

    const openAdminModal = (mode, admin = null) => {
      adminModalMode.value = mode;
      currentAdmin.value = admin ? { ...admin, contraseña: '' } : {
        id: null,
        nombre: '',
        correo: '', 
        documento: '',
        telefono: '',
        foto: '',
        contraseña: '',
        bar_id: activeBarStore.id
      };
      showAdminModal.value = true;
    };

    const closeAdminModal = () => {
      showAdminModal.value = false;
      isDragging.value = false;
    };

    const openTaskModal = async (admin) => {
      selectedAdmin.value = admin;
      await fetchTasks(admin.id);
      showTaskModal.value = true;
      activeTaskTab.value = 'pending';
      showTaskValidationErrors.value = false; 

      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      newTask.value.fecha = `${year}-${month}-${day}`;
      newTask.value.descripcion = ''; 

      nextTick(() => {
        if (taskDescriptionInput.value) {
          taskDescriptionInput.value.focus();
        }
      });
    };

    const closeTaskModal = () => showTaskModal.value = false;

    const addTask = async () => {
      showTaskValidationErrors.value = true; 

      if (!isNewTaskFormValid.value) {
        return Swal.fire('Error', 'La descripción y la fecha son requeridas.', 'error');
      }

      isTaskLoading.value = true; 

      try {
        const payload = {
          administrador_id: selectedAdmin.value.id,
          descripcion: newTask.value.descripcion,
          fecha: newTask.value.fecha,
          estado: 'pendiente'
        };
        await axios.post(`${API_BASE_URL}/tareas_crear`, payload);
        Swal.fire('Éxito', 'Tarea agregada.', 'success');
        newTask.value = { descripcion: '', fecha: '' }; 
        showTaskValidationErrors.value = false; 
        await fetchTasks(selectedAdmin.value.id);
      } catch (error) {
        Swal.fire('Error', 'No se pudo agregar la tarea.', 'error');
        console.error('Error al agregar tarea:', error);
      } finally {
        isTaskLoading.value = false; 
      }
    };

    const confirmDeleteTask = (task) => {
      Swal.fire({
        title: '¿Estás seguro?',
        text: `Se eliminará la tarea "${task.descripcion}".`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        showLoaderOnConfirm: true,
        allowOutsideClick: () => !Swal.isLoading(),
        preConfirm: async () => {
          try {
            await axios.delete(`${API_BASE_URL}/tareas_eliminar/${task.id}`);
            await fetchTasks(selectedAdmin.value.id);
            return { success: true };
          } catch (error) {
            Swal.showValidationMessage(
              'No se pudo eliminar la tarea.'
            );
            return { success: false };
          }
        }
      }).then((result) => {
        if (result.isConfirmed && result.value?.success) {
          Swal.fire('Eliminado', 'La tarea ha sido eliminada.', 'success');
        }
      });
    };

    const showCredits = () => {
      Swal.fire({
        title: 'Créditos',
        text: 'Sistema de Administración Control AS Bar desarrollado por sebastian sanchez',
        icon: 'info',
        confirmButtonText: 'Cerrar'
      });
    };

    const onDragOver = () => { isDragging.value = true; };
    const onDragLeave = () => { isDragging.value = false; };
    const onDrop = (event) => {
      isDragging.value = false;
      const file = event.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
          currentAdmin.value.foto = e.target.result;
        };
        reader.readAsDataURL(file);
      } else {
        Swal.fire('Error', 'Por favor selecciona un archivo de imagen válido.', 'error');
      }
    };

    const triggerFileUpload = () => { fileInput.value.click(); };

    const handleFileUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          currentAdmin.value.foto = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };

    const formatDate = (dateString) => {
      const date = new Date(dateString);
      return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };

    onMounted(() => {
      if (activeBarStore.id) {
        fetchAdmins(activeBarStore.id);
      }
    });

    return {
      activeBarStore,
      admins,
      showAdminModal,
      showTaskModal,
      adminModalMode,
      selectedAdmin,
      currentAdmin,
      newTask,
      activeTaskTab,
      pendingTasks,
      completedTasks,
      filteredTasks,
      isNewTaskFormValid,
      showTaskValidationErrors,
      taskDescriptionInput,
      currentYear, 
      isTaskLoading,
      isAdminLoading,
      goBack,
      formatPhone,
      handleImageError,
      openAdminModal,
      closeAdminModal,
      saveAdmin,
      confirmDeleteAdmin,
      openTaskModal,
      closeTaskModal,
      addTask,
      confirmDeleteTask,
      showCredits,
      passwordFieldType,
      togglePasswordVisibility,
      isDragging,
      onDragOver,
      onDragLeave,
      onDrop,
      triggerFileUpload,
      handleFileUpload,
      fileInput,
      formatDate
    };
  }
};
</script>


<style scoped>
/* Importa la fuente Lora para un estilo más formal */
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;700&display=swap');
/* --- Estilos para el Spinner de Carga --- */
.spinner {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #fff; /* Color del spinner */
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
  display: inline-block;
  vertical-align: middle;
  margin: 0 auto; /* Centrar en el botón */
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Estilo para el botón cuando está deshabilitado */
.add-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* Asegurar que el botón tenga un ancho fijo para que el texto/spinner no lo cambie */
.add-task-form .add-btn {
  /* Ajusta el ancho según tu diseño, para que el spinner y el texto ocupen lo mismo */
  min-width: 100px; 
  display: flex;
  align-items: center;
  justify-content: center;
}
/*
  =====================================
  Estilos para la subida de imagen
  =====================================
*/
/* Nuevos estilos para cuando no hay administradores */
.no-admins-message {
  text-align: center;
  margin-top: 3rem;
  padding: 2rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 0.9375rem;
  border: 0.0625rem solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(0.625rem);
  -webkit-backdrop-filter: blur(0.625rem);
}

.no-admins-message h2 {
  font-size: 1.8rem;
  color: #fff;
  margin-bottom: 0.625rem;
  font-family: 'Cyberpunk', sans-serif;
}

.no-admins-message p {
  font-size: 1rem;
  color: #a0a0a0;
  margin-bottom: 1.5625rem;
}

.large-btn {
  font-size: 1rem;
  padding: 0.9375rem 1.875rem;
}

.file-upload-area {
  border: 0.125rem dashed #4e4e4e;
  border-radius: 0.5rem;
  padding: 1.25rem;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.3s ease, background-color 0.3s ease;
  min-height: 9.375rem;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.file-upload-area.dragging {
  border-color: #00ffc8;
  background-color: rgba(0, 255, 200, 0.1);
}

.image-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  color: #888;
  font-size: 1rem;
}

.image-preview {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.image-preview img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 0.375rem;
}

/* --- NUEVOS ESTILOS PARA EL CAMPO DE CONTRASEÑA --- */
.form-group .password-container {
  position: relative;
}

.form-group .password-container input {
  padding-right: 2.5rem;
}

.form-group .password-container .toggle-password {
  position: absolute;
  top: 50%;
  right: 0.625rem;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--neon-cyan);
  transition: color 0.3s ease;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
}

.form-group .password-container .toggle-password:hover {
  color: var(--neon-pink);
}

.form-group .password-container .toggle-password svg {
  width: 100%;
  height: 100%;
}

/* Estilos base */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Barlow', -apple-system, BlinkMacSystemFont, sans-serif;
}

.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #0a0a0a;
  background-image:
    radial-gradient(circle at 20% 30%, rgba(58, 134, 255, 0.1) 0%, transparent 25%),
    radial-gradient(circle at 80% 70%, rgba(255, 0, 110, 0.1) 0%, transparent 25%);
}

/* Header */
.app-header {
  background: rgba(15, 15, 15, 0.95);
  backdrop-filter: blur(0.5rem);
  position: relative;
  z-index: 10;
  padding-bottom: 0.5rem; /* Added padding for better spacing */
}

.neon-border {
  height: 0.1875rem;
  background: linear-gradient(90deg,
      transparent,
      #3a86ff,
      #8338ec,
      #ff006e,
      transparent);
  animation: neon-flow 3s linear infinite;
  background-size: 200% 100%;
}

.header-content {
  padding: 0.75rem 1rem;
  max-width: 87.5rem;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap; /* Allow wrapping on smaller screens */
  gap: 0.8rem; /* Gap between items */
}

.back-button {
  background: rgba(58, 134, 255, 0.1);
  color: #3a86ff;
  border: 0.0625rem solid rgba(58, 134, 255, 0.3);
  padding: 0.4rem 0.8rem;
  border-radius: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  font-size: 0.85rem;
}

.back-button:hover {
  background: rgba(58, 134, 255, 0.2);
  transform: translateX(-0.1875rem);
}

.app-title-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-grow: 1; /* Allow it to take available space */
}

.logo {
  font-size: 1.8rem;
  font-weight: 800;
  letter-spacing: 0.1875rem;
  background: linear-gradient(45deg, #ff006e, #8338ec);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 0.75rem rgba(255, 0, 110, 0.3);
  font-family: 'Rajdhani', sans-serif;
  text-transform: uppercase;
}

.tagline {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 0.125rem;
  margin-top: -0.3125rem;
  font-family: 'Barlow Condensed', sans-serif;
}

.admin-formal-title {
  font-family: 'Lora', serif; /* Formal font */
  font-size: 1.1rem; /* Adjusted for mobile */
  color: #00eeff; /* Neon green for contrast */
  text-shadow: 0 0 0.5rem rgba(0, 255, 200, 0.5);
  margin-top: 0.5rem;
  text-align: center;
  width: 100%; /* Ensure it takes full width */
}


/* Main content */
.main-content {
  flex: 1;
  padding: 1rem;
  max-width: 87.5rem;
  margin: 0 auto;
  width: 100%;
}

.add-admin-btn {
  background: rgba(255, 0, 110, 0.9);
  color: white;
  border: none;
  padding: 0.7rem 1.2rem;
  border-radius: 1.875rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  transition: all 0.3s ease;
  box-shadow: 0 0.25rem 0.9375rem rgba(255, 0, 110, 0.3);
  font-family: 'Rajdhani', sans-serif;
  letter-spacing: 0.0625rem;
  font-size: 0.9rem;
}

.add-admin-btn:hover {
  transform: translateY(-0.125rem);
  box-shadow: 0 0.375rem 1.25rem rgba(255, 0, 110, 0.4);
}

.add-admin-btn span {
  font-size: 1.1rem;
  line-height: 0;
}

.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: 1rem;
}

.admin-card {
  background: rgba(25, 25, 25, 0.8);
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 0.3125rem 0.9375rem rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  backdrop-filter: blur(0.375rem);
  border: 0.0625rem solid rgba(255, 255, 255, 0.05);
}

.admin-card:hover {
  transform: translateY(-0.3125rem);
  box-shadow: 0 0.5rem 1.5625rem rgba(0, 0, 0, 0.4);
}

.admin-avatar {
  width: 100%;
  height: 10rem;
  overflow: hidden;
  position: relative;
  background: rgba(0, 0, 0, 0.4);
}

.admin-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.admin-card:hover .admin-avatar img {
  transform: scale(1.05);
}

.admin-status {
  position: absolute;
  bottom: 0.9375rem;
  right: 0.9375rem;
  width: 0.75rem;
  height: 0.75rem;
  background: #555;
  border-radius: 50%;
  border: 0.125rem solid #222;
}

.admin-status.active {
  background: #4ade80;
  box-shadow: 0 0 0.5rem #4ade80;
}

.admin-info {
  padding: 1rem;
}

.admin-info h3 {
  color: #ff006e;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

.admin-info .phone {
  color: #3a86ff;
  font-size: 0.8rem;
  margin-bottom: 0.15rem;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.admin-info .phone::before {
  content: '';
  display: inline-block;
  width: 0.875rem;
  height: 0.875rem;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%233a86ff'%3E%3Cpath d='M20 15.5c-1.2 0-2.5-.2-3.6-.6h-.3l-.3-.2c-.2-.1-.3-.4-.2-.6.1-.2.2-.3.3-.4l2.5-2.4c.2-.2.2-.5.1-.7l-3.4-3.2c-.2-.2-.5-.2-.7 0l-9.4 9.3c-.2.2-.3.4-.1.6.1.2.2.3.4.4v.5c-1.4 2.7-4 4.5-5.4 5.1-.2.1-.4.3-.4.5s.3.5.5.5h.2c4.2-.8 8.1-3.2 10.2-5l1.4 1.3c.2.2.5.3.7.3h.5c9.4-5 6-8.3 4.6-9.7-.6-.6-1.3-1.2-1.8-1.8-.2-.2-.4-.3-.6-.3s-.4 0-.5.1l-1.7 1.6c-.2.2-.3.3-.3.5s0 .4.1.5c1.4 0 2.3.1 2.9.1.4 0 .7.3.7.7 0 .6-.1 1.5-.1 2.9v.5z'/%3E%3C/svg%3E");
  background-size: contain;
}

.admin-info .date {
  color: #8338ec;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.admin-info .date::before {
  content: '';
  display: inline-block;
  width: 0.875rem;
  height: 0.875rem;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%238338ec'%3E%3Cpath d='M19 4h-1V2h-2v2H8V2H6v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 16H5V10h14v10zM9 14H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2zm-8 4H7v-2h2v2zm4 0h-2v-2h2v2zm4 0h-2v-2h2v2z'/%3E%3C/svg%3E");
  background-size: contain;
}

.admin-actions {
  display: flex;
  padding: 0 1rem 1rem;
  gap: 0.5rem;
}

.admin-actions button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.admin-actions button svg {
  width: 1rem;
  height: 1rem;
}

.edit-btn {
  background: rgba(58, 134, 255, 0.1);
  color: #3a86ff;
  border: 0.0625rem solid rgba(58, 134, 255, 0.2) !important;
}

.edit-btn:hover {
  background: rgba(58, 134, 255, 0.2);
}

.delete-btn {
  background: rgba(255, 54, 89, 0.1);
  color: #ff3659;
  border: 0.0625rem solid rgba(255, 54, 89, 0.2) !important;
}

.delete-btn:hover {
  background: rgba(255, 54, 89, 0.2);
}

.tasks-btn {
  background: rgba(131, 56, 236, 0.1);
  color: #8338ec;
  border: 0.0625rem solid rgba(131, 56, 236, 0.2) !important;
}

.tasks-btn:hover {
  background: rgba(131, 56, 236, 0.2);
}

/* Modales */



.modal-header {
  padding: 1rem;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  font-size: 1.1rem;
  font-weight: 600;
  background: linear-gradient(45deg, #ff006e, #8338ec);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.close-modal {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  transition: color 0.2s;
}

.close-modal:hover {
  color: white;
}

.modal-body {
  padding: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  color: #ff006e;
  margin-bottom: 0.3rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.6rem;
  background: rgba(0, 0, 0, 0.5);
  border: 0.0625rem solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  color: white;
  font-size: 0.9rem;
}

.form-group input:focus {
  outline: none;
  border-color: #3a86ff;
}

.image-preview {
  margin-top: 0.5rem;
  width: 5rem;
  height: 5rem;
  border-radius: 0.5rem;
  overflow: hidden;
  border: 0.0625rem solid rgba(255, 255, 255, 0.1);
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.save-btn {
  width: 100%;
  padding: 0.7rem;
  background: #3a86ff;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 0.5rem;
  font-size: 0.95rem;
}

.save-btn:hover {
  background: #2f72d8;
}

/* Task Modal */
.task-tabs {
  display: flex;
  margin-bottom: 1rem;
  border-bottom: 0.0625rem solid rgba(255, 255, 255, 0.1);
}

.task-tabs button {
  background: none;
  border: none;
  padding: 0.6rem 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  position: relative;
  font-size: 0.85rem;
}

.task-tabs button.active {
  color: #3a86ff;
  font-weight: 500;
}

.task-tabs button.active::after {
  content: '';
  position: absolute;
  bottom: -0.0625rem;
  left: 0;
  right: 0;
  height: 0.125rem;
  background: #3a86ff;
}

.task-list-container {
  max-height: 18.75rem;
  overflow-y: auto;
  margin-bottom: 1rem;
}

.task-item {
  display: flex;
  align-items: center;
  padding: 0.6rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 0.5rem;
  margin-bottom: 0.4rem;
}

.task-checkbox {
  margin-right: 0.5rem;
}

.task-checkbox input {
  width: 1.125rem;
  height: 1.125rem;
  accent-color: #4ade80;
  cursor: pointer;
}

.task-content {
  flex: 1;
}

.task-title {
  color: white;
  font-size: 0.9rem;
  margin-bottom: 0.15rem;
}

.task-title.completed {
  text-decoration: line-through;
  color: rgba(255, 255, 255, 0.5);
}

.task-meta {
  display: flex;
  flex-direction: column; /* Stack date and delete button on small screens */
  align-items: flex-start;
  gap: 0.2rem;
}

.task-date {
  color: #8338ec;
  font-size: 0.75rem;
}

.task-delete-btn {
  background: rgba(255, 54, 89, 0.1);
  color: #ff3659;
  border: 0.0625rem solid rgba(255, 54, 89, 0.2);
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.7rem;
  cursor: pointer;
}

.task-delete-btn:hover {
  background: rgba(255, 54, 89, 0.2);
}

.no-tasks {
  text-align: center;
  padding: 1rem;
  color: rgba(255, 255, 255, 0.5);
}

.add-task-form {
  margin-top: 1.2rem;
  padding-top: 1rem;
  border-top: 0.0625rem solid rgba(255, 255, 255, 0.1);
}

.add-task-form h4 {
  font-size: 1rem;
  margin-bottom: 0.8rem;
  background: linear-gradient(45deg, #ff006e, #8338ec);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.form-row {
  display: flex;
  flex-direction: column; /* Default to column for mobile */
  gap: 0.5rem;
}

.form-row input {
  flex: 1;
  padding: 0.6rem;
  background: rgba(0, 0, 0, 0.5);
  border: 0.0625rem solid rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  color: white;
  font-size: 0.9rem;
}

.form-row input[type="date"] {
  min-width: 100%; /* Ensure it takes full width on mobile */
}

.add-btn {
  background: #8338ec;
  color: white;
  border: none;
  padding: 0.6rem 0.8rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 0.9rem;
}

.add-btn:hover {
  background: #762bd9;
}

.add-btn:disabled {
  background-color: #555;
  cursor: not-allowed;
  opacity: 0.6;
}

/* New style for validation error */
.input-error {
  border-color: #ff3659 !important;
  box-shadow: 0 0 0.3125rem rgba(255, 54, 89, 0.5);
}

/* Confirm Modal */
.confirm-modal {
  width: 90%;
  max-width: 25rem;
  padding: 1rem;
}

.confirm-content {
  background: rgba(25, 25, 25, 0.95);
  border-radius: 0.75rem;
  overflow: hidden;
  border-top: 0.1875rem solid #ff3659;
}

.confirm-content p {
  padding: 1rem;
  color: #ff006e;
  text-align: center;
  font-size: 1rem;
}

.confirm-buttons {
  display: flex;
  flex-direction: column; /* Stack buttons on small screens */
  padding: 0 1rem 1rem;
  gap: 0.5rem;
}

.cancel-btn,
.confirm-btn {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: none;
  padding: 0.6rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
}

.confirm-btn {
  background: #ff3659;
}

/* Footer */
.app-footer {
  background: rgba(15, 15, 15, 0.95);
  backdrop-filter: blur(0.5rem);
  margin-top: auto;
  padding-top: 0.5rem; /* Added padding for better spacing */
}

.footer-content {
  padding: 1rem;
  max-width: 87.5rem;
  margin: 0 auto;
  display: flex;
  flex-direction: column; /* Default to column for mobile */
  justify-content: space-between;
  align-items: center;
  gap: 0.8rem;
}

.footer-logo {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center logo on mobile */
}

.glitch-small {
  font-size: 1.2rem;
  font-weight: 700;
  font-family: 'Rajdhani', sans-serif;
  background: linear-gradient(45deg, #ff006e, #8338ec);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.footer-logo p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.75rem;
  margin-top: -0.1875rem;
}

.footer-info {
    text-align: center;
    color: rgba(255, 255, 255, 0.5);
    font-size: 0.8rem;
}

.footer-btn {
  background: rgba(131, 56, 236, 0.1);
  color: #8338ec;
  border: 0.0625rem solid rgba(131, 56, 236, 0.3);
  padding: 0.4rem 0.8rem;
  border-radius: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.85rem;
}

.footer-btn:hover {
  background: rgba(131, 56, 236, 0.2);
}

/* Animations */
@keyframes neon-flow {
  0% {
    background-position: 0% 50%;
  }

  100% {
    background-position: 100% 50%;
  }
}

/* Responsive adjustments for larger screens */
@media (min-width: 481px) {
  .header-content {
    padding: 1rem 1.5rem;
    flex-wrap: nowrap; /* Prevent wrapping on larger screens */
  }

  .app-title-container {
      flex-grow: 0; /* Reset flex-grow */
  }

  .logo {
    font-size: 2rem;
  }

  .tagline {
    font-size: 0.8rem;
  }

  .admin-formal-title {
      font-size: 1.3rem;
  }

  .main-content {
    padding: 1.5rem;
  }

  .add-admin-btn {
    padding: 0.7rem 1.4rem;
    font-size: 0.95rem;
  }

  .add-admin-btn span {
    font-size: 1.2rem;
  }

  .admin-grid {
    grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr));
    gap: 1.25rem;
  }

  .admin-card {
    border-radius: 0.875rem;
  }

  .admin-avatar {
    height: 11rem;
  }

  .admin-info {
    padding: 1.1rem;
  }

  .admin-info h3 {
    font-size: 1.1rem;
  }

  .admin-info .phone {
    font-size: 0.85rem;
  }

  .admin-actions {
    padding: 0 1.1rem 1.1rem;
    gap: 0.4rem;
  }

  .admin-actions button {
    padding: 0.55rem;
    font-size: 0.825rem;
  }

  .admin-modal {
    max-width: 35rem;
  }

  .large-modal {
    max-width: 42rem;
  }

  .modal-header {
    padding: 1.1rem;
  }

  .modal-header h3 {
    font-size: 1.2rem;
  }

  .modal-body {
    padding: 1.1rem;
  }

  .form-group {
    margin-bottom: 1.1rem;
  }

  .form-group label {
    font-size: 0.9rem;
  }

  .form-group input {
    padding: 0.7rem;
    font-size: 0.9rem;
  }

  .image-preview {
    width: 6rem;
    height: 6rem;
  }

  .save-btn {
    padding: 0.75rem;
    font-size: 1rem;
  }

  .task-tabs {
    margin-bottom: 1.1rem;
  }

  .task-tabs button {
    padding: 0.7rem 0.9rem;
    font-size: 0.9rem;
  }

  .task-list-container {
    max-height: 20rem;
    margin-bottom: 1.1rem;
  }

  .task-item {
    padding: 0.7rem;
    margin-bottom: 0.45rem;
  }

  .task-checkbox {
    margin-right: 0.6rem;
  }

  .task-title {
    font-size: 0.925rem;
  }

  .task-meta {
    flex-direction: row; /* Revert to row for larger screens */
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
  }

  .task-date {
    font-size: 0.8rem;
  }

  .task-delete-btn {
    padding: 0.225rem 0.45rem;
    font-size: 0.75rem;
  }

  .no-tasks {
    padding: 1.25rem;
  }

  .add-task-form {
    margin-top: 1.3rem;
    padding-top: 1.1rem;
  }

  .add-task-form h4 {
    font-size: 1.05rem;
    margin-bottom: 0.9rem;
  }

  .form-row {
    flex-direction: row; /* Revert to row for larger screens */
  }

  .form-row input {
    padding: 0.7rem;
    font-size: 0.9rem;
  }

  .form-row input[type="date"] {
    min-width: 8.75rem; /* Specific width for date input */
  }

  .add-btn {
    padding: 0 0.9rem;
    font-size: 0.9rem;
  }

  .confirm-modal {
    max-width: 28rem;
  }

  .confirm-content p {
    padding: 1.25rem;
    font-size: 1.05rem;
  }

  .confirm-buttons {
    flex-direction: row; /* Revert to row for larger screens */
    padding: 0 1.1rem 1.1rem;
    gap: 0.6rem;
  }

  .cancel-btn,
  .confirm-btn {
    padding: 0.7rem;
    font-size: 0.95rem;
  }

  .footer-content {
    padding: 1.25rem;
    flex-direction: row; /* Revert to row for larger screens */
    gap: 1rem;
  }

  .footer-logo {
    align-items: flex-start; /* Align logo to start for larger screens */
  }

  .glitch-small {
    font-size: 1.3rem;
  }

  .footer-logo p {
    font-size: 0.8rem;
  }

  .footer-btn {
    padding: 0.45rem 0.9rem;
    font-size: 0.9rem;
  }
}

@media (min-width: 769px) {
  .header-content {
    padding: 1.25rem 2rem;
  }

  .logo {
    font-size: 2.2rem;
  }

  .tagline {
    font-size: 0.85rem;
  }

  .admin-formal-title {
      font-size: 1.5rem;
  }

  .main-content {
    padding: 2rem;
  }

  .add-admin-btn {
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
  }

  .add-admin-btn span {
    font-size: 1.3rem;
  }

  .admin-grid {
    grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
    gap: 1.5rem;
  }

  .admin-card {
    border-radius: 0.75rem;
  }

  .admin-avatar {
    height: 11.25rem;
  }

  .admin-info {
    padding: 1.25rem;
  }

  .admin-info h3 {
    font-size: 1.15rem;
  }

  .admin-info .phone {
    font-size: 0.9rem;
  }

  .admin-actions {
    padding: 0 1.25rem 1.25rem;
    gap: 0.5rem;
  }

  .admin-actions button {
    padding: 0.6rem;
    font-size: 0.85rem;
  }

  .admin-modal {
    max-width: 31.25rem;
  }

  .large-modal {
    max-width: 37.5rem;
  }

  .modal-header {
    padding: 1.25rem;
  }

  .modal-header h3 {
    font-size: 1.25rem;
  }

  .modal-body {
    padding: 1.25rem;
  }

  .form-group {
    margin-bottom: 1.25rem;
  }

  .form-group label {
    font-size: 0.95rem;
  }

  .form-group input {
    padding: 0.75rem;
    font-size: 0.95rem;
  }

  .image-preview {
    width: 5rem;
    height: 5rem;
  }

  .save-btn {
    padding: 0.8rem;
    font-size: 1rem;
  }

  .task-tabs {
    margin-bottom: 1.25rem;
  }

  .task-tabs button {
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
  }

  .task-list-container {
    max-height: 18.75rem;
    margin-bottom: 1.25rem;
  }

  .task-item {
    padding: 0.75rem;
    margin-bottom: 0.5rem;
  }

  .task-checkbox {
    margin-right: 0.75rem;
  }

  .task-title {
    font-size: 0.95rem;
  }

  .task-meta {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
  }

  .task-date {
    font-size: 0.85rem;
  }

  .task-delete-btn {
    padding: 0.25rem 0.5rem;
    font-size: 0.8rem;
  }

  .no-tasks {
    padding: 1.5rem;
  }

  .add-task-form {
    margin-top: 1.5rem;
    padding-top: 1.25rem;
  }

  .add-task-form h4 {
    font-size: 1.1rem;
    margin-bottom: 1rem;
  }

  .form-row {
    flex-direction: row;
  }

  .form-row input {
    padding: 0.75rem;
    font-size: 0.95rem;
  }

  .form-row input[type="date"] {
    min-width: 8.75rem;
  }

  .add-btn {
    padding: 0 1rem;
    font-size: 1rem;
  }

  .confirm-modal {
    max-width: 25rem;
  }

  .confirm-content p {
    padding: 1.5rem;
    font-size: 1.1rem;
  }

  .confirm-buttons {
    flex-direction: row;
    padding: 0 1.25rem 1.25rem;
    gap: 0.75rem;
  }

  .cancel-btn,
  .confirm-btn {
    padding: 0.75rem;
    font-size: 1rem;
  }

  .footer-content {
    padding: 1.5rem;
    flex-direction: row;
    gap: 1rem;
  }

  .footer-logo {
    align-items: flex-start;
  }

  .glitch-small {
    font-size: 1.5rem;
  }

  .footer-logo p {
    font-size: 0.85rem;
  }

  .footer-btn {
    padding: 0.5rem 1rem;
    font-size: 1rem;
  }
}
/* ==== MODALES - SCROLL CORREGIDO ==== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: flex-start;     /* Cambiado de center a flex-start */
  z-index: 1000;
  backdrop-filter: blur(0.3125rem);
  overflow-y: auto;            /* ← Permite scroll en el overlay si el modal es muy alto */
  padding: 1rem 0;             /* Espacio arriba/abajo en móviles */
}

.admin-modal {
  background: rgba(25, 25, 25, 0.95);
  border-radius: 0.75rem;
  width: 90%;
  max-width: 30rem;
  box-shadow: 0 0.3125rem 1.875rem rgba(0, 0, 0, 0.5);
  border-top: 0.1875rem solid #3a86ff;
  margin: auto;                /* Centra verticalmente cuando cabe */
  max-height: 95vh;            /* ← NUNCA más alto que la pantalla */
  display: flex;
  flex-direction: column;
  overflow: hidden;            /* sigue ocultando overflow del contenedor principal */
  backdrop-filter: blur(0.625rem);
}

.large-modal {
  max-width: 37.5rem;
}

/* El cuerpo del modal ahora sí tiene scroll */
.modal-body {
  padding: 1.5rem;
  overflow-y: auto;            /* ← AQUÍ ESTÁ EL SCROLL */
  flex: 1;                     /* Ocupa el espacio disponible */
  -webkit-overflow-scrolling: touch; /* scroll suave en iOS */
}

/* Opcional: mejora visual del scroll en webkit */
.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: rgba(255,255,255,0.05);
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb {
  background: rgba(58, 134, 255, 0.5);
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb:hover {
  background: #3a86ff;
}
/* Banner informativo en pestaña Completadas */
.completed-info-banner {
  background: linear-gradient(90deg, rgba(131, 56, 236, 0.2), rgba(58, 134, 255, 0.2));
  border: 1px solid rgba(131, 56, 236, 0.4);
  border-radius: 0.75rem;
  padding: 1rem;
  margin-bottom: 1rem;
  text-align: center;
  font-size: 0.9rem;
  color: #e0e0ff;
  backdrop-filter: blur(4px);
}

.completed-info-banner p {
  margin: 0;
  line-height: 1.5;
}

.completed-info-banner strong {
  color: #00eeff;
  font-size: 1rem;
}
.task-dates {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 0.85rem;
}

.task-date.assigned {
  color: #aaa;
}

.task-date.completed {
  color: #4ade80;
  font-weight: 600;
}

/* Opcional: si quieres que se vea más destacado */
.task-date.completed::before {
  content: "✓ ";
}
.save-btn.loading {
  opacity: 0.8;
  cursor: not-allowed;
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.save-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 48px;
}
</style>
