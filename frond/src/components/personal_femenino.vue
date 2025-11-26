<template>
  <div class="app">
    <header class="header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-placeholder"></div>
          <h1 class="app-title">CONTROL<span class="glitch" data-text="KA"> AS</span></h1>
        </div>
        <button class="back-btn" @click="goBack">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m12 19-7-7 7-7" /><path d="M19 12H5" />
          </svg> Volver
        </button>
      </div>
    </header>

    <main class="main-content">
      <div class="container">
        <div class="top-section">
          <h2 class="section-title">Gestión de Personal Femenino</h2>
          <button class="add-btn" @click="openModal">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 5v14" /><path d="M5 12h14" />
            </svg> Agregar Personal
          </button>
        </div>

        <div class="filter-section">
          <div class="search-input-group">
            <label for="searchQuery">Buscar:</label>
            <input type="text" id="searchQuery" v-model="searchQuery.general" placeholder="Buscar por nombre o documento..." @input="filterGeneralQuery" />
          </div>
          <div class="search-input-group">
            <label for="searchAddedBy">Agregado por:</label>
            <select id="searchAddedBy" v-model="searchQuery.agregadoPor">
              <option value="">Todos</option>
              <option v-for="(name, id) in addedByNames" :key="id" :value="id">{{ name }}</option>
            </select>
          </div>
        </div>

        <div v-if="isLoading" class="loading-state"><p>Cargando personas...</p></div>

        <div class="cards-grid" v-else-if="filteredMujeres.length > 0">
          <div v-for="person in filteredMujeres" :key="person.id" class="person-card">
            <div class="card-image-wrapper">
              <img v-if="person.foto" :src="person.foto" :alt="person.nombre" class="card-image" />
              <div v-else class="placeholder-image">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M19.64 12.55V7.95c0-1.89-1.2-2.74-2.88-1.85L12.5 9.47c-1.2.66-1.2 1.76 0 2.41l4.26 2.33c1.68.89 2.88.04 2.88-1.85Z" />
                  <path d="M6 17a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
                  <path d="M11 19c-3.87 0-7-3.13-7-7s3.13-7 7-7" />
                  <path d="M17 21c-3.87 0-7-3.13-7-7s3.13-7 7-7" />
                </svg>
              </div>
            </div>
            <div class="card-content">
              <h3 class="person-name">{{ person.nombre }}</h3>
              <div class="person-info">
                <p><strong>Documento:</strong> {{ person.documento || 'N/A' }}</p>
                <p><strong>Teléfono:</strong> {{ person.telefono || 'N/A' }}</p>
                <p>
                  <strong>Examen médico:</strong>
                  <span :class="{ 'examen-vencido': isExamenVencido(person.fecha_examen) }">
                    {{ person.fecha_examen ? formatDate(person.fecha_examen) : 'Sin registrar' }}
                    <span v-if="isExamenVencido(person.fecha_examen)" class="vencido-text"> (VENCIDO)</span>
                  </span>
                </p>
                <p><strong>Agregado por:</strong> {{ addedByNames[person.agregado_por] || 'Cargando...' }}</p>
                <p><strong>Agregado:</strong> {{ formatDate(person.fecha_agregado) }}</p>
              </div>
              <div class="card-actions">
                <button class="edit-btn" @click="editPerson(person)">Editar</button>
                <button class="examen-btn" @click="openExamenModal(person)">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                  </svg>
                  Exámenes
                </button>
                <button class="delete-btn" @click="confirmDelete(person)">Eliminar</button>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
          </svg>
          <h3>No hay personas agregadas</h3>
          <p>Comienza agregando tu primera persona o ajusta los filtros de búsqueda.</p>
        </div>
      </div>
    </main>

    <!-- MODAL AGREGAR / EDITAR -->
    <Teleport to="body">
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>{{ isEditing ? 'Editar' : 'Agregar' }} Personal</h3>
            <button class="close-btn" @click="closeModal">✕</button>
          </div>
          <form @submit.prevent="savePerson" class="modal-form">

            <!-- FOTO DE PERFIL -->
            <div class="form-group">
              <label>Foto de Perfil *</label>
              <input type="file" id="file-input" @change="handleFileUpload" accept="image/*" style="display: none;" />
              <label for="file-input" class="custom-file-upload">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 14.89V20a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5.11" />
                  <path d="M12 2v14" /><path d="m7 9 5-5 5 5" />
                </svg>
                <span>{{ fileName || 'Seleccionar foto' }}</span>
              </label>
              <div class="photo-preview" :class="{ 'has-image': currentPerson.foto }">
                <img v-if="currentPerson.foto" :src="currentPerson.foto" alt="Preview" class="photo-preview-image" />
                <template v-else>
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M15 8v1.17c0 .54.26 1.05.7 1.35l4.31 3c.87.6 1.09 1.15.65 2.13-.53 1.15-2.07 1.4-3.12.63l-4.73-3.46a2.02 2.02 0 0 0-2.31 0L5.46 16.82c-1.05.77-2.59.52-3.12-.63-.44-.98-.22-1.53.65-2.13l4.31-3c.44-.3.7-.81.7-1.35V8" />
                    <circle cx="12" cy="5" r="2" />
                  </svg>
                  <p>Sin foto</p>
                </template>
              </div>
            </div>

            <div class="form-group">
              <label>Nombre *</label>
              <input type="text" v-model="currentPerson.nombre" required placeholder="Nombre completo" />
            </div>

            <div class="form-group" v-if="!isEditing">
              <label>Fecha de agregado</label>
              <input type="text" :value="currentDate" readonly class="readonly-input" />
            </div>

            <div class="form-group">
              <label>Documento *</label>
              <input type="text" v-model="currentPerson.documento" required placeholder="Solo números" @input="filterDocumento" />
            </div>

            <div class="form-group">
              <label>Teléfono</label>
              <input type="tel" v-model="currentPerson.telefono" placeholder="Opcional" />
            </div>

            <div class="form-group">
              <label>Agregado por</label>
              <input type="text" :value="modalAddedByName" readonly class="readonly-input" />
            </div>

            <!-- SOLO AL CREAR: Fecha y foto del examen -->
            <div class="form-group" v-if="!isEditing">
              <label>Fecha del Examen Médico *</label>
              <input type="date" v-model="currentPerson.fecha_examen" required />
            </div>

            <div class="form-group" v-if="!isEditing">
              <label>Subir Foto del Examen Médico (PDF o imagen) *</label>
              <input type="file" ref="fileInputExamen" @change="handleExamenUpload" accept="image/*,application/pdf" style="display: none" />
              <label class="custom-file-upload" @click="$refs.fileInputExamen?.click()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 14.89V20a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5.11" />
                  <path d="M12 2v14" /><path d="m7 9 5-5 5 5" />
                </svg>
                <span>{{ examenFileName || 'Seleccionar archivo' }}</span>
              </label>
              <div class="photo-preview" :class="{ 'has-image': currentPerson.foto_examen }">
                <img v-if="isImageExamen" :src="currentPerson.foto_examen" alt="Examen" class="photo-preview-image" />
                <div v-else-if="currentPerson.foto_examen" class="pdf-preview">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e91e63" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                  </svg>
                  <span>PDF Cargado</span>
                </div>
                <template v-else>
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                  </svg>
                  <p>Sin examen médico</p>
                </template>
              </div>
            </div>

            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="closeModal">Cancelar</button>
              <button type="submit" class="submit-btn" :disabled="isLoading">
                {{ isLoading ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Agregar') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- MODAL DE EXÁMENES -->
    <Teleport to="body">
      <div v-if="showExamenModal" class="modal-overlay" @click="closeExamenModal">
        <div class="modal examen-modal" @click.stop>
          <div class="modal-header examen-modal-header">
            <div class="header-icon-title">
              <div class="icon-circle">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                </svg>
              </div>
              <h3>Examen Médico</h3>
            </div>
            <button class="close-btn" @click="closeExamenModal">✕</button>
          </div>
          <div class="examen-content" v-if="selectedPerson">
            <div class="examen-header">
              <img :src="selectedPerson.foto" alt="Foto" class="examen-profile-img" />
              <div class="examen-info">
                <h2>{{ selectedPerson.nombre }}</h2>
                <p><strong>Documento:</strong> {{ selectedPerson.documento }}</p>
                <p class="fecha-examen-line">
                  <strong>Fecha examen actual:</strong>
                  <span :class="{ 'examen-vencido': isExamenVencido(selectedPerson.fecha_examen) }">
                    {{ selectedPerson.fecha_examen ? formatDate(selectedPerson.fecha_examen) : 'No registrado' }}
                    <span v-if="isExamenVencido(selectedPerson.fecha_examen)" class="vencido-badge">VENCIDO</span>
                  </span>
                </p>
              </div>
            </div>

            <div class="examen-document">
              <h4>Documento del examen médico actual</h4>
              <div class="document-preview">
                <img v-if="selectedPerson.foto_examen && selectedPerson.foto_examen.startsWith('data:image')"
                     :src="selectedPerson.foto_examen" alt="Examen" />
                <iframe v-else-if="selectedPerson.foto_examen"
                        :src="selectedPerson.foto_examen"
                        class="pdf-iframe" frameborder="0"></iframe>
                <div v-else class="no-document">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                  </svg>
                  <p>No hay documento cargado</p>
                </div>
              </div>
            </div>

            <div class="update-section">
              <h4>Actualizar examen médico</h4>
              <button class="update-examen-btn" @click="$refs.fileExamenUpdate?.click()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                Seleccionar nuevo examen
              </button>
              <input type="file" ref="fileExamenUpdate" @change="handleNewExamen" accept="image/*,application/pdf" style="display:none" />
              
              <div v-if="newExamenFileName" class="new-examen-preview">
                <p class="file-selected">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  {{ newExamenFileName }}
                </p>
                <div class="preview-box" v-if="newExamenFile">
                  <img v-if="newExamenFile.startsWith('data:image')" :src="newExamenFile" alt="Preview nuevo examen" class="preview-image" />
                  <div v-else class="pdf-preview-new">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ffa500" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                    <span>PDF Seleccionado</span>
                  </div>
                </div>
                <button class="submit-update-btn" @click="updateExamen" :disabled="isUpdatingExamen">
                  <svg v-if="!isUpdatingExamen" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                  <div v-else class="spinner"></div>
                  {{ isUpdatingExamen ? 'Guardando...' : 'Guardar nuevo examen' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- MODAL CONFIRMAR ELIMINAR -->
    <Teleport to="body">
      <div v-if="showDeleteConfirm" class="modal-overlay" @click="closeDeleteConfirm">
        <div class="confirm-modal" @click.stop>
          <div class="confirm-content">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#e91e63" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <path d="M9 9l6 6" /><path d="M15 9l-6 6" />
            </svg>
            <h3>¿Estás seguro?</h3>
            <p>Esta acción eliminará permanentemente a <strong>{{ personToDelete?.nombre }}</strong></p>
            <div class="confirm-actions">
              <button class="cancel-btn" @click="closeDeleteConfirm">Cancelar</button>
              <button class="confirm-delete-btn" @click="deletePerson" :disabled="isLoading">
                {{ isLoading ? 'Eliminando...' : 'Eliminar' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2025 Control AS App. Todos los derechos reservados.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import Swal from 'sweetalert2';
import { API_BASE_URL } from '../config/api';

export default {
  name: 'GestionMujeres',
  setup() {
    const userStore = useUserStore();
    const duenoId = computed(() => userStore.id);

    const mujeres = ref([]);
    const addedByNames = ref({});
    const showModal = ref(false);
    const showDeleteConfirm = ref(false);
    const isEditing = ref(false);
    const personToDelete = ref(null);
    const editingId = ref(null);
    const isLoading = ref(false);
    const fileName = ref('');
    const examenFileName = ref('');

    // Modal exámenes
    const showExamenModal = ref(false);
    const selectedPerson = ref(null);
    const newExamenFile = ref(null);
    const newExamenFileName = ref('');
    const isUpdatingExamen = ref(false);

    const searchQuery = ref({ general: '', agregadoPor: '' });

    const currentPerson = ref({
      nombre: '', documento: null, telefono: null, foto: null,
      fecha_examen: '', foto_examen: null,
      agregado_por: duenoId.value, dueno_id: duenoId.value
    });

    const currentDate = computed(() => new Date().toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' }));
    const isImageExamen = computed(() => currentPerson.value.foto_examen?.startsWith('data:image'));

    const isExamenVencido = (fecha) => {
      if (!fecha) return false;
      const fechaExamen = new Date(fecha);
      const hoy = new Date();
      const diffMonths = (hoy.getFullYear() - fechaExamen.getFullYear()) * 12 + (hoy.getMonth() - fechaExamen.getMonth());
      return diffMonths > 6 || (diffMonths === 6 && hoy.getDate() > fechaExamen.getDate());
    };

    const filteredMujeres = computed(() => {
      const q = searchQuery.value.general.toLowerCase().trim();
      const por = searchQuery.value.agregadoPor;
      return mujeres.value.filter(p => {
        const nombre = p.nombre.toLowerCase();
        const doc = p.documento?.toString().toLowerCase() || '';
        const matchesSearch = !q || nombre.includes(q) || doc.includes(q);
        const matchesAddedBy = !por || p.agregado_por == por;
        return matchesSearch && matchesAddedBy;
      });
    });

    const modalAddedByName = computed(() => addedByNames.value[currentPerson.value.agregado_por] || 'Cargando...');

    const fetchUserName = async (id) => {
      if (!id || addedByNames.value[id]) return addedByNames.value[id] || 'Desconocido';
      try {
        const res = await axios.get(`${API_BASE_URL}/buscar_usuario/${id}`);
        const name = res.data.nombre || `ID: ${id}`;
        addedByNames.value[id] = name;
        return name;
      } catch (err) {
        addedByNames.value[id] = `ID: ${id}`;
        return addedByNames.value[id];
      }
    };

    const fetchMujeres = async () => {
      if (!duenoId.value) return;
      isLoading.value = true;
      try {
        const res = await axios.get(`${API_BASE_URL}/mujeres/dueno/${duenoId.value}`);
        mujeres.value = res.data;
        const ids = new Set([duenoId.value, ...mujeres.value.map(m => m.agregado_por)]);
        await Promise.all(Array.from(ids).map(fetchUserName));
      } catch (err) {
        console.error(err);
        mujeres.value = [];
      } finally {
        isLoading.value = false;
      }
    };

    onMounted(() => {
      fetchUserName(duenoId.value);
      fetchMujeres();
    });

    watch(duenoId, () => { fetchUserName(duenoId.value); fetchMujeres(); }, { immediate: true });

    const formatDate = (d) => d ? new Date(d).toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' }) : '';

    const openModal = () => { isEditing.value = false; resetForm(); showModal.value = true; };
    const closeModal = () => { showModal.value = false; resetForm(); };

    const resetForm = () => {
      currentPerson.value = {
        nombre: '', documento: null, telefono: null, foto: null,
        fecha_examen: '', foto_examen: null,
        agregado_por: duenoId.value, dueno_id: duenoId.value
      };
      fileName.value = '';
      examenFileName.value = '';
      editingId.value = null;
    };

    const handleFileUpload = (e) => {
      const file = e.target.files[0];
      if (file) {
        fileName.value = file.name;
        const reader = new FileReader();
        reader.onload = (ev) => currentPerson.value.foto = ev.target.result;
        reader.readAsDataURL(file);
      }
    };

    const handleExamenUpload = (e) => {
      const file = e.target.files[0];
      if (file) {
        examenFileName.value = file.name;
        const reader = new FileReader();
        reader.onload = (ev) => currentPerson.value.foto_examen = ev.target.result;
        reader.readAsDataURL(file);
      }
    };

    const filterDocumento = (e) => {
      const v = e.target.value.replace(/\D/g, '');
      currentPerson.value.documento = v;
      e.target.value = v;
    };

    const filterGeneralQuery = () => {};

    const savePerson = async () => {
      if (!currentPerson.value.nombre?.trim()) return Swal.fire('Error', 'El nombre es obligatorio', 'error');
      if (!currentPerson.value.documento?.toString().trim()) return Swal.fire('Error', 'El documento es obligatorio', 'error');
      if (!currentPerson.value.foto) return Swal.fire('Error', 'La foto de perfil es obligatoria', 'error');
      if (!isEditing.value) {
        if (!currentPerson.value.fecha_examen) return Swal.fire('Error', 'La fecha del examen médico es obligatoria', 'error');
        if (!currentPerson.value.foto_examen) return Swal.fire('Error', 'Debes subir el examen médico', 'error');
      }

      isLoading.value = true;
      try {
        const payload = {
          nombre: currentPerson.value.nombre.trim(),
          documento: currentPerson.value.documento.toString().trim(),
          telefono: currentPerson.value.telefono || null,
          foto: currentPerson.value.foto,
          fecha_examen: currentPerson.value.fecha_examen || null,
          foto_examen: currentPerson.value.foto_examen || null,
        };

        if (isEditing.value) {
          await axios.put(`${API_BASE_URL}/mujeres/${editingId.value}`, payload);
          Swal.fire('¡Actualizada!', 'Cambios guardados', 'success');
        } else {
          payload.agregado_por = duenoId.value;
          payload.dueno_id = duenoId.value;
          await axios.post(`${API_BASE_URL}/mujeres`, payload);
          Swal.fire('¡Agregada!', 'Personal agregado con éxito', 'success');
        }
        await fetchMujeres();
        closeModal();
      } catch (err) {
        Swal.fire('Error', err.response?.data?.detail || 'Error al guardar', 'error');
      } finally {
        isLoading.value = false;
      }
    };

    const editPerson = (person) => {
      isEditing.value = true;
      editingId.value = person.id;
      currentPerson.value = { ...person, documento: person.documento ? String(person.documento) : null };
      fileName.value = person.foto ? 'Foto cargada' : '';
      examenFileName.value = person.foto_examen ? 'Examen cargado' : '';
      showModal.value = true;
    };

    const confirmDelete = (p) => { personToDelete.value = p; showDeleteConfirm.value = true; };
    const closeDeleteConfirm = () => { showDeleteConfirm.value = false; personToDelete.value = null; };

    const deletePerson = async () => {
      isLoading.value = true;
      try {
        await axios.delete(`${API_BASE_URL}/mujeres_eliminar/${personToDelete.value.id}`);
        await fetchMujeres();
        closeDeleteConfirm();
        Swal.fire('Eliminada', 'Persona eliminada correctamente', 'success');
      } catch (err) {
        Swal.fire('Error', 'No se pudo eliminar', 'error');
      } finally {
        isLoading.value = false;
      }
    };

    const openExamenModal = (person) => {
      selectedPerson.value = { ...person };
      newExamenFile.value = null;
      newExamenFileName.value = '';
      showExamenModal.value = true;
    };

    const closeExamenModal = () => {
      showExamenModal.value = false;
      selectedPerson.value = null;
      newExamenFile.value = null;
      newExamenFileName.value = '';
    };

    const handleNewExamen = (e) => {
      const file = e.target.files[0];
      if (file) {
        newExamenFileName.value = file.name;
        const reader = new FileReader();
        reader.onload = (ev) => newExamenFile.value = ev.target.result;
        reader.readAsDataURL(file);
      }
    };

    const updateExamen = async () => {
      if (!newExamenFile.value || !selectedPerson.value) return;
      isUpdatingExamen.value = true;
      try {
        const payload = {
          foto_examen: newExamenFile.value,
          fecha_examen: new Date().toISOString().split('T')[0]
        };
        await axios.put(`${API_BASE_URL}/mujeres/${selectedPerson.value.id}`, payload);
        await fetchMujeres();
        const updated = mujeres.value.find(p => p.id === selectedPerson.value.id);
        if (updated) {
          selectedPerson.value = { ...updated };
        }
        newExamenFile.value = null;
        newExamenFileName.value = '';
        Swal.fire('¡Actualizado!', 'Examen médico renovado correctamente', 'success');
      } catch (err) {
        console.error(err);
        Swal.fire('Error', 'No se pudo actualizar el examen', 'error');
      } finally {
        isUpdatingExamen.value = false;
      }
    };

    const goBack = () => window.history.back();

    return {
      mujeres, addedByNames, showModal, showDeleteConfirm, isEditing, currentPerson, personToDelete,
      currentDate, isLoading, fileName, examenFileName, searchQuery, filteredMujeres, modalAddedByName,
      isImageExamen, formatDate, openModal, closeModal, handleFileUpload, handleExamenUpload,
      filterDocumento, filterGeneralQuery, savePerson, editPerson, confirmDelete, deletePerson,
      closeDeleteConfirm, goBack, isExamenVencido, showExamenModal, selectedPerson,
      newExamenFileName, isUpdatingExamen, openExamenModal, closeExamenModal,
      handleNewExamen, updateExamen, newExamenFile
    };
  }
};
</script>

<style scoped>
/* Estilos Base Mejorados para ambiente de bar */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  min-height: 100vh;
  background: radial-gradient(
      circle at 50% 10%,
      rgba(52, 152, 219, 0.1) 0%,
      transparent 50%
    ),
    linear-gradient(135deg, #0f0f0f 0%, #202020 100%);
  color: #f0f0f0;
  font-family: 'Poppins', sans-serif;
  display: flex;
  flex-direction: column;
}

/* Header */
.header {
  background: rgba(15, 15, 15, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1.5rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo-placeholder {
  width: 45px;
  height: 45px;
  background: linear-gradient(45deg, #3498db, #e91e63);
  border-radius: 50%;
  box-shadow: 0 0 10px #3498db, 0 0 20px #3498db;
}

.app-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2.5rem;
  font-weight: normal;
  color: #f0f0f0;
  text-shadow: 0 0 10px #3498db, 0 0 20px #3498db;
}

/* Back button */
.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  color: #3498db;
  border: 1px solid rgba(52, 152, 219, 0.3);
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(-5px) scale(1.05);
  box-shadow: 0 0 10px #3498db, 0 0 20px #3498db;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 3rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.top-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
}

.section-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 2rem;
  color: #f0f0f0;
  text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(45deg, #3498db, #e91e63);
  color: #f0f0f0;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 8px 30px rgba(52, 152, 219, 0.4);
}

/* Sección de búsqueda y filtros */
.filter-section {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.search-input-group {
  flex: 1;
  min-width: 200px;
}

.search-input-group label {
  display: block;
  font-size: 0.85rem;
  color: #3498db;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.search-input-group input,
.search-input-group select {
  width: 100%;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #f0f0f0;
  font-size: 0.95rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search-input-group input:focus,
 Fondo.search-input-group select:focus {
  outline: none;
  border-color: #e91e63;
  box-shadow: 0 0 8px rgba(233, 30, 99, 0.5);
}

.search-input-group select {
  cursor: pointer;
  -webkit-appearance: none;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1em;
}

.search-input-group select option {
  background: #2c2c2c;
  color: #f0f0f0;
}

/* Cards Grid */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.person-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  overflow: hidden;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
}

.person-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 15px;
  background: linear-gradient(45deg, rgba(52, 152, 219, 0.3), rgba(233, 30, 99, 0.3));
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.person-card:hover::before { opacity: 1; }
.person-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}

.card-image-wrapper {
  position: relative;
  height: 200px;
  overflow: hidden;
  border-radius: 10px;
  border: 2px solid #333;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
}

.card-image-wrapper::before {
  content: '';
  position: absolute;
  top: -2px; left: -2px; right: -2px; bottom: -2px;
  background: linear-gradient(45deg, #3498db, #e91e63);
  border-radius: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: -1;
}

.person-card:hover .card-image-wrapper::before { opacity: 1; }

.placeholder-image {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.placeholder-image svg {
  width: 48px;
  height: 48px;
  margin-bottom: 0.5rem;
  color: #666;
  opacity: 0.5;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
  transition: transform 0.5s ease;
}

.card-image-wrapper:hover .card-image { transform: scale(1.05); }

.card-content {
  padding: 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.person-name {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.6rem;
  margin-bottom: 0.8rem;
  color: #e91e63;
  text-shadow: 0 0 10px #e91e63, 0 0 20px #e91e63;
}

.person-info {
  margin-bottom: 1.2rem;
  font-size: 0.9rem;
  line-height: 1.5;
  flex: 1;
}

.person-info p {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.4rem;
}

.person-info strong { color: #3498db; }

.card-actions {
  display: flex;
  gap: 0.8rem;
  margin-top: auto;
  flex-wrap: wrap;
}

.edit-btn, .delete-btn, .examen-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  border: 1px solid;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 100px;
}

.edit-btn {
  background: rgba(52, 152, 219, 0.1);
  color: #3498db;
  border-color: rgba(52, 152, 219, 0.3);
}

.edit-btn:hover {
  background: rgba(52, 152, 219, 0.2);
  box-shadow: 0 0 10px rgba(52, 152, 219, 0.5);
  transform: translateY(-2px);
}

.examen-btn {
  background: linear-gradient(135deg, rgba(255, 165, 0, 0.15), rgba(255, 140, 0, 0.1));
  color: #ffa500;
  border-color: rgba(255, 165, 0, 0.4);
  position: relative;
  overflow: hidden;
}

.examen-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 165, 0, 0.3), transparent);
  transition: left 0.5s ease;
}

.examen-btn:hover::before { left: 100%; }

.examen-btn:hover {
  background: linear-gradient(135deg, rgba(255, 165, 0, 0.25), rgba(255, 140, 0, 0.2));
  box-shadow: 0 0 15px rgba(255, 165, 0, 0.6);
  transform: translateY(-2px);
}

.delete-btn {
  background: rgba(233, 30, 99, 0.1);
  color: #e91e63;
  border-color: rgba(233, 30, 99, 0.3);
}

.delete-btn:hover {
  background: rgba(233, 30, 99, 0.2);
  box-shadow: 0 0 10px rgba(233, 30, 99, 0.5);
  transform: translateY(-2px);
}

.examen-vencido { color: #e74c3c !important; }
.vencido-text { color: #e74c3c; font-weight: bold; }
.vencido-badge {
  display: inline-block;
  background: linear-gradient(45deg, #e74c3c, #c0392b);
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: bold;
  margin-left: 0.5rem;
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.4);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 5rem 2rem;
  color: rgba(255, 255, 255, 0.6);
}

.empty-state svg {
  margin-bottom: 1.5rem;
  color: rgba(255, 255, 255, 0.6);
  opacity: 0.3;
}

.empty-state h3 {
  margin-bottom: 0.5rem;
  color: #f0f0f0;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.5rem;
}

/* Modal Overlay & Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal {
  background: linear-gradient(135deg, #0f0f0f, #202020);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  width: 90%;
  max-width: 550px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  margin: 20px;
  animation: fadeInScale 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 10px 50px rgba(0, 0, 0, 0.5);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInScale {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h3 {
  color: #e91e63;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.8rem;
  text-shadow: 0 0 10px #e91e63, 0 0 20px #e91e63;
}

.close-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  font-size: 1.5rem;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #f0f0f0;
  transform: rotate(90deg);
}

.modal-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.8rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.6rem;
  color: #3498db;
  font-weight: 600;
  font-size: 1rem;
  text-transform: uppercase;
}

.form-group input {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: #f0f0f0;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.5);
}

.readonly-input {
  background: rgba(255, 255, 255, 0.02) !important;
  color: rgba(255, 255, 255, 0.6) !important;
  cursor: not-allowed;
}

.custom-file-upload {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.8rem 1.5rem;
  background: linear-gradient(90deg, #3498db, #e91e63);
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  width: 100%;
  text-align: left;
}

.custom-file-upload:hover {
  background: linear-gradient(90deg, #3498db, #c0392b);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.photo-preview {
  margin-top: 1rem;
  border: 2px046 dashed #666;
  border-radius: 10px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 120px;
  background: rgba(0, 0, 0, 0.1);
  color: #888;
  font-size: 1.2rem;
  position: relative;
  overflow: hidden;
  text-align: center;
}

.photo-preview.has-image {
  border: 2px solid #e91e63;
}

.photo-preview::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg width='56' height='56' viewBox='0 0 56 56' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cpath d='m0 0h56v56h-56z'/%3E%3Cpath d='m14 14 21 21-8 8-5-5-8-8 21-21' stroke='%23666' stroke-width='2'/%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.15;
  border-radius: 10px;
  pointer-events: none;
}

.photo-preview.has-image::before { content: none; }

.photo-preview-image {
  width: 100%;
  height: auto;
  max-height: 150px;
  object-fit: contain;
  border-radius: 6px;
}

.photo-preview p {
  color: #888;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.pdf-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #e91e63;
  font-weight: 600;
  background: rgba(233, 30, 99, 0.1);
  border-radius: 10px;
  height: 100%;
  padding: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.cancel-btn, .submit-btn {
  padding: 0.9rem 2rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #f0f0f0;
}

.cancel-btn:hover { background: rgba(255, 255, 255, 0.2); }

.submit-btn {
  background: linear-gradient(45deg, #3498db, #e91e63);
  color: #f0f0f0;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(52, 152, 219, 0.4);
}

/* Modal de exámenes */
.examen-modal {
  max-width: 900px;
  width: 95%;
}

.examen-modal-header {
  background: linear-gradient(135deg, rgba(255, 165, 0, 0.1), rgba(255, 140, 0, 0.05));
  border-bottom: 2px solid rgba(255, 165, 0, 0.3);
}

.header-icon-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.icon-circle {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #ffa500, #ff8c00);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 20px rgba(255, 165, 0, 0.5);
  animation: rotate 10s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.icon-circle svg {
  color: white;
  filter: drop-shadow(0 0 3px rgba(255, 255, 255, 0.8));
}

.examen-modal-header h3 {
  color: #ffa500;
  text-shadow: 0 0 10px #ffa500, 0 0 20px #ffa500;
}

.examen-content { padding: 2rem; }

.examen-header {
  display: flex;
  gap: 1.5rem;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid rgba(255, 165, 0, 0.2);
  background: linear-gradient(135deg, rgba(255, 165, 0, 0.05), transparent);
  border-radius: 10px;
}

.examen-profile-img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  border: 3px solid #ffa500;
  box-shadow: 0 0 20px rgba(255, 165, 0, 0.5);
}

.examen-info h2 {
  color: #ffa500;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  text-shadow: 0 0 10px rgba(255, 165, 0, 0.5);
}

.examen-info p {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.3rem;
}

.examen-document h4 {
  margin-bottom: 1rem;
  color: #3498db;
  font-size: 1.2rem;
  font-weight: 600;
}

.document-preview {
  max-height: 600px;
  overflow: auto;
  border: 2px dashed rgba(255, 165, 0, 0.3);
  border-radius: 10px;
  background: rgba(0, 0, 0, 0.3);
}

.document-preview img, .pdf-iframe {
  width: 100%;
  height: auto;
  max-height: 600px;
  object-fit: contain;
}

.pdf-iframe {
  height: 600px;
  border: none;
}

.no-document {
  padding: 3rem;
  text-align: center;
  color: #888;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.update-section {
  margin-top: 2rem;
  text-align: center;
  background: linear-gradient(135deg, rgba(255, 165, 0, 0.05), transparent);
  padding: 2rem;
  border-radius: 10px;
  border: 1px solid rgba(255, 165, 0, 0.2);
}

.update-section h4 {
  color: #ffa500;
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.update-examen-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: linear-gradient(135deg, #ffa500, #ff8c00);
  padding: 1rem 2.5rem;
  border: none;
  border-radius: 10px;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 165, 0, 0.3);
}

.update-examen-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(255, 165, 0, 0.5);
  background: linear-gradient(135deg, #ff8c00, #ff7700);
}

.new-examen-preview { margin-top: 1.5rem; animation: slideDown 0.3s ease; }

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.file-selected {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin: 1rem 0;
  color: #27ae60;
  font-weight: bold;
  font-size: 1rem;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.preview-box {
  margin: 1rem auto;
  max-width: 400px;
  border: 2px solid rgba(255, 165, 0, 0.4);
  border-radius: 10px;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
}

.preview-image {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: contain;
  border-radius: 8px;
}

.pdf-preview-new {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 2rem;
  color: #ffa500;
  font-weight: 600;
}

.submit-update-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  background: linear-gradient(135deg, #27ae60, #229954);
  padding: 1rem 2.5rem;
  border: none;
  border-radius: 10px;
  color: white;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
}

.submit-update-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(39, 174, 96, 0.5);
  background: linear-gradient(135deg, #229954, #1e8449);
}

.submit-update-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Confirmation Modal */
.confirm-modal {
  background: linear-gradient(135deg, #0f0f0f, #202020);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 2.5rem;
  text-align: center;
  max-width: 450px;
  animation: fadeInScale 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.confirm-content h3 {
  margin-bottom: 1rem;
  color: #e91e63;
  font-family: 'Bebas Neue', sans-serif;
  font-size: 1.5rem;
}

.confirm-content p {
  margin-bottom: 2rem;
  color: rgba(255, 255, 255, 0.6);
}

.confirm-delete-btn {
  background: linear-gradient(45deg, #e74c3c, #c0392b);
  color: white;
  border: none;
  padding: 0.9rem 2rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s ease;
}

.confirm-delete-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(231, 76, 60, 0.4);
}

/* Footer */
.footer {
  background: rgba(15, 15, 15,  操作0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1.5rem 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.footer-content p {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9rem;
}

.loading-state {
  text-align: center;
  padding: 3rem;
  color: rgba(255, 255, 255, 0.6);
  font-size: 1.1rem;
}

/* Efecto Glitch (para títulos si quieres activarlo) */
@keyframes glitch {
  0% { text-shadow: 0.05em 0 0 #e91e63, -0.05em -0.025em 0 #3498db, 0.025em 0.05em 0 #ff00ff; }
  15% { text-shadow: 0.05em 0 0 #e91e63, -0.05em -0.025em 0 #3498db, 0.025em 0.05em 0 #ff00ff; }
  16% { text-shadow: -0.05em -0.025em 0 #e91e63, 0.05em 0 0 #3498db, -0.025em -0.05em 0 #ff00ff; }
  17% { text-shadow: 0 0 0 #e91e63, 0 0 0 #3498db, 0 0 0 #ff00ff; }
  18% { text-shadow: -0.05em -0.025em 0 #e91e63, 0.05em 0 0 #3498db, -0.025em -0.05em 0 #ff00ff; }
  20% { text-shadow: 0 0 0 #e91e63, 0 0 0 #3498db, 0 0 0 #ff00ff; }
  22% { text-shadow: 0.05em 0.025em 0 #e91e63, -0.05em 0 0 #3498db, 0.025em -0.05em 0 #ff00ff; }
  40% { text-shadow: 0.05em 0.025em 0 #e91e63, -0.05em 0 0 #3498db, 0.025em -0.05em 0 #ff00ff; }
  41% { text-shadow: -0.05em 0 0 #e91e63, 0.05em -0.025em 0 #3498db, -0.025em 0.05em 0 #ff00ff; }
  42% { text-shadow: 0 0 0 #e91e63, 0 0 0 #3498db, 0 0 0 #ff00ff; }
  43% { text-shadow: -0.05em 0 0 #e91e63, 0.05em -0.025em 0 #3498db, -0.025em 0.05em 0 #ff00ff; }
  45% { text-shadow: 0 0 0 #e91e63, 0 0 0 #3498db, 0 0 0 #ff00ff; }
  70% { text-shadow: 0 0 0 #e91e63, 0 0 0 #3498db, 0 0 0 #ff00ff; }
  71% { text-shadow: 0.05em 0.025em 0 #e91e63, -0.05em 0 0 #3498db, 0.025em -0.05em 0 #ff00ff; }
  72% { text-shadow: -0.05em -0.025em 0 #e91e63, 0.05em 0 0 #3498db, -0.025em -0.05em 0 #ff00ff; }
  100% { text-shadow: 0 0 0 #e91e63, 0 0 0 #3498db, 0 0 0 #ff00ff; }
}

/* Responsive */
@media (max-width: 768px) {
  .header-content, .container { padding: 0 1rem; }
  .filter-section { flex-direction: column; gap: 1rem; }
  .search-input-group { min-width: unset; }
  .logo-section { gap: 0.75rem; }
  .app-title { font-size: 2rem; }
  .top-section { flex-direction: column; gap: 1.5rem; align-items: stretch; }
  .section-title { font-size: 1.5rem; }
  .cards-grid { grid-template-columns: 1fr; }
  .card-actions { flex-direction: column; }
  .edit-btn, .delete-btn, .examen-btn { width: 100%; }
  .modal, .examen-modal { margin: 1rem; max-height: 95vh; }
  .modal-form, .examen-content { padding: 1.5rem; }
  .form-actions { flex-direction: column; gap: 0.75rem; }
  .cancel-btn, .submit-btn { width: 100%; }
  .examen-header { flex-direction: column; text-align: center; }
  .examen-profile-img { width: 100px; height: 100px; }
  .document-preview, .pdf-iframe { max-height: 400px; }
  .update-section { padding: 1.5rem; }
}

@media (max-width: 480px) {
  .header { padding: 1rem 0; }
  .logo-section { flex-direction: column; align-items: flex-start; gap: 0.25rem; }
  .app-title { font-size: 1.75rem; }
  .back-btn { padding: 0.75rem; font-size: 0; width: 45px; height: 45px; justify-content: center; }
  .back-btn svg { margin: 0; }
  .add-btn { font-size: 0.8rem; padding: 0.6rem 1rem; }
  .modal-header h3 { font-size: 1.5rem; }
  .modal-form, .examen-content { padding: 1rem; }
  .photo-preview { min-height: 80px; padding: 0.75rem; }
  .photo-preview svg { width: 36px; height: 36px; }
  .examen-info h2 { font-size: 1.5rem; }
  .update-examen-btn, .submit-update-btn { padding: 0.8rem 1.5rem; font-size: 0.9rem; }
}
</style>