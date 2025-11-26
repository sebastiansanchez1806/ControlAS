<template>
  <div class="app-container">
    <header class="header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-wrapper">
            <h1 class="logo-text">CONTROL AS</h1>
            <div class="logo-glow"></div>
          </div>
          <div class="header-message">
            <div class="greeting-card">
              <h2 class="greeting">
                ¡Hola, {{ admin.nombre }}!
              </h2>
              <p class="greeting-subtitle">Gestión de Tareas</p>
            </div>
          </div>
        </div>

        <button class="back-btn" @click="goBack">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" />
          </svg>
          volver
        </button>
      </div>
    </header>

    <nav class="nav-container">
      <div class="nav-tabs">
        <button
          class="nav-tab"
          :class="{ active: activeTab === 'pending' }"
          @click="activeTab = 'pending'"
        >
          <div class="tab-content">
            <div class="tab-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 11H15M9 15H15M17 21H7C5.89543 21 5 20.1046 5 19V5C5 3.89543 5.89543 3 7 3H12.5858C12.851 3 13.1054 3.10536 13.2929 3.29289L19.7071 9.70711C19.8946 9.89464 20 10.149 20 10.4142V19C20 20.1046 19.1046 21 18 21H17Z" stroke-width="2" />
              </svg>
            </div>
            <span class="tab-text">Pendientes</span>
            <span class="tab-badge">{{ pendingTasks.length }}</span>
          </div>
        </button>

        <button
          class="nav-tab"
          :class="{ active: activeTab === 'completed' }"
          @click="activeTab = 'completed'"
        >
          <div class="tab-content">
            <div class="tab-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 12L11 14L15 10M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke-width="2" />
              </svg>
            </div>
            <span class="tab-text">Terminadas</span>
            <span class="tab-badge">{{ completedTasks.length }}</span>
          </div>
        </button>
      </div>
    </nav>

    <main class="main-content">
      <div class="filter-section">
        <input v-model="searchQuery" type="text" placeholder="Buscar por descripción..." class="search-input" />
        <input v-model="selectedDay" type="number" placeholder="Día" class="date-filter day-filter" min="1" max="31" />
        <select v-model="selectedMonth" class="date-filter month-filter">
          <option value="">Mes</option>
          <option v-for="(month, index) in months" :key="index" :value="index.toString()">{{ month }}</option>
        </select>
        <input v-model="selectedYear" type="number" placeholder="Año" class="date-filter year-filter" min="2000" max="2100" />
      </div>

      <transition name="slide" mode="out-in">
        <!-- PESTAÑA PENDIENTES (sin cambios) -->
        <div v-if="activeTab === 'pending'" key="pending" class="task-section">
          <div v-if="filteredPendingTasks.length > 0" class="tasks-grid">
            <div v-for="(task, index) in filteredPendingTasks" :key="task.id" class="task-card pending-task" :style="{ '--delay': index * 0.1 + 's' }">
              <div class="task-header">
                <div class="task-priority"></div>
                <div class="task-actions">
                  <button class="action-btn" @click.stop="confirmComplete(task)">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M5 13L9 17L19 7" stroke-width="2" stroke-linecap="round" />
                    </svg>
                  </button>
                </div>
              </div>

              <div class="task-body">
                <h3 class="task-title">{{ task.descripcion }}</h3>
                <div class="task-meta">
                  <div class="meta-item">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M8 2V6M16 2V6M3 10H21M5 4H19C20.1046 4 21 4.89543 21 6V20C21 21.1046 20.1046 22 19 22H5C3.89543 22 3 21.1046 3 20V6C3 4.89543 3.89543 4 5 4Z" stroke-width="1.5" />
                    </svg>
                    <span>{{ formatDate(task.fecha) }}</span>
                  </div>
                </div>
              </div>

              <div class="task-footer">
                <button class="complete-btn" @click.stop="confirmComplete(task)">
                  <span>Marcar Completada</span>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M5 13L9 17L19 7" stroke-width="2" stroke-linecap="round" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div v-else class="empty-state">
            <div class="empty-illustration">
              <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 12L11 14L15 10M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke-width="1" />
              </svg>
            </div>
            <h3 class="empty-title">¡Excelente trabajo, {{ admin.nombre }}!</h3>
            <p class="empty-subtitle">No tienes tareas pendientes que coincidan con tu búsqueda.</p>
          </div>
        </div>

        <!-- PESTAÑA TERMINADAS - CON EL MENSAJE NUEVO -->
        <div v-else key="completed" class="task-section">

          <!-- Mensaje informativo (siempre visible en Terminadas) -->
          <div class="completed-info-banner">
            <p>
              <strong>Información:</strong><br>
              Todas las tareas completadas serán enviadas a tu correo y eliminadas del aplicativo 
              los primeros días de cada mes a las 3:00 am.
            </p>
          </div>

          <!-- Tareas completadas -->
          <div v-if="filteredCompletedTasks.length > 0" class="tasks-grid">
            <div v-for="(task, index) in filteredCompletedTasks" :key="task.id" class="task-card completed-task" :style="{ '--delay': index * 0.1 + 's' }">
              <div class="task-header">
                <div class="completion-badge">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M9 12L11 14L15 10M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke-width="2" />
                  </svg>
                </div>
              </div>

              <div class="task-body">
                <h3 class="task-title">{{ task.descripcion }}</h3>
                <div class="task-meta">
                  <div class="meta-item completed-date">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M9 12L11 14L15 10M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke-width="1.5" />
                    </svg>
                    <span>Completada {{ formatDate(task.fecha_completada) }}</span>
                  </div>
                  <div class="meta-item original-date">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path d="M8 2V6M16 2V6M3 10H21M5 4H19C20.1046 4 21 4.89543 21 6V20C21 21.1046 20.1046 22 19 22H5C3.89543 22 3 21.1046 3 20V6C3 4.89543 3.89543 4 5 4Z" stroke-width="1.5" />
                    </svg>
                    <span>Fecha original: {{ formatDate(task.fecha) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Estado vacío -->
          <div v-else class="empty-state">
            <div class="empty-illustration">
              <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 11H15M9 15H15M17 21H7C5.89543 21 5 20.1046 5 19V5C5 3.89543 5.89543 3 7 3H12.5858C12.851 3 13.1054 3.10536 13.2929 3.29289L19.7071 9.70711C19.8946 9.89464 20 10.149 20 10.4142V19C20 20.1046 19.1046 21 18 21H17Z" stroke-width="1" />
              </svg>
            </div>
            <h3 class="empty-title">Historial vacío</h3>
            <p class="empty-subtitle">Aún no has completado ninguna tarea que coincida con tu búsqueda.</p>
          </div>
        </div>
      </transition>
    </main>

    <!-- Modal de confirmación (sin cambios) -->
    <transition name="modal">
      <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-container">
          <div class="modal-header">
            <h3>Confirmar Completación</h3>
            <button class="modal-close" @click="closeModal">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M18 6L6 18M6 6L18 18" stroke-width="2" stroke-linecap="round" />
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div class="confirmation-icon">
              <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 12L11 14L15 10M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z" stroke-width="1.5" />
              </svg>
            </div>

            <h4 class="modal-question">¿Marcar como completada?</h4>
            <p class="modal-description">Esta acción marcará la tarea como terminada y la moverá al historial.</p>

            <div class="task-preview">
              <div class="preview-content">
                <h5 class="preview-title">{{ selectedTask?.descripcion }}</h5>
                <div class="preview-date">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M8 2V6M16 2V6M3 10H21M5 4H19C20.1046 4 21 4.89543 21 6V20C21 21.1046 20.1046 22 19 22H5C3.89543 22 3 21.1046 3 20V6C3 4.89543 3.89543 4 5 4Z" stroke-width="1.5" />
                  </svg>
                  <span>{{ formatDate(selectedTask?.fecha) }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button class="modal-btn cancel-btn" @click="closeModal">Cancelar</button>
            <button class="modal-btn confirm-btn" @click="completeTask">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M5 13L9 17L19 7" stroke-width="2" stroke-linecap="round" />
              </svg>
              Completar Tarea
            </button>
          </div>
        </div>
      </div>
    </transition>
    
    <footer class="footer">
      <p>&copy; 2025 Control AS. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>
<script>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAdminStore } from '@/stores/admin';
import axios from 'axios';
import Swal from 'sweetalert2';
import { API_BASE_URL } from '../config/api';

export default {
  name: 'Control AS',
  setup() {
    const activeTab = ref('pending');
    const showModal = ref(false);
    const selectedTask = ref(null);

    const pendingTasks = ref([]);
    const completedTasks = ref([]);

    // Nuevos estados para la búsqueda por fecha
    const searchQuery = ref('');
    const selectedDay = ref('');
    const selectedMonth = ref('');
    const selectedYear = ref('');

    // Array de meses para el filtro
    const months = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];

    const admin = useAdminStore();
    const router = useRouter();

    const fetchTasks = async () => {
      if (!admin.id) {
        console.error('El ID del administrador no está disponible.');
        return;
      }

      try {
        // *** USO DE LA CONSTANTE GLOBAL ***
        const url = `${API_BASE_URL}/tareas_ver/${admin.id}`;
        const response = await axios.get(url);

        const data = response.data;

        pendingTasks.value = data.filter(task => task.estado === 'pendiente');
        completedTasks.value = data.filter(task => task.estado === 'completada');
      } catch (error) {
        console.error('No se pudieron obtener las tareas:', error);
        Swal.fire('Error', 'No se pudieron obtener las tareas.', 'error');
      }
    };

    onMounted(() => {
      fetchTasks();
    });

    const formatDate = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toLocaleDateString('es-ES', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      });
    };

    const confirmComplete = (task) => {
      selectedTask.value = task;
      showModal.value = true;
    };

    const completeTask = async () => {
      if (!selectedTask.value) return;

      try {
        // *** USO DE LA CONSTANTE GLOBAL ***
        await axios.put(`${API_BASE_URL}/tareas/${selectedTask.value.id}/completar`);

        Swal.fire('Completada', 'La tarea ha sido marcada como completada.', 'success');

        closeModal();
        await fetchTasks();
        activeTab.value = 'completed';
      } catch (error) {
        console.error('Error al completar la tarea:', error);
        Swal.fire('Error', 'No se pudo completar la tarea.', 'error');
      }
    };

    const closeModal = () => {
      showModal.value = false;
      selectedTask.value = null;
    };

    const goBack = () => {
      router.back();
    };
    
    // Función de filtrado centralizada
    const filterTasksByDate = (tasks, dateField) => {
      return tasks.filter(task => {
        const taskMatchesSearch = task.descripcion.toLowerCase().includes(searchQuery.value.toLowerCase());
        
        const taskDate = new Date(task[dateField]);
        const taskDay = taskDate.getDate();
        const taskMonth = taskDate.getMonth(); // 0-11
        const taskYear = taskDate.getFullYear();

        const dayMatchesFilter = selectedDay.value === '' || parseInt(selectedDay.value) === taskDay;
        
        // CORRECCIÓN: Convertir selectedMonth a número para la comparación
        const monthValue = selectedMonth.value !== '' ? parseInt(selectedMonth.value) : '';
        const monthMatchesFilter = monthValue === '' || monthValue === taskMonth;

        const yearMatchesFilter = selectedYear.value === '' || parseInt(selectedYear.value) === taskYear;

        return taskMatchesSearch && dayMatchesFilter && monthMatchesFilter && yearMatchesFilter;
      });
    };

    // Propiedad computada para filtrar las tareas pendientes
    const filteredPendingTasks = computed(() => {
      return filterTasksByDate(pendingTasks.value, 'fecha');
    });

    // Propiedad computada para filtrar las tareas completadas
    const filteredCompletedTasks = computed(() => {
      return filterTasksByDate(completedTasks.value, 'fecha_completada');
    });

    return {
      activeTab,
      pendingTasks,
      completedTasks,
      showModal,
      selectedTask,
      formatDate,
      confirmComplete,
      completeTask,
      closeModal,
      goBack,
      admin,
      searchQuery,
      selectedDay,
      selectedMonth,
      selectedYear,
      months,
      filteredPendingTasks,
      filteredCompletedTasks,
    };
  }
};
</script>
<style scoped>
/* Modal de Confirmación */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  animation: fadeIn 0.3s ease;
}

.modal-container {
  background: linear-gradient(135deg, #111827 0%, #000000 100%);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 
              0 0 100px rgba(236, 72, 153, 0.2);
  overflow: hidden;
  animation: modalSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.modal-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #ec4899 0%, #3b82f6 100%);
}

.modal-header {
  background: rgba(255, 255, 255, 0.03);
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ec4899 0%, #3b82f6 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.modal-close {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #ffffff;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

.modal-body {
  padding: 2rem;
  text-align: center;
}

.confirmation-icon {
  margin: 0 auto 1.5rem;
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  animation: pulseGlow 2s ease-in-out infinite;
}

.confirmation-icon::before {
  content: '';
  position: absolute;
  inset: -4px;
  background: linear-gradient(135deg, #ec4899 0%, #3b82f6 100%);
  border-radius: 50%;
  z-index: -1;
  opacity: 0.3;
  filter: blur(10px);
}

.confirmation-icon svg {
  stroke: #ec4899;
  filter: drop-shadow(0 0 10px rgba(236, 72, 153, 0.5));
}

.modal-question {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 0.75rem;
}

.modal-description {
  color: #9ca3af;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0 0 1.5rem;
}

.task-preview {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.25rem;
  margin-top: 1.5rem;
  position: relative;
  overflow: hidden;
}

.task-preview::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #ec4899 0%, #3b82f6 100%);
}

.preview-content {
  text-align: left;
}

.preview-title {
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  margin: 0 0 0.75rem;
  line-height: 1.4;
}

.preview-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #9ca3af;
  font-size: 0.875rem;
}

.preview-date svg {
  flex-shrink: 0;
}

.modal-footer {
  background: rgba(255, 255, 255, 0.03);
  padding: 1.5rem 2rem;
  display: flex;
  gap: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-btn {
  flex: 1;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.confirm-btn {
  background: linear-gradient(135deg, #ec4899 0%, #3b82f6 100%);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(236, 72, 153, 0.3);
  position: relative;
  overflow: hidden;
}

.confirm-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #3b82f6 0%, #ec4899 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.confirm-btn:hover::before {
  opacity: 1;
}

.confirm-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(236, 72, 153, 0.5);
}

.confirm-btn svg,
.confirm-btn span {
  position: relative;
  z-index: 1;
}

/* Animaciones */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(30px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes pulseGlow {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-enter-from { opacity: 0; transform: translateX(30px); }
.slide-leave-to { opacity: 0; transform: translateX(-30px); }

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.modal-enter-from,
.modal-leave-to { opacity: 0; }
.modal-enter-from .modal-container,
.modal-leave-to .modal-container { transform: scale(0.9) translateY(20px); }

/* Estilos base para una mejor experiencia en cualquier dispositivo. */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #ffffff;
  background: linear-gradient(135deg, #000000 0%, #111827 100%);
  min-height: 100vh;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: linear-gradient(135deg, #000000 0%, #111827 100%);
}

.header {
  background: linear-gradient(135deg, #111827 0%, #000000 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 1.5rem 1rem;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
  flex-wrap: wrap;
  gap: 1rem;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.logo-text {
  font-size: 1.75rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ec4899 0%, #3b82f6 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.05em;
}

.greeting-card {
  text-align: left;
}

.greeting {
  font-size: 1.25rem;
  font-weight: 700;
  background: linear-gradient(90deg, #ec4899 0%, #3b82f6 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.2;
}

.greeting-subtitle {
  font-size: 0.875rem;
  color: #9ca3af;
  margin-top: 0.25rem;
}

.back-btn {
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  border: none;
  color: #ffffff;
  padding: 0.75rem 1.25rem;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-weight: 600;
  text-transform: uppercase;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  cursor: pointer;
}

.back-btn:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
}

/* Navegación */
.nav-container {
  background: #000000;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-tabs {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
}

.nav-tab {
  flex: 1;
  background: transparent;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  padding: 0;
}

.tab-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  position: relative;
  opacity: 0.6;
}

.nav-tab.active .tab-content {
  opacity: 1;
}

.nav-tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 3px;
  background: linear-gradient(90deg, #ec4899 0%, #3b82f6 100%);
  border-radius: 3px 3px 0 0;
}

.tab-icon {
  color: #ffffff;
  transition: transform 0.3s ease, color 0.3s ease;
}

.nav-tab.active .tab-icon {
  color: #ec4899;
  transform: scale(1.1);
}

.tab-text {
  font-weight: 600;
  font-size: 0.75rem;
  color: #ffffff;
}

.tab-badge {
  position: absolute;
  top: 0.25rem;
  right: 0.25rem;
  background: linear-gradient(135deg, #ec4899 0%, #3b82f6 100%);
  color: #ffffff;
  font-size: 0.625rem;
  font-weight: 700;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Contenido Principal */
.main-content {
  flex-grow: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem 1rem;
  width: 100%;
}

/* Sección de filtros */
.filter-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 2rem;
}

.search-input,
.date-filter {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  padding: 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  width: 100%;
  transition: all 0.3s ease;
}

.search-input::placeholder,
.date-filter::placeholder {
  color: #9ca3af;
}

.search-input:focus,
.date-filter:focus {
  outline: none;
  border-color: #ec4899;
  box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.3);
}

.date-filter {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  padding-right: 2rem;
  cursor: pointer;
}

.date-filter option {
  background-color: #111827;
  color: #ffffff;
}

/* Sección de tareas */
.task-section {
  min-height: 400px;
}

/* Grid de tareas */
.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.task-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 1.25rem;
  backdrop-filter: blur(20px);
  transition: all 0.4s ease;
  animation: slideInUp 0.6s ease;
  animation-delay: var(--delay);
  animation-fill-mode: both;
  position: relative;
  overflow: hidden;
}

.task-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #ec4899 0%, #3b82f6 100%);
}

.task-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.2);
}

.pending-task:hover::before {
  background: linear-gradient(90deg, #3b82f6 0%, #ec4899 100%);
}

.completed-task {
  opacity: 0.8;
  border-color: rgba(255, 255, 255, 0.05);
}

.completed-task::before {
  background: #252836;
}

.completed-task:hover {
  opacity: 1;
}

.task-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 1rem;
}

.task-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #ffffff;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background: #ec4899;
  transform: scale(1.1);
}

.completion-badge {
  background: linear-gradient(135deg, #ec4899 0%, #3b82f6 100%);
  border-radius: 12px;
  padding: 0.5rem;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.task-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.task-meta {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #9ca3af;
  font-size: 0.875rem;
}

.completed-date {
  color: #ec4899;
}

.original-date {
  color: #6b7280;
  font-size: 0.8rem;
}

.task-footer {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

.complete-btn {
  background: linear-gradient(135deg, #ec4899 0%, #3b82f6 100%);
  border: none;
  color: #ffffff;
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
}

.complete-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(236, 72, 153, 0.4);
}

/* Estado vacío */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-illustration {
  margin-bottom: 1.5rem;
  opacity: 0.3;
}

.empty-illustration svg {
  stroke: #ec4899;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.5rem;
}

.empty-subtitle {
  color: #9ca3af;
  font-size: 1rem;
  max-width: 400px;
}

/* Pie de página */
.footer {
  background: #000000;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem 1rem;
  text-align: center;
  color: #6b7280;
  font-size: 0.875rem;
  margin-top: auto;
}

/* Banner informativo en pestaña Terminadas */
.completed-info-banner {
  background: linear-gradient(90deg, rgba(236, 72, 153, 0.2), rgba(59, 130, 246, 0.2));
  border: 1px solid rgba(236, 72, 153, 0.4);
  border-radius: 16px;
  padding: 1.25rem;
  margin-bottom: 2rem;
  text-align: center;
  font-size: 0.95rem;
  color: #e0e0ff;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.completed-info-banner p {
  margin: 0;
  line-height: 1.6;
}

.completed-info-banner strong {
  color: #ec4899;
  font-size: 1.05rem;
  background: linear-gradient(90deg, #ec4899, #3b82f6);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Media Queries para Responsive Design */

/* Teléfonos pequeños y medianos (menos de 768px) */
@media (max-width: 768px) {
  .header {
    padding: 1rem;
    position: sticky;
    top: 0;
    z-index: 100;
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .logo-section {
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
    order: -1;
  }

  .logo-text {
    font-size: 1.5rem;
  }

  .greeting-card {
    text-align: center;
  }

  .greeting {
    font-size: 1.25rem;
  }

  .greeting-subtitle {
    font-size: 0.8rem;
  }

  .back-btn {
    width: 100%;
    padding: 0.65rem 1rem;
  }

  .nav-container {
    position: sticky;
    top: 130px;
    z-index: 99;
  }
  
  .main-content {
    padding: 1rem;
    background: transparent;
  }

  .filter-section {
    background: transparent;
  }

  .task-section {
    background: transparent;
  }
  
  .tasks-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .task-card {
    padding: 1rem;
  }

  .task-title {
    font-size: 1rem;
  }
  
  .complete-btn {
    padding: 0.65rem 1rem;
    font-size: 0.8rem;
  }

  .modal-container {
    margin: 1rem;
  }

  .modal-header,
  .modal-body,
  .modal-footer {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .modal-footer {
    flex-direction: column;
  }

  .empty-state {
    padding: 3rem 1rem;
  }

  .empty-title {
    font-size: 1.25rem;
  }

  .empty-subtitle {
    font-size: 0.9rem;
  }

  .completed-info-banner {
    font-size: 0.85rem;
    padding: 1rem;
  }
}

/* Escritorio (más de 768px) */
@media (min-width: 769px) {
  .filter-section {
    display: flex;
    flex-direction: row;
  }
  
  .search-input,
  .date-filter {
    width: auto;
  }

  .header-content {
    padding: 1.5rem 2rem;
  }

  .logo-section {
    flex-wrap: nowrap;
  }

  .logo-text {
    font-size: 2rem;
  }

  .greeting {
    font-size: 1.5rem;
  }

  .greeting-subtitle {
    font-size: 0.9rem;
  }
  
  .main-content {
    padding: 2rem;
  }

  .tasks-grid {
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  }
  
  .task-card {
    padding: 1.5rem;
  }
}
</style>