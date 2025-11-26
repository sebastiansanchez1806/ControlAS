<template>
  <div class="app-container">
    <header class="header">
      <div class="header-content">
        
        <button @click="handleBack" class="back-button">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          Volver
        </button>
        
        <div class="logo">
          <h1>Control AS</h1>
          <p>Bienvenido {{ userStore.nombre }}!!</p>
        </div>
        <div class="header-actions">
          <button @click="openAddModal" class="add-button" :class="{ 'button-disabled': !canCreateMore }">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 5v14M5 12h14"/>
            </svg>
            Agregar Local
          </button>
          
          <button v-if="hasBurdelBars" @click="goToPersonal" class="personal-button">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
              <circle cx="9" cy="7" r="4"/>
              <path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>
            </svg>
            Personal
          </button>
          
          <button @click="goToConfiguracion" class="gear-button">
            ⚙️
          </button>
          
        </div>
      </div>
      <div class="header-divider glitch-divider"></div>
      
      <!-- Barra de información de límite de locales -->
      <div v-if="limitInfo" class="limit-info-bar">
        <div class="limit-content">
          <span class="limit-text">
            Locales: {{ limitInfo.cantidad_actual }} / {{ limitInfo.cantidad_permitida }}
          </span>
          <div class="limit-progress">
            <div 
              class="limit-progress-fill" 
              :style="{ width: (limitInfo.cantidad_actual / limitInfo.cantidad_permitida * 100) + '%' }"
              :class="{ 'limit-reached': !limitInfo.puede_crear_mas }"
            ></div>
          </div>
          <span v-if="!limitInfo.puede_crear_mas" class="limit-warning">
            ⚠️ Límite alcanzado
          </span>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div class="content-wrapper">
        <div class="section-title">
          <h2>Mis Locales</h2>
          <p>Gestiona todos tus establecimientos desde aquí</p>
        </div>

        <div class="bars-grid">
          <div v-if="bars.length === 0 && noBarsMessage" class="no-bars-message">
              <p>{{ noBarsMessage }}</p>
              <button @click="openAddModal" class="add-first-bar-button" :class="{ 'button-disabled': !canCreateMore }">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 5v14M5 12h14"/>
                </svg>
                Agrega tu primer local
              </button>
          </div>

          <div
            v-for="bar in bars"
            :key="bar.id"
            class="bar-card"
            >
            <div class="bar-image">
              <img :src="bar.image" :alt="bar.name" />
              <div class="image-overlay"></div>
            </div>
            <div class="bar-info">
              <h3 class="bar-name">{{ bar.name }}</h3>
              <p class="bar-location">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10 3H3v7h7V3zM21 3h-7v7h7V3zM10 14H3v7h7v-7zM21 14h-7v7h7v-7z"/>
                </svg>
                ID: {{ bar.id }}
              </p>

              <p class="bar-location">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                {{ bar.location }}
              </p>
              <p class="bar-location">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" 
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 3h16l-7 7v7l3 3H8l3-3v-7z"/>
                </svg>
                {{ bar.tipo }}
              </p>

              <div class="card-actions">
                <button @click.stop="handleBarClick(bar)" class="enter-button">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="15 17 20 12 15 7"/>
                    <path d="M4 12h16"/>
                  </svg>
                  Entrar
                </button>

                <div class="options-menu">
                  <button @click.stop="toggleMenu(bar.id, bar.name, $event)" class="menu-button">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="1"/>
                      <circle cx="12" cy="5" r="1"/>
                      <circle cx="12" cy="19" r="1"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div v-if="showNotification" class="notification-overlay">
      <div class="notification-card">
        <small class="notification-text">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-8.63"/>
            <polyline points="22 4 12 14.01 9 11.01"/>
          </svg>
          {{ notificationMessage }}
        </small>
      </div>
    </div>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-logo">
          <h3>Control AS</h3>
          <p>Sistema de Gestión</p>
        </div>
        <div class="footer-info">
          <p>&copy; 2025 Control AS. Todos los derechos reservados.</p>
          <p>Soluciones empresariales profesionales</p>
        </div>
      </div>
    </footer>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path v-if="!isEditing" d="M12 5v14M5 12h14"/>
              <path v-else d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            </svg>
            {{ isEditing ? 'Editar Local' : 'Nuevo Local' }}
          </h2>
          <button @click="closeModal" class="close-button">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="submitForm" class="bar-form">
          <div class="form-row">
            <div class="form-group">
              <label for="name">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                  <polyline points="9,22 9,12 15,12 15,22"/>
                </svg>
                Nombre del Local
              </label>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                required
                class="form-input"
                placeholder="Ej: La Terraza Dorada"
              />
            </div>
          </div>

          <div v-if="!isEditing" class="form-row">
            <div class="form-group">
              <label>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M10 20H4a2 2 0 0 1-2-2V5c0-1.1.9-2 2-2h3.93a2 2 0 0 1 1.66.75L12 6h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-9"/>
                </svg>
                Tipo de Local
              </label>
              <div class="tipo-local-selector">
                <button
                  type="button"
                  @click="formData.tipo = 'bar'"
                  :class="['tipo-button', { active: formData.tipo === 'bar' }]"
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 8v13m0-13V6a2 2 0 0 1 2-2h1a2 2 0 0 1 2 2v2m-5 0h5"/>
                  </svg>
                  Bar
                </button>
                <button
                  type="button"
                  @click="formData.tipo = 'burdel'"
                  :class="['tipo-button', { active: formData.tipo === 'burdel' }]"
                >
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                  </svg>
                  Burdel
                </button>
              </div>
              <small class="form-help">Selecciona la categoría del establecimiento.</small>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="location">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                Ubicación
              </label>
              <input
                id="location"
                v-model="formData.location"
                type="text"
                required
                class="form-input"
                placeholder="Ej: Zona Rosa, Bogotá"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="image-upload">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <circle cx="8.5" cy="8.5" r="1.5"/>
                  <polyline points="21,15 16,10 5,21"/>
                </svg>
                Imagen del Local
              </label>
              <div class="image-upload-area" @click="triggerFileUpload">
                <template v-if="formData.image">
                  <img :src="formData.image" :alt="formData.name || 'Imagen del local'" class="uploaded-image-preview"/>
                  <div class="image-upload-overlay">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M12 5v14M5 12h14"/>
                    </svg>
                    <span>Cambiar imagen</span>
                  </div>
                </template>
                <template v-else>
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                    <path d="M12 5v14M5 12h14"/>
                  </svg>
                  <p>Arrastra y suelta tu imagen aquí o haz clic para subir</p>
                  <small>JPG, PNG, GIF (Máx 5MB)</small>
                </template>
                <input
                  id="image-upload"
                  type="file"
                  accept="image/jpeg, image/png, image/gif"
                  @change="handleFileUpload"
                  class="hidden-file-input"
                />
              </div>
              <small class="form-help">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="8" x2="12" y2="12"/>
                  <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
                Sube una imagen desde tus archivos.
              </small>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="cancel-button">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
              Cancelar
            </button>
            <button type="submit" class="submit-button" :disabled="isLoading">
              <svg v-if="!isLoading" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20,6 9,17 4,12"/>
              </svg>
              <svg v-else class="spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
              </svg>
              {{ isEditing ? 'Actualizar' : (isLoading ? 'Creando...' : 'Crear') }} Local
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showDeleteModal" class="modal-overlay" @click="closeDeleteModal">
      <div class="modal-content delete-modal" @click.stop>
        <div class="modal-header">
          <h2>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            Confirmar Eliminación
          </h2>
          <button @click="closeDeleteModal" class="close-button">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="delete-content">
          <div class="warning-section">
            <div class="warning-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            </div>
            <p class="delete-message">
              ¿Estás seguro de que deseas eliminar este local?
            </p>
          </div>

          <div class="local-preview" v-if="barToDelete">
            <div class="local-image">
              <img :src="barToDelete.image" :alt="barToDelete.name" />
            </div>
            <div class="local-details">
              <h4>{{ barToDelete.name }}</h4>
            </div>
          </div>
          <div class="warning-text">
            <p>Esta acción no se puede deshacer. El local será eliminado permanentemente del sistema.</p>
          </div>
        </div>

        <div class="form-actions">
          <button @click="closeDeleteModal" class="cancel-button">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            Cancelar
          </button>
          <button @click="deleteBar" class="delete-confirm-button">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3,6 5,6 21,6"/>
              <path d="m19,6v14a2,2 0,0 1-2,2H7a2,2 0,0 1-2-2V6m3,0V4a2,2 0,0 1,2-2h4a2,2 0,0 1,2,2v2"/>
            </svg>
            Sí, eliminar local
          </button>
        </div>
      </div>
    </div>

    <div v-if="activeMenu && !showModal && !showDeleteModal" class="menu-popover-overlay" @click="closeMenu">
      <div class="menu-popover" @click.stop :style="{ top: popoverPosition.top + 'px', left: popoverPosition.left + 'px' }">
        <h4 class="popover-title">{{ activeBarName }}</h4>
        <button @click.stop="editBar(activeMenuId)" class="menu-item">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="m18.5 2.5-3 3L22 12l-5.5 5.5-3-3z"/>
          </svg>
          Editar
        </button>
        <button @click.stop="confirmDelete(activeMenuId)" class="menu-item delete">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3,6 5,6 21,6"/>
            <path d="m19,6v14a2,2 0,0 1-2,2H7a2,2 0,0 1-2-2V6m3,0V4a2,2 0,0 1,2-2h4a2,2 0,0 1,2,2v2"/>
          </svg>
          Eliminar
        </button>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue';
import { useUserStore } from '@/stores/user';
import { useActiveBarStore } from '../stores/activeBar';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { API_BASE_URL } from '../config/api';
import Swal from 'sweetalert2';

export default {
  name: 'Locales',
  setup() {
    const bars = ref([]);
    const userStore = useUserStore();
    const activeBarStore = useActiveBarStore();
    const router = useRouter();

    const showModal = ref(false);
    const showDeleteModal = ref(false);
    const isEditing = ref(false);
    const activeMenu = ref(null);
    const activeMenuId = ref(null);
    const activeBarName = ref('');
    const currentBarId = ref(null);
    const barToDelete = ref(null);
    const popoverPosition = reactive({ top: 0, left: 0 });

    const noBarsMessage = ref('');
    const notificationMessage = ref('');
    const showNotification = ref(false);
    const isLoading = ref(false);
    
    const hasBurdelBars = ref(false);
    const limitInfo = ref(null);
    
    const canCreateMore = computed(() => {
  const result = limitInfo.value ? limitInfo.value.puede_crear_mas : true;
  console.log('🔍 canCreateMore:', result);
  console.log('📊 limitInfo completo:', limitInfo.value);
  return result;
});

    const formData = reactive({
      name: '',
      location: '',
      image: '',
      tipo: 'bar'
    });

    const fetchLimitInfo = async () => {
      if (!userStore.id) return;
      
      try {
        const response = await axios.get(`${API_BASE_URL}/dueno/${userStore.id}/info`);
        limitInfo.value = response.data;
        console.log('📊 Info de límites:', limitInfo.value);
      } catch (error) {
        console.error('Error al obtener información de límites:', error);
        limitInfo.value = null;
      }
    };

    const updateHasBurdelBars = () => {
      hasBurdelBars.value = bars.value.some(bar => {
        const tipoNormalizado = bar.tipo ? bar.tipo.trim().toLowerCase() : '';
        return tipoNormalizado === 'burdel';
      });
      console.log('🌐 Actualizando hasBurdelBars:', hasBurdelBars.value);
    };
    
    const showSuccessNotification = (message) => {
      notificationMessage.value = message;
      showNotification.value = true;
      setTimeout(() => {
        showNotification.value = false;
        notificationMessage.value = '';
      }, 3000);
    };

    const fetchBars = async () => {
      if (!userStore.id) {
        console.warn('userStore.id no está disponible. No se pueden cargar los bares.');
        noBarsMessage.value = 'No se pudo cargar la información de tus bares. Por favor, asegúrate de haber iniciado sesión.';
        bars.value = [];
        updateHasBurdelBars();
        return;
      }

      try {
        const response = await axios.get(`${API_BASE_URL}/bares/dueno/${userStore.id}`);
        console.log('📥 Respuesta del backend:', response.data);
        
        if (response.data && response.data.bares && response.data.bares.length > 0) {
          bars.value = response.data.bares.map(bar => {
            console.log('🔍 Mapeando bar:', bar);
            return {
              id: bar.id,
              name: bar.nombre,
              location: bar.ubicacion,
              image: bar.imagen,
              dueno_id: bar.dueno_id,
              tipo: bar.tipo? bar.tipo.trim().toLowerCase() : 'bar'
            };
          });
          console.log('✅ Bares mapeados:', bars.value);
          noBarsMessage.value = '';
        } else {
          bars.value = [];
          noBarsMessage.value = response.data.mensaje || 'No tienes bares registrados aún.';
        }
        
        updateHasBurdelBars();
        await fetchLimitInfo();
        
      } catch (error) {
        console.error('Error al obtener los bares:', error);
        bars.value = [];
        noBarsMessage.value = 'Error al cargar tus bares. Intenta recargar la página.';
        updateHasBurdelBars();
      }
    };
const submitForm = async () => {
  // Validación: Si no está editando y no puede crear más locales
  if (!isEditing.value && !canCreateMore.value) {
    await Swal.fire({
      icon: 'warning',
      title: 'Límite alcanzado',
      html: `
        <p style="margin-bottom: 15px; font-size: 1.1rem; color: #E0E0E0;">
          Has alcanzado el límite de <strong style="color: #4A90E2;">${limitInfo.value.cantidad_permitida}</strong> locales permitidos.
        </p>
        <p style="margin-bottom: 15px; font-size: 1rem; color: #B0B0B0;">
          Comunícate con servicio al cliente para obtener más locales:
        </p>
        <a 
          href="https://wa.me/573213686373?text=Hola,%20necesito%20aumentar%20mi%20límite%20de%20locales" 
          target="_blank" 
          style="
            font-size: 1.3rem; 
            font-weight: bold; 
            color: #25D366; 
            text-decoration: none; 
            display: inline-flex; 
            align-items: center; 
            gap: 10px;
            padding: 12px 20px;
            background: rgba(37, 211, 102, 0.1);
            border-radius: 10px;
            transition: all 0.3s ease;
          "
          onmouseover="this.style.background='rgba(37, 211, 102, 0.2)'; this.style.transform='scale(1.05)';"
          onmouseout="this.style.background='rgba(37, 211, 102, 0.1)'; this.style.transform='scale(1)';"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
          📱 321 368 6373
        </a>
      `,
      confirmButtonText: 'Entendido',
      confirmButtonColor: '#4A90E2',
      background: '#15151F',
      color: '#E0E0E0',
      customClass: {
        popup: 'swal-custom-popup',
        title: 'swal-custom-title',
        confirmButton: 'swal-custom-confirm'
      }
    });
    return;
  }

  isLoading.value = true;
  
  try {
    const tipoNormalizado = formData.tipo.trim().toLowerCase();
    
    if (isEditing.value) {
      // MODO EDICIÓN: Actualizar local existente
      const response = await axios.put(`${API_BASE_URL}/bares_actualizar/${currentBarId.value}`, {
        nombre: formData.name,
        ubicacion: formData.location,
        imagen: formData.image
      });

      if (response.data && response.data.bar) {
        const index = bars.value.findIndex(bar => bar.id === currentBarId.value);
        if (index !== -1) {
          const updatedBar = {
            id: response.data.bar.id,
            name: response.data.bar.nombre,
            location: response.data.bar.ubicacion,
            image: response.data.bar.imagen,
            tipo: (response.data.bar.tipo_local || bars.value[index].tipo).trim().toLowerCase()
          };
          bars.value.splice(index, 1, updatedBar);
        }
        showSuccessNotification('¡Local actualizado con éxito!');
      }
    } else {
      // MODO CREACIÓN: Crear nuevo local
      const payload = {
        nombre: formData.name,
        ubicacion: formData.location,
        imagen: formData.image,
        dueno_id: userStore.id,
        tipo: tipoNormalizado
      };
      
      console.log('📤 Enviando al backend:', payload);
      
      // Validaciones antes de enviar
      if (!payload.dueno_id) {
        throw new Error('Error: dueno_id no está definido');
      }
      
      if (!payload.tipo || !['bar', 'burdel'].includes(payload.tipo)) {
        throw new Error(`Error: tipo '${payload.tipo}' no es válido. Debe ser 'bar' o 'burdel'`);
      }
      
      const response = await axios.post(`${API_BASE_URL}/crea_bares`, payload);

      if (response.data && response.data.bar) {
        await fetchBars(); // Recargar la lista de bares
        showSuccessNotification('¡Local creado con éxito!');
      }
    }
    
    closeModal();
    updateHasBurdelBars();
    
  } catch (error) {
    console.error('❌ Error completo:', error);
    console.error('📋 Detalles del error:', error.response?.data);
    
    // Manejo de errores específicos
    if (error.response?.data?.detail) {
      let errorMsg = '';
      
      // Si el detail es un array (errores de validación de FastAPI)
      if (Array.isArray(error.response.data.detail)) {
        errorMsg = error.response.data.detail.map(err => err.msg || err).join(', ');
      } else {
        errorMsg = error.response.data.detail;
      }
      
      await Swal.fire({
        icon: 'error',
        title: 'Error',
        html: `
          <p style="margin-bottom: 10px;">Error al ${isEditing.value ? 'actualizar' : 'crear'} el local:</p>
          <p style="color: #FF6B6B; font-weight: 600;">${errorMsg}</p>
        `,
        confirmButtonColor: '#FF0000',
        background: '#15151F',
        color: '#E0E0E0',
        customClass: {
          popup: 'swal-custom-popup',
          title: 'swal-custom-title',
          confirmButton: 'swal-custom-confirm'
        }
      });
    } else if (error.message) {
      // Error con mensaje personalizado
      await Swal.fire({
        icon: 'error',
        title: 'Error',
        text: error.message,
        confirmButtonColor: '#FF0000',
        background: '#15151F',
        color: '#E0E0E0',
        customClass: {
          popup: 'swal-custom-popup',
          title: 'swal-custom-title',
          confirmButton: 'swal-custom-confirm'
        }
      });
    } else {
      // Error genérico
      await Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Ocurrió un error inesperado. Por favor, intenta de nuevo.',
        confirmButtonColor: '#FF0000',
        background: '#15151F',
        color: '#E0E0E0',
        customClass: {
          popup: 'swal-custom-popup',
          title: 'swal-custom-title',
          confirmButton: 'swal-custom-confirm'
        }
      });
    }
  } finally {
    isLoading.value = false;
  }
};

    const deleteBar = async () => {
      if (!barToDelete.value) return;

      try {
        const { value: password, isDismissed } = await Swal.fire({
          title: 'Verificación requerida',
          html: `
            <p style="margin-bottom: 15px; color: #E0E0E0;">
              Para eliminar <strong style="color: #FF69B4;">${barToDelete.value.name}</strong>, 
              ingresa tu contraseña:
            </p>
            <div style="position: relative; width: 100%;">
              <input 
                id="password-input" 
                type="password" 
                placeholder="Ingresa tu contraseña"
                autocomplete="current-password"
                style="
                  width: 100%;
                  padding: 12px 45px 12px 16px;
                  background: rgba(255, 255, 255, 0.08);
                  border: 1px solid rgba(255, 255, 255, 0.15);
                  border-radius: 10px;
                  color: #F0F0F0;
                  font-size: 1rem;
                  box-sizing: border-box;
                "
              />
              <button 
                id="toggle-password" 
                type="button"
                style="
                  position: absolute;
                  right: 12px;
                  top: 50%;
                  transform: translateY(-50%);
                  background: transparent;
                  border: none;
                  color: #4A90E2;
                  cursor: pointer;
                  padding: 5px;
                  display: flex;
                  align-items: center;
                  justify-content: center;
                "
              >
                <svg id="eye-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
              </button>
            </div>
          `,
          showCancelButton: true,
          confirmButtonText: 'Verificar y Eliminar',
          cancelButtonText: 'Cancelar',
          confirmButtonColor: '#FF0000',
          cancelButtonColor: '#1A202C',
          background: '#15151F',
          color: '#E0E0E0',
          customClass: {
            popup: 'swal-custom-popup',
            title: 'swal-custom-title',
            confirmButton: 'swal-custom-confirm',
            cancelButton: 'swal-custom-cancel'
          },
          didOpen: () => {
            const passwordInput = document.getElementById('password-input');
            const toggleButton = document.getElementById('toggle-password');
            const eyeIcon = document.getElementById('eye-icon');
            
            let isPasswordVisible = false;
            
            toggleButton.addEventListener('click', () => {
              isPasswordVisible = !isPasswordVisible;
              passwordInput.type = isPasswordVisible ? 'text' : 'password';
              
              if (isPasswordVisible) {
                eyeIcon.innerHTML = `
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                `;
              } else {
                eyeIcon.innerHTML = `
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                `;
              }
            });
            
            passwordInput.focus();
          },
          preConfirm: () => {
            const password = document.getElementById('password-input').value;
            if (!password) {
              Swal.showValidationMessage('Debes ingresar tu contraseña');
              return false;
            }
            return password;
          }
        });

        if (isDismissed) {
          return;
        }

        Swal.fire({
          title: 'Verificando...',
          html: 'Por favor espera',
          allowOutsideClick: false,
          background: '#15151F',
          color: '#E0E0E0',
          didOpen: () => {
            Swal.showLoading();
          }
        });

        try {
          await axios.post(`${API_BASE_URL}/dueno/${userStore.id}/verify-password`, {
            password: password
          });

          await axios.delete(`${API_BASE_URL}/bares_eliminar/${barToDelete.value.id}`);
          
          Swal.close();
          
          await Swal.fire({
            icon: 'success',
            title: '¡Eliminado!',
            text: 'El local ha sido eliminado exitosamente',
            confirmButtonColor: '#4A90E2',
            background: '#15151F',
            color: '#E0E0E0',
            timer: 2000,
            timerProgressBar: true
          });

          await fetchBars();
          closeDeleteModal();
          updateHasBurdelBars();

        } catch (verifyError) {
          Swal.close();
          
          if (verifyError.response?.status === 401) {
            await Swal.fire({
              icon: 'error',
              title: 'Contraseña incorrecta',
              text: 'La contraseña ingresada no es válida. Por favor, intenta de nuevo.',
              confirmButtonColor: '#FF0000',
              background: '#15151F',
              color: '#E0E0E0'
            });
          } else {
            await Swal.fire({
              icon: 'error',
              title: 'Error',
              text: 'Ocurrió un error al verificar la contraseña. Intenta de nuevo.',
              confirmButtonColor: '#FF0000',
              background: '#15151F',
              color: '#E0E0E0'
            });
          }
        }

      } catch (error) {
        console.error('Error al eliminar el bar:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Ocurrió un error inesperado. Por favor, intenta de nuevo.',
          confirmButtonColor: '#FF0000',
          background: '#15151F',
          color: '#E0E0E0'
        });
      }
    };
const openAddModal = () => {
  // Verificar PRIMERO si puede crear más locales
  if (!canCreateMore.value) {
    Swal.fire({
      icon: 'warning',
      title: 'Límite alcanzado',
      html: `
        <p style="margin-bottom: 15px; font-size: 1.1rem; color: #E0E0E0;">
          Has alcanzado el límite de <strong style="color: #4A90E2;">${limitInfo.value.cantidad_permitida}</strong> locales permitidos.
        </p>
        <p style="margin-bottom: 15px; font-size: 1rem; color: #B0B0B0;">
          Comunícate con servicio al cliente para obtener más locales:
        </p>
        <a 
          href="https://wa.me/573213686373?text=Hola,%20necesito%20aumentar%20mi%20límite%20de%20locales" 
          target="_blank" 
          style="
            font-size: 1.3rem; 
            font-weight: bold; 
            color: #25D366; 
            text-decoration: none; 
            display: inline-flex; 
            align-items: center; 
            gap: 10px;
            padding: 12px 20px;
            background: rgba(37, 211, 102, 0.1);
            border-radius: 10px;
            transition: all 0.3s ease;
          "
          onmouseover="this.style.background='rgba(37, 211, 102, 0.2)'; this.style.transform='scale(1.05)';"
          onmouseout="this.style.background='rgba(37, 211, 102, 0.1)'; this.style.transform='scale(1)';"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
          📱 321 368 6373
        </a>
      `,
      confirmButtonText: 'Entendido',
      confirmButtonColor: '#4A90E2',
      background: '#15151F',
      color: '#E0E0E0',
      customClass: {
        popup: 'swal-custom-popup',
        title: 'swal-custom-title',
        confirmButton: 'swal-custom-confirm'
      }
    });
    return; // IMPORTANTE: Detener la ejecución aquí
  }
  
  // Solo llega aquí si puede crear más locales
  isEditing.value = false;
  resetForm();
  showModal.value = true;
  closeMenu();
};
    const editBar = (barId) => {
      const bar = bars.value.find(b => b.id === barId);
      if (bar) {
        isEditing.value = true;
        currentBarId.value = bar.id;
        formData.name = bar.name;
        formData.location = bar.location;
        formData.image = bar.image;
        formData.tipo = bar.tipo || 'bar';
        showModal.value = true;
        closeMenu();
      }
    };

    const confirmDelete = (barId) => {
      barToDelete.value = bars.value.find(bar => bar.id === barId);
      if (barToDelete.value) {
        showDeleteModal.value = true;
        closeMenu();
      }
    };

    const closeModal = () => {
      showModal.value = false;
      resetForm();
    };

    const closeDeleteModal = () => {
      showDeleteModal.value = false;
      barToDelete.value = null;
    };

    const resetForm = () => {
      formData.name = '';
      formData.location = '';
      formData.image = '';
      formData.tipo = 'bar';
      currentBarId.value = null;
    };

    const handleFileUpload = (event) => {
      const file = event.target.files?.[0];
      if (file) {
        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
          console.error('Por favor, sube un archivo de imagen (JPG, PNG, GIF).');
          alert('Por favor, sube un archivo de imagen válido (JPG, PNG o GIF).');
          formData.image = '';
          event.target.value = '';
          return;
        }

        const maxSize = 5 * 1024 * 1024;
        if (file.size > maxSize) {
          console.error('La imagen es demasiado grande. El tamaño máximo permitido es 5MB.');
          alert('La imagen es demasiado grande. El tamaño máximo permitido es 5MB.');
          formData.image = '';
          event.target.value = '';
          return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
          formData.image = e.target.result;
        };
        reader.onerror = () => {
          console.error('Error al leer el archivo');
          alert('Error al cargar la imagen. Por favor, intenta de nuevo.');
          formData.image = '';
        };
        reader.readAsDataURL(file);
      } else {
        formData.image = '';
      }
    };

    const triggerFileUpload = () => {
      const fileInput = document.getElementById('image-upload');
      if (fileInput) {
        fileInput.click();
      }
    };

    const handleBarClick = (bar) => {
      activeBarStore.setBar(bar);
      console.log(`Navegando a la gestión de "${bar.name}" con ID en Pinia: ${activeBarStore.id}`);
      router.push({ name: 'jefe_productos' });
    };

    const toggleMenu = (id, name, event) => {
      const buttonRect = event.currentTarget.getBoundingClientRect();
      popoverPosition.top = buttonRect.bottom + 10;
      popoverPosition.left = buttonRect.left;

      if (activeMenu.value === id) {
        closeMenu();
      } else {
        activeMenu.value = id;
        activeMenuId.value = id;
        activeBarName.value = name;
      }
    };

    const closeMenu = (event) => {
      if (activeMenu.value) {
        if (event) {
          const popoverElement = document.querySelector('.menu-popover');
          const menuButton = event.target.closest('.menu-button');

          if (popoverElement && !popoverElement.contains(event.target) && !menuButton) {
            activeMenu.value = null;
            activeBarName.value = '';
            activeMenuId.value = null;
          }
        } else {
          activeMenu.value = null;
          activeBarName.value = '';
          activeMenuId.value = null;
        }
      }
    };

    const handleBack = () => {
      userStore.logout();
      router.push({ name: 'Login' });
    };

    const goToPersonal = () => {
      router.push({ name: 'femenino' });
    };
    
    const goToConfiguracion = () => {
      router.push({ name: 'configuracion' });
    };

    onMounted(() => {
      console.log('🎯 Componente Locales montado');
      console.log('👤 Usuario ID:', userStore.id);
      fetchBars();
      document.addEventListener('click', closeMenu);
    });

    onUnmounted(() => {
      document.removeEventListener('click', closeMenu);
    });

    return {
      bars,
      showModal,
      showDeleteModal,
      isEditing,
      activeMenu,
      activeMenuId,
      activeBarName,
      formData,
      barToDelete,
      popoverPosition,
      userStore,
      noBarsMessage,
      notificationMessage,
      showNotification,
      isLoading,
      hasBurdelBars,
      limitInfo,
      canCreateMore,
      openAddModal,
      editBar,
      confirmDelete,
      deleteBar,
      closeModal,
      closeDeleteModal,
      submitForm,
      handleBarClick,
      toggleMenu,
      closeMenu,
      handleFileUpload,
      triggerFileUpload,
      handleBack,
      goToPersonal,
      goToConfiguracion
    };
  }
};
</script>
<style scoped>
/* --- Estilos Generales y Reseteo --- */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';
  line-height: 1.6;
  color: #E0E0E0;
  background: #0A0A0F;
  transition: background 0.5s ease;
}

.app-container {
  min-height: 100vh;
  background: linear-gradient(145deg, #0A0A0F 0%, #050507 100%);
  color: #E0E0E0;
  display: flex;
  flex-direction: column;
}

/* --- Header y Logo (Estilos Glitch) --- */
.header {
  background: #050507;
  padding: 25px 0 0;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px 25px;
  position: relative;
  flex-wrap: wrap;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.logo {
  text-align: center;
  flex-grow: 1;
}

.logo h1 {
  font-size: 3.8rem;
  margin: 0;
  font-weight: 900;
  color: #FFFFFF;
  letter-spacing: 3px;
  text-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
  animation: glitch 1.5s infinite alternate-reverse;
}

.logo p {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.7;
  margin-top: -8px;
  font-weight: 400;
  color: #A0A0A0;
}

.header-divider {
  height: 2px;
  background: linear-gradient(90deg, transparent, #4A90E2, #FF69B4, transparent);
  width: 100%;
  position: relative;
  overflow: hidden;
  margin-top: 5px;
  box-shadow: 0 2px 10px rgba(74, 144, 226, 0.5);
}

.glitch-divider::before,
.glitch-divider::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: inherit;
  opacity: 0;
}

.glitch-divider::before {
  animation: glitch-line 1.5s infinite linear alternate-reverse;
  filter: hue-rotate(90deg);
}

.glitch-divider::after {
  animation: glitch-line 1.5s infinite linear alternate-reverse 0.2s;
  filter: hue-rotate(180deg);
}

/* --- Botones de Acción Global --- */
.header-actions button {
  color: #fff;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease, transform 0.2s ease;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';
  font-size: 0.9rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.back-button {
  background: #1A202C; 
  color: #E0E0E0;
  border: 2px solid transparent;
  background-clip: padding-box;
  position: relative;
  padding: 12px 24px;
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
  cursor: pointer;
  user-select: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
}

.back-button:hover {
  background: #2D3748;
  transform: translateY(-3px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.3);
}

.back-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  background-color: #151821;
}

.back-button::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: -1;
  margin: -2px;
  border-radius: inherit;
  background: linear-gradient(45deg, #4A90E2, #FF69B4);
  transition: opacity 0.3s ease;
  opacity: 0; /* Inicialmente transparente */
}

.back-button:hover::before {
  opacity: 1; /* Muestra el brillo al pasar el ratón */
}

.back-button:active::before {
  opacity: 0;
}

.add-button {
  background-color: #4A90E2; /* Azul */
  box-shadow: 0 4px 10px rgba(74, 144, 226, 0.5);
}

.add-button:hover {
  background-color: #357ABD;
  box-shadow: 0 6px 15px rgba(53, 122, 189, 0.5);
  transform: translateY(-2px);
}

.add-button:active {
  background-color: #2a65a3;
  transform: translateY(0);
}

.personal-button {
  background-color: #FF69B4; /* Rosado */
  box-shadow: 0 4px 10px rgba(255, 105, 180, 0.5);
}

.personal-button:hover {
  background-color: #E65A9C;
  box-shadow: 0 6px 15px rgba(230, 90, 156, 0.5);
  transform: translateY(-2px);
}

.personal-button:active {
  background-color: #D64A8A;
  transform: translateY(0);
}

.personal-button svg {
  stroke: white;
}

.gear-button {
  background-color: #222; 
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease, background-color 0.3s ease;
}

.gear-button:hover {
  background-color: #444; 
  transform: rotate(90deg);
}

/* --- Interactive/Selectable Glow Buttons (NUEVOS ESTILOS DE LUMINOSIDAD) --- */

/** * Botón genérico para elementos de navegación o selección 
 * que deben "encenderse" al ser seleccionados.
 * Aplica la clase .active para el efecto de brillo.
 */
.glow-select-button {
  background-color: #1A202C; /* Fondo oscuro base */
  color: #E0E0E0;
  border: 1px solid rgba(74, 144, 226, 0.1);
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.glow-select-button:hover {
  background-color: #2D3748;
  border-color: #4A90E2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

.glow-select-button.active {
  /* Estado Seleccionado: Se ilumina */
  background: linear-gradient(90deg, #4A90E2, #FF69B4); /* Fondo de acento */
  color: #FFF;
  font-weight: 700;
  border-color: #FF69B4;
  
  /* El Efecto de Brillo Luminoso (Glow) */
  box-shadow: 
    0 0 8px rgba(74, 144, 226, 0.8), /* Brillo Azul 1 */
    0 0 16px rgba(74, 144, 226, 0.5), /* Brillo Azul 2 */
    0 0 24px rgba(255, 105, 180, 0.8), /* Brillo Rosado 1 */
    0 0 32px rgba(255, 105, 180, 0.3), /* Brillo Rosado 2 */
    inset 0 0 10px rgba(255, 255, 255, 0.4); /* Resalte blanco interior */

  transform: scale(1.03);
  text-shadow: 0 0 4px #FFF;
}

/* --- Contenido Principal --- */
.main-content {
  flex: 1;
  padding: 60px 20px;
}

.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.section-title {
  text-align: center;
  margin-bottom: 60px;
}

.section-title h2 {
  font-size: 3rem;
  margin: 0 0 15px 0;
  background: linear-gradient(45deg, #4A90E2, #FF69B4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 800;
  letter-spacing: 1px;
}

.section-title p {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-weight: 500;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.3);
}

.bars-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 35px;
  justify-items: center;
}

.bar-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
  cursor: default;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  backdrop-filter: blur(10px);
  width: 100%;
  max-width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1);
}

.bar-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 20px 40px rgba(74, 144, 226, 0.3), 0 0 0 2px rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 105, 180, 0.4);
}

.bar-image {
  height: 240px;
  overflow: hidden;
  position: relative;
  border-radius: 20px 20px 0 0;
}

.bar-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 40%, rgba(0, 0, 0, 0.6) 100%);
}

.bar-card:hover .bar-image img {
  transform: scale(1.15);
}

.bar-info {
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.bar-name {
  font-size: 1.8rem;
  margin: 0 0 15px 0;
  background: linear-gradient(45deg, #FF69B4, #4A90E2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
  line-height: 1.3;
  text-shadow: 1px 1px 0 rgba(255, 255, 255, 0.2), -1px -1px 0 rgba(255, 255, 255, 0.2), 1px -1px 0 rgba(255, 255, 255, 0.2), -1px 1px 0 rgba(255, 255, 255, 0.2);
}

.bar-location {
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.05rem;
  display: flex;
  align-items: center;
  gap: 10px;
  text-shadow: 0 0 2px rgba(255, 255, 255, 0.1);
}

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-top: 15px;
}

.enter-button {
  background: linear-gradient(90deg, #4A90E2, #FF69B4);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 15px rgba(74, 144, 226, 0.4);
}

.enter-button:hover {
  background: linear-gradient(90deg, #FF69B4, #4A90E2);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.4);
}

.options-menu {
  position: relative;
  z-index: 10;
}

.menu-button {
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  border-radius: 50%;
  width: 42px;
  height: 42px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  margin-left: 15px;
}

.menu-button:hover {
  background: rgba(255, 105, 180, 0.9);
  transform: scale(1.15);
}

.no-bars-message {
  grid-column: 1 / -1;
  text-align: center;
  padding: 40px 20px;
  background-color: #2a2a2e;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #e0e0e0;
}

.no-bars-message p {
  font-size: 1.3rem;
  margin-bottom: 25px;
  font-weight: 500;
}
.add-first-bar-button {
  background-color: #007bff;
  color: white;
  padding: 12px 25px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background-color 0.3s ease, transform 0.2s ease;
  text-decoration: none;
}

.add-first-bar-button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.add-first-bar-button svg {
  color: white;
}


/* --- Footer --- */
.footer {
  background: #050507;
  padding: 40px 0;
  margin-top: auto;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.4);
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  flex-wrap: wrap;
}

.footer-content > * {
  text-align: center;
}

.footer-logo h3 {
  font-size: 2.2rem;
  margin: 0;
  font-weight: 900;
  color: #FFFFFF;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  animation: glitch 1.5s infinite alternate-reverse;
}

.footer-logo p {
  margin: 0;
  font-size: 0.95rem;
  opacity: 0.7;
  color: #A0A0A0;
}

.footer-info {
  text-align: right;
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.6);
}

.footer-info p {
  margin: 5px 0;
  opacity: 0.9;
}

/* --- Modales y Formularios --- */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.88);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(12px);
  animation: fadeIn 0.3s ease-out forwards;
}

.modal-content {
  background: #15151F;
  border-radius: 28px;
  padding: 50px;
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  color: #E0E0E0;
  box-shadow: 0 35px 70px rgba(0, 0, 0, 0.6);
  border: 1px solid rgba(74, 144, 226, 0.3);
  animation: scaleIn 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) forwards;
}

.delete-modal {
  max-width: 550px; /* Reducido de 650px */
  padding: 35px !important; /* Reducido de 50px */
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding-bottom: 25px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
  font-size: 1.5rem !important; /* Reducido */
  font-weight: 600;
  color: #FFFFFF;
  display: flex;
  align-items: center;
  gap: 10px;
  text-shadow: 0 0 4px rgba(255, 255, 255, 0.2);
}
.modal-header h2 svg {
  width: 18px; /* Reducido */
  height: 18px;
}
.close-button {
  background: transparent;
  border: none;
  color: #A0A0A0;
  cursor: pointer;
  font-size: 2rem;
  transition: color 0.2s ease, transform 0.2s ease;
  padding: 0px;
  border-radius: 50%;
}

.close-button:hover {
  color: #FF69B4;
  transform: rotate(90deg);
}

.bar-form .form-group {
  margin-bottom: 28px;
}

.bar-form label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.1rem;
  color: #B0B0B0;
  margin-bottom: 12px;
  font-weight: 500;
  text-shadow: 0 0 1px rgba(255, 255, 255, 0.1);
}

.form-input {
  width: 100%;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  color: #F0F0F0;
  font-size: 1.05rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  text-shadow: 0 0 1px rgba(255, 255, 255, 0.05);
}

.form-input::placeholder {
  color: rgba(208, 208, 208, 0.4);
}

.form-input:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.3);
  background: rgba(255, 255, 255, 0.12);
}

.image-upload-area {
  background: rgba(255, 255, 255, 0.05);
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  transition: all 0.3s ease;
  cursor: pointer;
  margin-top: 15px;
  position: relative;
  overflow: hidden;
}

.image-upload-area:hover {
  border-color: #4A90E2;
  background: rgba(74, 144, 226, 0.08);
}

.hidden-file-input {
  display: none;
}

.uploaded-image-preview {
  max-width: 100%;
  max-height: 100%;
  border-radius: 6px;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.image-upload-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}

.image-upload-area:hover .image-upload-overlay {
  opacity: 1;
}

.image-upload-overlay svg {
  color: white;
  margin-bottom: 5px;
}

.image-upload-overlay span {
  font-weight: bold;
}

.image-upload-area p {
  color: #E0E0E0;
  font-size: 0.9em;
  text-align: center;
  margin: 0;
}

.image-upload-area small {
  color: #A0A0A0;
  font-size: 0.75em;
  margin-top: 5px;
}

.form-help {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  margin-top: 40px;
  padding-top: 25px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.submit-button{
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px 30px;
  border-radius: 12px;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}
.cancel-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px; /* Reducido de 15px 30px */
  border-radius: 10px; /* Reducido de 12px */
  font-size: 0.95rem; /* Reducido de 1.05rem */
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #1A202C;
  color: #E0E0E0;
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.cancel-button:hover {
  background-color: #2D3748;
  transform: translateY(-2px);
}

.submit-button {
  background: linear-gradient(45deg, #4A90E2, #FF69B4);
  color: white;
  border: none;
  box-shadow: 0 4px 15px rgba(74, 144, 226, 0.4);
}

.submit-button:hover {
  background: linear-gradient(45deg, #FF69B4, #4A90E2);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.4);
}
.submit-button:disabled {
  background: #333; 
  color: #888;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.delete-confirm-button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px; /* Reducido de 15px 30px */
  border-radius: 10px; /* Reducido de 12px */
  font-size: 0.95rem; /* Reducido de 1.05rem */
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #FF0000;
  color: white;
  border: none;
  box-shadow: 0 4px 15px rgba(255, 0, 0, 0.4);
}

.delete-confirm-button:hover {
  background-color: #D60000;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(214, 0, 0, 0.4);
}

.delete-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.warning-section {
  margin-bottom: 35px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.warning-icon {
  color: #FFD700;
  margin-bottom: 5px;
}
.warning-icon svg {
  width: 55px; /* Reducido de 70px */
  height: 55px;
}

.delete-message {
  font-size: 1rem !important; /* Reducido de 1.1rem */
  font-weight: 500;
  color: #FFF;
  margin-bottom: px;
  text-shadow: 0 0 3px rgba(255, 255, 255, 0.2);
}
.local-preview {
  padding: 0px; /* Reducido de 25px */
  gap: 18px;
  margin-bottom: 10px;
}

.local-image {
  width: 70px; /* Reducido de 90px */
  height: 70px;
}
.local-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.local-details h4 {
  font-size: 1.2rem; /* Reducido de 1.5rem */
  margin: 0 0 8px 0;
}
.local-details p {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  gap: 10px;
  text-shadow: 0 0 1px rgba(255, 255, 255, 0.1);
}

.warning-text {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 5px;
  text-shadow: 0 0 1px rgba(255, 255, 255, 0.1);
}


.menu-popover-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 100;
  background: rgba(0, 0, 0, 0);
  pointer-events: auto;
}

.menu-popover {
  position: absolute;
  background: #1A1A2E;
  border-radius: 10px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
  min-width: 180px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.15);
  opacity: 0;
  transform: translateY(-10px);
  animation: fadeInSlide 0.2s ease-out forwards;
  padding: 10px 0;
  z-index: 101;
}

.popover-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #4A90E2;
  padding: 10px 20px;
  margin-bottom: 5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 12px 20px;
  background: transparent;
  color: #E0E0E0;
  border: none;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
  font-size: 1rem;
  font-weight: 500;
}

.menu-item:hover {
  background: rgba(74, 144, 226, 0.2);
}

.menu-item.delete:hover {
  background: rgba(255, 105, 180, 0.2);
  color: #FF6B6B;
}

/* --- Selectores (Dropdown) --- */
.select-container {
  position: relative;
  display: block;
  width: 100%;
}

.form-select {
  width: 100%;
  padding: 16px 20px 16px 20px; 
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  color: #F0F0F0;
  font-size: 1.05rem;
  appearance: none; 
  -webkit-appearance: none;
  -moz-appearance: none;
  transition: border-color 0.3s, box-shadow 0.3s;
  cursor: pointer;
  line-height: 1.5;
}

.form-select:focus {
  border-color: #4A90E2;
  box-shadow: 0 0 0 4px rgba(74, 144, 226, 0.3);
  outline: none;
  background: rgba(255, 255, 255, 0.12);
}

.select-arrow {
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  pointer-events: none; 
  color: #4A90E2;
}

.select-arrow svg {
  display: block;
  transition: transform 0.3s;
}

/* --- Notificaciones --- */
.notification-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-in-out;
}

.notification-card {
  background-color: #15151F;
  color: #4CAF50;
  border: 1px solid #4CAF50;
  border-radius: 8px;
  padding: 16px 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 12px;
  animation: slideInUp 0.3s ease-out;
}

.notification-text {
  font-size: 16px;
  font-weight: 500;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.notification-text svg {
  color: #4CAF50;
}

/* --- Animaciones --- */
@keyframes glitch {
  0% {
    text-shadow: 0.05em 0 0 rgba(74, 144, 226, 0.75), -0.05em -0.025em 0 rgba(255, 105, 180, 0.75), -0.025em 0.05em 0 rgba(255, 255, 255, 0.75);
  }
  14% {
    text-shadow: 0.05em 0 0 rgba(74, 144, 226, 0.75), -0.05em -0.025em 0 rgba(255, 105, 180, 0.75), -0.025em 0.05em 0 rgba(255, 255, 255, 0.75);
  }
  15% {
    text-shadow: -0.05em -0.025em 0 rgba(74, 144, 226, 0.75), -0.025em 0.05em 0 rgba(255, 105, 180, 0.75), 0.05em 0.05em 0 rgba(255, 255, 255, 0.75);
  }
  49% {
    text-shadow: -0.05em -0.025em 0 rgba(74, 144, 226, 0.75), -0.025em 0.05em 0 rgba(255, 105, 180, 0.75), 0.05em 0.05em 0 rgba(255, 255, 255, 0.75);
  }
  50% {
    text-shadow: 0.025em 0.05em 0 rgba(74, 144, 226, 0.75), 0.05em 0 0 rgba(255, 105, 180, 0.75), 0 -0.05em 0 rgba(255, 255, 255, 0.75);
  }
  99% {
    text-shadow: 0.025em 0.05em 0 rgba(74, 144, 226, 0.75), 0.05em 0 0 rgba(255, 105, 180, 0.75), 0 -0.05em 0 rgba(255, 255, 255, 0.75);
  }
  100% {
    text-shadow: 0.05em 0 0 rgba(74, 144, 226, 0.75), -0.05em -0.025em 0 rgba(255, 105, 180, 0.75), -0.025em 0.05em 0 rgba(255, 255, 255, 0.75);
  }
}

@keyframes glitch-line {
  0% {
    transform: translate(0, 0);
    opacity: 0.8;
  }
  20% {
    transform: translate(-2px, 2px);
    opacity: 0.5;
  }
  40% {
    transform: translate(3px, -1px);
    opacity: 0.7;
  }
  60% {
    transform: translate(-1px, 3px);
    opacity: 0.6;
  }
  80% {
    transform: translate(2px, -2px);
    opacity: 0.9;
  }
  100% {
    transform: translate(0, 0);
    opacity: 0.8;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideInUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

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

@keyframes fadeInSlide {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.spinner {
  animation: rotate 1s linear infinite;
  display: inline-block;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* --- Media Queries (Responsividad) --- */
@media (min-width: 769px) {

}


@media (max-width: 1024px) {
  .header-content,
  .footer-content,
  .content-wrapper {
    padding: 0 25px;
  }
  .logo h1 {
    font-size: 3rem;
  }
  .logo p {
    font-size: 1rem;
  }
  .section-title h2 {
    font-size: 2.5rem;
  }
  .section-title p {
    font-size: 1.1rem;
  }
  .bar-card {
    max-width: 350px;
  }
  .modal-content {
    padding: 40px;
  }
  .footer-logo h3 {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
    padding-bottom: 20px;
  }
  .header-actions {
    flex-direction: row;
    width: 100%;
    align-items: center;
    justify-content: center;
    gap: 15px;
  }
  .back-button,
  .add-button,
  .personal-button,
  .glow-select-button { /* Se aplica también a los nuevos botones */
    width: auto;
    flex: 1;
    justify-content: center;
    padding: 12px 20px;
    font-size: 1rem;
  }
  .logo {
    order: -1;
  }
  .logo h1 {
    font-size: 3.2rem;
  }
  .logo p {
    font-size: 0.9rem;
  }
  .main-content {
    padding: 40px 15px;
  }
  .section-title {
    margin-bottom: 40px;
  }
  .section-title h2 {
    font-size: 2rem;
  }
  .section-title p {
    font-size: 1rem;
  }
  .bars-grid {
    grid-template-columns: 1fr;
    gap: 25px;
  }
  .bar-card {
    max-width: 90%;
    margin: 0 auto;
  }
  .modal-content {
    padding: 30px;
    max-width: 95%;
  }
  .modal-header h2 {
    font-size: 1.8rem;
  }
  .form-actions {
    flex-direction: column;
    gap: 10px;
  }
  .form-actions button {
    width: 100%;
    justify-content: center;
  }
  .footer-content {
    flex-direction: column;
    gap: 20px;
  }
  .footer-info {
    text-align: center;
  }
  .footer-logo h3 {
    font-size: 1.8rem;
  }
  .card-actions {
    flex-direction: column;
    gap: 10px;
  }
  .enter-button {
    width: 100%;
    justify-content: center;
  }
  .options-menu {
    width: 100%;
    display: flex;
    justify-content: center;
    margin-left: 0;
  }
  .menu-popover {
    left: 50% !important;
    transform: translateX(-50%) translateY(0);
  }
}

@media (max-width: 480px) {
  .header-content,
  .footer-content {
    padding: 0 15px;
  }
  .header-actions {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 10px;
  }
  .back-button,
  .add-button,
  .personal-button {
    width: calc(50% - 5px);
  }
  .logo h1 {
    font-size: 2.5rem;
  }
  .logo p {
    font-size: 0.8rem;
  }
  .modal-content {
    padding: 25px;
  }
  .modal-header h2 {
    font-size: 1.6rem;
  }
  .bar-card {
    border-radius: 15px;
  }
  .bar-info {
    padding: 20px;
  }
  .bar-name {
    font-size: 1.4rem;
  }
  .local-preview {
    flex-direction: column;
    text-align: center;
  }
  .local-image {
    margin-bottom: 15px;
  }
  .image-upload-area {
    padding: 20px;
    min-height: 150px;
  }
  .image-upload-area svg {
    width: 40px;
    height: 40px;
  }
  .image-upload-area p {
    font-size: 1rem;
  }
}
/* --- Selector de Tipo de Local (Botones Pills) --- */
.tipo-local-selector {
  display: flex;
  gap: 15px;
  width: 100%;
  margin-top: 12px;
}

.tipo-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.08);
  border: 2px solid rgba(255, 255, 255, 0.15);
  border-radius: 50px; /* Forma de "bolita" o "pill" */
  color: #B0B0B0;
  font-size: 1.05rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;
}

.tipo-button:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(74, 144, 226, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.tipo-button.active {
  background: linear-gradient(90deg, #4A90E2, #FF69B4);
  color: #FFFFFF;
  border-color: #FF69B4;
  font-weight: 700;
  
  /* Efecto de brillo luminoso */
  box-shadow: 
    0 0 8px rgba(74, 144, 226, 0.8),
    0 0 16px rgba(74, 144, 226, 0.5),
    0 0 24px rgba(255, 105, 180, 0.8),
    0 0 32px rgba(255, 105, 180, 0.3),
    inset 0 0 10px rgba(255, 255, 255, 0.4);
  
  transform: scale(1.05);
  text-shadow: 0 0 4px #000000;
}

.tipo-button.active svg {
  filter: drop-shadow(0 0 3px rgba(255, 255, 255, 0.8));
}

.tipo-button svg {
  transition: all 0.3s ease;
}

/* Responsividad para móviles */
@media (max-width: 480px) {
  .tipo-local-selector {
    flex-direction: column;
    gap: 10px;
  }
  
  .tipo-button {
    width: 100%;
  }
}
/* --- Estilos Personalizados para SweetAlert2 --- */
:deep(.swal-custom-popup) {
  border-radius: 20px !important;
  border: 1px solid rgba(74, 144, 226, 0.3) !important;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6) !important;
}

:deep(.swal-custom-title) {
  font-size: 1.4rem !important;
  font-weight: 700 !important;
  color: #FFFFFF !important;
  margin-bottom: 15px !important;
}

:deep(.swal-custom-confirm) {
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  padding: 10px 20px !important;
  border-radius: 10px !important;
}

:deep(.swal-custom-cancel) {
  font-size: 0.9rem !important;
  font-weight: 600 !important;
  padding: 10px 20px !important;
  border-radius: 10px !important;
}

:deep(.swal2-html-container) {
  font-size: 0.95rem !important;
  line-height: 1.6 !important;
}

:deep(.swal2-validation-message) {
  background: rgba(255, 0, 0, 0.1) !important;
  color: #FF6B6B !important;
  border: 1px solid rgba(255, 0, 0, 0.3) !important;
}
/* Barra de información de límites */
.limit-info-bar {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px 40px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.limit-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 20px;
}

.limit-text {
  font-size: 0.95rem;
  color: #E0E0E0;
  font-weight: 600;
  white-space: nowrap;
}

.limit-progress {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  overflow: hidden;
  max-width: 300px;
}

.limit-progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4A90E2, #FF69B4);
  transition: width 0.3s ease;
  border-radius: 10px;
}

.limit-progress-fill.limit-reached {
  background: linear-gradient(90deg, #FF6B6B, #FF0000);
}

.limit-warning {
  font-size: 0.9rem;
  color: #FFD700;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 5px;
}

@media (max-width: 768px) {
  .limit-content {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
  
  .limit-progress {
    max-width: 100%;
    width: 100%;
  }
}
:deep(.swal2-html-container a) {
  color: #4A90E2 !important;
  text-decoration: none !important;
  font-weight: 700 !important;
  transition: color 0.3s ease !important;
}

:deep(.swal2-html-container a:hover) {
  color: #FF69B4 !important;
  text-decoration: underline !important;
}
.add-button.button-disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.add-button.button-disabled:hover {
  background-color: #4A90E2;
  transform: none;
  box-shadow: 0 4px 10px rgba(74, 144, 226, 0.5);
}
.add-first-bar-button.button-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: #555;
}

.add-first-bar-button.button-disabled:hover {
  background-color: #555;
  transform: none;
}
</style>