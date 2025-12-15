<template>
  <div class="bar-container">
    <header class="header">
      <div class="header-background"></div>
      <div class="header-content">
        <div class="header-left">
          <div class="bar-info">
            <h1 class="bar-name">{{ bar.name }}</h1>
          </div>
        </div>
        <button class="back-button" @click="goBack">
          <svg class="back-icon" viewBox="0 0 24 24" fill="none">
            <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Volver</span>
        </button>
        <!-- Mensaje informativo elegante -->

      </div>
    </header>
   <div class="info-banner">
    <div class="info-text">
        Las facturas se borran automáticamente
        <span class="highlight">los días 1 de cada mes a las 3:00 a.m.</span>
        <br>
        **Recuerda: Cada comprobante fue enviado a tu email registrado.**
    </div>
</div>
    <main class="main-content">
      <div class="section-header">
        <div class="title-container">
          <div class="title-icon">📊</div>
          <h2 class="section-title">Facturas Generadas</h2>
        </div>
        <div class="stats-badge">
          {{ filteredInvoices.length }} facturas
        </div>
      </div>
      
      <div class="search-section">
        <div class="search-container">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none">
            <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
            <path d="M21 21l-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por fecha (ej: enero), hora (ej: 09:30 AM) o administrador..."
            class="search-input"
          />
          <div v-if="searchQuery" @click="searchQuery = ''" class="clear-search">
            <svg viewBox="0 0 24 24" fill="none">
              <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="invoices-section">
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>Cargando facturas...</p>
        </div>

        <div v-if="error" class="error-state">
          <div class="error-icon">⚠️</div>
          <p>{{ error }}</p>
        </div>

        <div v-if="!isLoading && !error" class="invoice-grid">
          <div
            v-for="invoice in filteredInvoices"
            :key="invoice.id"
            class="invoice-card"
            @click="viewInvoice(invoice)"
          >
            <div class="card-header">
              <div class="date-info">
                <div class="date-primary">{{ formatDate(invoice.fecha) }} - {{ formatTime(invoice.hora) }}</div>
                <div class="time-secondary">{{ formatRelativeTime(invoice.hora) }}</div>
              </div>
              <div class="amount-badge">
                ${{ formatAmount(invoice.total_ingresos) }}
              </div>
            </div>

            <div class="card-body">
              <div class="admin-info">
                <span class="admin-label">Administrador:</span>
                <span class="admin-name">{{ invoice.admin_nombre || 'N/A' }}</span>
              </div>
            </div>

            <div class="card-footer">
              <span class="view-details">Ver detalles</span>
              <svg class="arrow-icon" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>

          <div v-if="filteredInvoices.length === 0 && searchQuery" class="empty-state">
            <div class="empty-icon">📄</div>
            <h3>No se encontraron facturas</h3>
            <p>No se encontraron resultados para la búsqueda "{{ searchQuery }}".</p>
            <p>Intenta ajustar los criterios de búsqueda.</p>
          </div>

          <div v-if="filteredInvoices.length === 0 && !searchQuery" class="empty-state">
            <div class="empty-icon">📄</div>
            <h3>No se encontraron facturas</h3>
            <p>No hay facturas registradas en este momento.</p>
          </div>
        </div>

        <div v-if="hasMore && !isLoading && !error && !searchQuery" class="loading-more-state">
          <div class="loading-spinner"></div>
          <p>Cargando más facturas...</p>
        </div>
        <div v-else-if="invoices.length > 0 && !isLoading && !error && !searchQuery" class="end-of-list">
          <p>Has llegado al final de la lista.</p>
        </div>
      </div>
    </main>

    <Transition name="modal">
      <div v-if="isModalOpen && selectedInvoice" class="modal-backdrop" @click="closeModal">
        <div class="modal-container" @click.stop>
          <div class="modal-header">
            <div class="modal-title-section">
              <h2 class="modal-title">Factura Diaria</h2>
              <div class="modal-subtitle">Detalles completos de la factura</div>
            </div>
            <button @click="closeModal" class="modal-close">
              <svg viewBox="0 0 24 24" fill="none">
                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div class="invoice-summary">
              <div class="summary-grid">
                <div class="summary-item">
                  <div class="summary-label">📅 Fecha</div>
                  <div class="summary-value">{{ formatDate(selectedInvoice.fecha) }}</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">🕒 Hora</div>
                  <div class="summary-value">{{ formatTime(selectedInvoice.hora) }}</div>
                </div>
                <div class="summary-item">
                  <div class="summary-label">👤 Admin</div>
                  <div class="summary-value">{{ selectedInvoice.admin_nombre }}</div>
                </div>
              </div>

              <div class="totals-grid">
                <div class="total-item total-ingresos">
                  <div class="total-label">💰 Ingresos Totales</div>
                  <div class="total-amount">${{ formatAmount(selectedInvoice.total_ingresos) }}</div>
                </div>
                <div class="total-item total-gastos">
                  <div class="total-label">💸 Gastos Totales</div>
                  <div class="total-amount">${{ formatAmount(selectedInvoice.total_gastos) }}</div>
                </div>
                <div class="total-item total-neto total-neto-special">
                  <div class="total-label">📈 Total Neto</div>
                  <div class="total-amount">${{ formatAmount(selectedInvoice.total_neto) }}</div>
                </div>
              </div>
            </div>

            <div class="gastos-section" v-if="selectedInvoice.gastos && selectedInvoice.gastos.length > 0">
              <h3 class="gastos-title">
                <span class="gastos-icon">💸</span>
                Gastos
              </h3>
              <div class="gastos-list">
                <div v-for="gasto in selectedInvoice.gastos" :key="gasto.id" class="gasto-item">
                  <div class="gasto-name">{{ gasto.nombre }}</div>
                  <div class="gasto-price">${{ formatAmount(gasto.precio) }}</div>
                </div>
              </div>
            </div>

            <div class="products-section">
              <h3 class="products-title">
                <span class="products-icon">🛍️</span>
                Detalle de Productos
              </h3>

              <div class="products-list">
                <div
                  v-for="item in selectedInvoice.detalles_factura"
                  :key="item.id"
                  class="product-item"
                >
                  <div class="product-image-container">
                    <img :src="item.imagen_producto" alt="Producto" class="product-image" />
                  </div>

                  <div class="product-details">
                    <h4 class="product-name">{{ item.nombre_producto }}</h4>

                    <div class="product-metrics">
                      <div class="metric-row">
                        <span class="metric-label">Inicial:</span>
                        <span class="metric-value">{{ item.cantidad_inicial }}</span>
                      </div>
                      <div class="metric-row">
                        <span class="metric-label">Final:</span>
                        <span class="metric-value">{{ item.cantidad_final }}</span>
                      </div>
                      <div class="metric-row highlight">
                        <span class="metric-label">Vendidos:</span>
                        <span class="metric-value sold">{{ item.cantidad_vendida }}</span>
                      </div>
                      <div class="metric-row">
                        <span class="metric-label">Precio unitario:</span>
                        <span class="metric-value price">${{ formatAmount(item.precio_unitario) }}</span>
                      </div>
                      <div class="metric-row total">
                        <span class="metric-label">Subtotal:</span>
                        <span class="metric-value subtotal">${{ formatAmount(item.subtotal) }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="closeModal" class="close-modal-button">
              <span>Cerrar</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useActiveBarStore } from '@/stores/activeBar';
import axios from 'axios';
import { format, formatDistanceToNow, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';
import Swal from 'sweetalert2';
// *** 1. IMPORTACIÓN DE LA CONSTANTE GLOBAL CON RUTA RELATIVA ***
import { API_BASE_URL } from '../config/api';
// *************************************************************

const router = useRouter();
// Eliminada: const API_URL = 'http://192.168.100.37:8000';

const formatDate = (dateString) => {
  const date = parseISO(dateString);
  return format(date, "EEEE, d 'de' MMMM 'de' yyyy", { locale: es });
};

const formatTime = (isoString) => {
  if (!isoString) return '';
  const date = parseISO(isoString);
  return format(date, 'hh:mm a', { 
    locale: es,
    timeZone: 'America/Bogota'  // ← Esta línea es la clave
  });
};

const formatRelativeTime = (isoString) => {
  const date = parseISO(isoString);
  return formatDistanceToNow(date, { addSuffix: true, locale: es });
};

const formatAmount = (amount) => {
  if (typeof amount !== 'number') return '$0';
  return amount.toLocaleString('es-CO', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  });
};

const goBack = () => {
  router.go(-1);
};

const bar = useActiveBarStore();
const invoices = ref([]);
const searchQuery = ref('');
const selectedInvoice = ref(null);
const isModalOpen = ref(false);
const isLoading = ref(true);
const error = ref(null);

const page = ref(0);
const pageSize = 15;
const hasMore = ref(true);
const isLoadingMore = ref(false);

const filteredInvoices = computed(() => {
  const query = searchQuery.value.toLowerCase().trim();
  if (!query) {
    return invoices.value;
  }
  return invoices.value.filter(invoice => {
    const adminName = (invoice.admin_nombre || '').toLowerCase();
    const formattedDate = formatDate(invoice.fecha).toLowerCase();
    const formattedTime = formatTime(invoice.hora).toLowerCase();

    return adminName.includes(query) || formattedDate.includes(query) || formattedTime.includes(query);
  });
});

const fetchData = async (isInitialLoad = true) => {
  if (isInitialLoad) {
    isLoading.value = true;
    error.value = null;
    invoices.value = [];
    page.value = 0;
  }

  const barId = bar.id;
  if (!barId) {
    error.value = "ID del bar no disponible. Por favor, intente de nuevo.";
    isLoading.value = false;
    return;
  }

  try {
    // *** USO DE LA CONSTANTE GLOBAL ***
    const response = await axios.get(`${API_BASE_URL}/facturas/bar/${barId}`, {
      params: { skip: page.value * pageSize, limit: pageSize }
    });

    const newInvoices = response.data;
    invoices.value = [...invoices.value, ...newInvoices];
    page.value += 1;
    hasMore.value = newInvoices.length === pageSize;
  } catch (err) {
    console.error("Error al cargar las facturas:", err);
    error.value = "Hubo un error al cargar las facturas.";
  } finally {
    isLoading.value = false;
    isLoadingMore.value = false;
  }
};

const checkAndLoadMore = async () => {
  await nextTick();
  const { scrollHeight, clientHeight } = document.documentElement;
  if (scrollHeight <= clientHeight && hasMore.value) {
    await fetchData(false);
    await checkAndLoadMore(); // Vuelve a verificar recursivamente hasta que la página se llene o se acaben los datos.
  }
};

const handleScroll = async () => {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
  if (scrollTop + clientHeight >= scrollHeight - 200 && hasMore.value && !isLoadingMore.value && !searchQuery.value) {
    isLoadingMore.value = true;
    await fetchData(false);
  }
};

onMounted(async () => {
  await fetchData();
  checkAndLoadMore();
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

const viewInvoice = (invoice) => {
  selectedInvoice.value = invoice;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedInvoice.value = null;
};

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* --- Reset & Base Styles --- */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.bar-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
  font-family: 'Inter', sans-serif;
  color: white;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}

/* --- Header Section --- */
.header {
  position: relative;
  padding: 2rem 1rem;
  overflow: hidden;
}

.header-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #e91e63 0%, #3f51b5 100%);
  opacity: 0.1;
  z-index: 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 2;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.header-left {
  display: flex;
  align-items: center;
  flex-grow: 1;
}

.bar-info {
  display: flex;
  flex-direction: column;
}

.bar-name {
  font-size: clamp(1.5rem, 5vw, 2.5rem);
  font-weight: 800;
  background: linear-gradient(135deg, #e91e63, #3f51b5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.2;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #3f51b5, #2196f3);
  border: none;
  border-radius: 25px;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(63, 81, 181, 0.4);
  white-space: nowrap;
}

.back-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(63, 81, 181, 0.6);
}

.back-icon {
  width: 20px;
  height: 20px;
  stroke: currentColor;
}

/* --- Botón de Eliminar --- */
.delete-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #f44336, #e53935);
  border: none;
  border-radius: 25px;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(244, 67, 54, 0.4);
  white-space: nowrap;
}

.delete-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(244, 67, 54, 0.6);
}

.delete-button svg {
  width: 20px;
  height: 20px;
  stroke: currentColor;
}

/* --- Main Content Section --- */
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem 4rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.title-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.title-icon {
  font-size: clamp(1.5rem, 5vw, 2rem);
  width: clamp(45px, 10vw, 60px);
  height: clamp(45px, 10vw, 60px);
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e91e63, #3f51b5);
  box-shadow: 0 5px 20px rgba(233, 30, 99, 0.3);
}

.section-title {
  font-size: clamp(2rem, 5vw, 2.5rem);
  font-weight: 700;
  background: linear-gradient(135deg, white, #e0e0e0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
  line-height: 1.2;
}

.stats-badge {
  background: linear-gradient(135deg, #e91e63, #3f51b5);
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: 600;
  color: white;
  box-shadow: 0 5px 15px rgba(233, 30, 99, 0.3);
  white-space: nowrap;
}

/* --- Search Section --- */
.search-section {
  margin-bottom: 3rem;
}

.search-container {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.search-icon {
  position: absolute;
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.7);
  z-index: 2;
  stroke: currentColor;
}

.search-input {
  width: 100%;
  padding: 1.25rem 1.25rem 1.25rem 4rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 25px;
  color: white;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.search-input:focus {
  outline: none;
  border-color: #e91e63;
  box-shadow: 0 0 0 3px rgba(233, 30, 99, 0.1);
}

.clear-search {
  position: absolute;
  right: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.3s ease;
  stroke: currentColor;
}

.clear-search:hover {
  color: #e91e63;
}

/* --- Invoices Section --- */
.loading-state, .error-state, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top: 3px solid #e91e63;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-icon, .empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.loading-more-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
}

.end-of-list {
  display: flex;
  justify-content: center;
  padding: 2rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.invoice-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.invoice-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.invoice-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(135deg, #e91e63, #3f51b5);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.invoice-card:hover {
  transform: translateY(-5px);
  border-color: rgba(233, 30, 99, 0.3);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.invoice-card:hover::before {
  transform: scaleX(1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.date-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.date-primary {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
}

.time-secondary {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
}

.amount-badge {
  background: linear-gradient(135deg, #4caf50, #2196f3);
  padding: 0.5rem 1rem;
  border-radius: 15px;
  font-weight: 700;
  font-size: 1.1rem;
  color: white;
  box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
  white-space: nowrap;
}

.card-body {
  margin-bottom: 1.5rem;
}

.admin-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.admin-label {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.admin-name {
  font-size: 1rem;
  font-weight: 600;
  color: #e91e63;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.view-details {
  color: #3f51b5;
  font-weight: 600;
  font-size: 0.9rem;
}

.arrow-icon {
  width: 20px;
  height: 20px;
  color: #3f51b5;
  transition: transform 0.3s ease;
  stroke: currentColor;
}

.invoice-card:hover .arrow-icon {
  transform: translateX(5px);
}

/* --- Modal Styles --- */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  backdrop-filter: blur(5px);
}

.modal-container {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 25px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  position: relative;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 2rem;
  background: linear-gradient(135deg, #e91e63 0%, #3f51b5 100%);
  color: white;
}

.modal-title-section {
  flex-grow: 1;
}

.modal-title {
  font-size: clamp(1.5rem, 5vw, 2rem);
  font-weight: 700;
  margin: 0 0 0.5rem;
}

.modal-subtitle {
  font-size: 1rem;
  opacity: 0.9;
}

.modal-close {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 10px;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  margin-left: 1rem;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: rotate(90deg);
}

.modal-close svg {
  width: 20px;
  height: 20px;
  stroke: currentColor;
}

.modal-body {
  padding: 2rem;
  overflow-y: auto;
  flex-grow: 1;
}

.invoice-summary {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-item {
  text-align: center;
}

.summary-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.5rem;
}

.summary-value {
  font-size: 1.1rem;
  font-weight: 600;
  color: white;
}

.totals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.total-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  border-radius: 10px;
  text-align: center;
  transition: all 0.3s ease;
}

.total-ingresos {
  background: rgba(76, 175, 80, 0.1);
  color: #4caf50;
}

.total-gastos {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
}

/* ✨ Nuevo estilo para el Total Neto con efecto tornasol azul y rosado */
.total-neto-special {
  background-image: linear-gradient(135deg, #3f51b5, #e91e63, #3f51b5, #e91e63);
  background-size: 200% auto;
  color: white;
  padding: 1.5rem;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
  transform: scale(1.05);
  z-index: 1;
  animation: color-shift 4s ease-in-out infinite;
}

@keyframes color-shift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.total-label {
  font-size: 1rem;
  font-weight: 500;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.total-amount {
  font-size: clamp(1.5rem, 4vw, 2rem);
  font-weight: 800;
}

.products-section, .gastos-section {
  margin-top: 2rem;
}

.products-title, .gastos-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: clamp(1.25rem, 4vw, 1.5rem);
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: white;
}

.products-icon, .gastos-icon {
  font-size: 1.5rem;
}

.products-list, .gastos-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-height: 40vh;
  overflow-y: auto;
  padding-right: 1rem;
}

/* Scrollbar styling for Webkit browsers */
.products-list::-webkit-scrollbar, .gastos-list::-webkit-scrollbar {
  width: 6px;
}

.products-list::-webkit-scrollbar-thumb, .gastos-list::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #e91e63, #3f51b5);
  border-radius: 10px;
}

.product-item, .gasto-item {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.product-image-container {
  flex-shrink: 0;
  margin: 0 auto;
}

.product-image {
  width: clamp(60px, 15vw, 80px);
  height: clamp(60px, 15vw, 80px);
  border-radius: 10px;
  object-fit: cover;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.product-details {
  flex-grow: 1;
}

.product-name {
  font-size: clamp(1rem, 3vw, 1.2rem);
  font-weight: 600;
  color: #e91e63;
  margin-bottom: 1rem;
}

.product-metrics {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

.metric-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.metric-row.highlight {
  background: rgba(233, 30, 99, 0.1);
  border-radius: 8px;
  padding: 0.75rem;
  margin: 0.25rem 0;
}

.metric-row.total {
  background: rgba(63, 81, 181, 0.1);
  border-radius: 8px;
  padding: 0.75rem;
  margin: 0.25rem 0;
  font-weight: 600;
}

.metric-label {
  font-size: clamp(0.8rem, 2.5vw, 0.9rem);
  color: rgba(255, 255, 255, 0.7);
}

.metric-value {
  font-weight: 600;
  color: white;
  font-size: clamp(0.9rem, 2.8vw, 1.1rem);
}

.metric-value.sold {
  color: #e91e63;
  font-weight: 700;
}

.metric-value.price {
  color: #4caf50;
}

.metric-value.subtotal {
  color: #3f51b5;
  font-weight: 700;
}

/* --- Gastos Specific Styles --- */
.gasto-item {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  gap: 1rem;
  background: rgba(244, 67, 54, 0.08);
  border: 1px solid rgba(244, 67, 54, 0.2);
  border-radius: 15px;
  transition: transform 0.2s ease;
}

.gasto-item:hover {
  transform: translateX(5px);
}

.gasto-name {
  font-weight: 500;
  color: white;
  flex-grow: 1;
  font-size: clamp(0.9rem, 3vw, 1rem);
}

.gasto-price {
  font-weight: 600;
  color: #f44336;
  white-space: nowrap;
  font-size: clamp(0.9rem, 3vw, 1rem);
}

.modal-footer {
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: center;
}

.close-modal-button {
  background: linear-gradient(135deg, #3f51b5, #2196f3);
  border: none;
  border-radius: 25px;
  padding: 1rem 3rem;
  color: white;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(63, 81, 181, 0.4);
}

.close-modal-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(63, 81, 181, 0.6);
}

/* --- Transiciones del Modal --- */
.modal-enter-active, .modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.modal-enter-to, .modal-leave-from {
  opacity: 1;
  transform: scale(1);
}

/* ========================================== */
/* === RESPONSIVE DESIGN OPTIMIZADO === */
/* ========================================== */

/* --- Large Tablets (1024px y menos) --- */
@media (max-width: 1024px) {
  .invoice-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

/* --- Tablets (768px y menos) --- */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    text-align: center;
  }

  .header-left {
    justify-content: center;
  }

  .back-button, .delete-button {
    width: 100%;
    justify-content: center;
    order: -1;
    padding: 0.75rem 1.5rem;
  }

  .section-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .stats-badge {
    width: 100%;
    text-align: center;
  }

  .search-input {
    padding: 1rem 1rem 1rem 3rem;
    font-size: 0.9rem;
  }

  .search-icon, .clear-search {
    left: 1rem;
    right: 1rem;
    width: 18px;
    height: 18px;
  }

  .invoice-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  /* === MODAL OPTIMIZADO PARA TABLETS === */
  .modal-container {
    border-radius: 15px;
    max-height: 95vh;
    margin: 0.5rem;
  }

  .modal-header {
    padding: 1.5rem 1rem;
  }

  .modal-title {
    font-size: 1.4rem;
    margin-bottom: 0.25rem;
  }

  .modal-subtitle {
    font-size: 0.85rem;
    opacity: 0.8;
  }

  .modal-body {
    padding: 1rem;
    font-size: 0.9rem;
  }

  /* --- Summary Section Optimizado --- */
  .invoice-summary {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
  }

  .summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .summary-item {
    text-align: center;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
  }

  .summary-label {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 0.4rem;
    font-weight: 500;
  }

  .summary-value {
    font-size: 0.9rem;
    font-weight: 600;
    color: white;
    line-height: 1.2;
  }

  /* --- Totales Grid Mejorado --- */
  .totals-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.75rem;
    padding-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
  }

  .total-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.875rem;
    border-radius: 8px;
    flex-direction: row;
  }

  .total-neto-special {
    background-image: linear-gradient(135deg, #3f51b5, #e91e63);
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    transform: none;
    animation: none;
  }

  .total-label {
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0;
    opacity: 0.9;
  }

  .total-amount {
    font-size: 1.1rem;
    font-weight: 700;
    text-align: right;
  }

  /* --- Gastos Section Optimizado --- */
  .gastos-section {
    margin-top: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1rem;
  }

  .gastos-title {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    gap: 0.5rem;
  }

  .gastos-icon {
    font-size: 1.2rem;
    filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.3));
  }

  .gastos-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    max-height: 30vh;
    overflow-y: auto;
    padding-right: 0.5rem;
  }

  .gasto-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    gap: 1rem;
    background: rgba(244, 67, 54, 0.1);
    border: 1px solid rgba(244, 67, 54, 0.25);
    border-radius: 8px;
    transition: transform 0.2s ease;
  }

  .gasto-item:active {
    transform: scale(0.98);
    transition: transform 0.1s ease;
  }

  .gasto-name {
    font-weight: 500;
    color: white;
    flex-grow: 1;
    font-size: 0.85rem;
    line-height: 1.3;
  }

  .gasto-price {
    font-weight: 600;
    color: #ff5252;
    font-size: 0.85rem;
    white-space: nowrap;
  }

  /* --- Products Section Optimizado --- */
  .products-section {
    margin-top: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1rem;
  }

  .products-title {
    font-size: 1.1rem;
    margin-bottom: 1rem;
    gap: 0.5rem;
  }

  .products-icon {
    font-size: 1.2rem;
    filter: drop-shadow(0 0 4px rgba(255, 255, 255, 0.3));
  }

  .products-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    max-height: 45vh;
    overflow-y: auto;
    padding-right: 0.5rem;
  }

  /* --- Product Item Completamente Rediseñado --- */
  .product-item {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.12);
    align-items: flex-start;
  }

  .product-item:active {
    transform: scale(0.98);
    transition: transform 0.1s ease;
  }

  .product-image-container {
    flex-shrink: 0;
    margin: 0;
  }

  .product-image {
    width: 50px;
    height: 50px;
    border-radius: 8px;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.15);
  }

  .product-details {
    flex-grow: 1;
    min-width: 0;
  }

  .product-name {
    font-size: 0.9rem;
    font-weight: 600;
    color: #e91e63;
    margin-bottom: 0.75rem;
    line-height: 1.2;
    word-break: break-word;
  }

  /* --- Metrics Compactos y Legibles --- */
  .product-metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.4rem;
    font-size: 0.75rem;
  }

  .metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.25rem 0.5rem;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 4px;
  }

  .metric-row.highlight {
    background: rgba(233, 30, 99, 0.15);
    border: 1px solid rgba(233, 30, 99, 0.3);
    padding: 0.4rem 0.6rem;
    grid-column: span 2;
    margin: 0.2rem 0;
  }

  .metric-row.total {
    background: rgba(63, 81, 181, 0.15);
    border: 1px solid rgba(63, 81, 181, 0.3);
    padding: 0.4rem 0.6rem;
    grid-column: span 2;
    margin: 0.2rem 0;
    font-weight: 600;
  }

  .metric-label {
    font-size: 0.7rem;
    color: rgba(255, 255, 255, 0.7);
    font-weight: 500;
  }

  .metric-value {
    font-weight: 600;
    color: white;
    font-size: 0.75rem;
    text-align: right;
  }

  .metric-value.sold {
    color: #ff4081;
    font-weight: 700;
    font-size: 0.8rem;
  }

  .metric-value.price {
    color: #4caf50;
    font-size: 0.75rem;
  }

  .metric-value.subtotal {
    color: #3f51b5;
    font-weight: 700;
    font-size: 0.8rem;
  }

  /* --- Footer del Modal --- */
  .modal-footer {
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
  }

  .close-modal-button {
    width: 100%;
    padding: 0.875rem;
    font-size: 0.9rem;
    border-radius: 10px;
  }
}

/* --- Mobile Phones (480px y menos) --- */
@media (max-width: 480px) {
  .header-content, .main-content {
    padding: 0 0.5rem;
  }

  .header {
    padding: 1.5rem 0.5rem;
  }

  .bar-name {
    font-size: 1.5rem;
  }

  .back-button, .delete-button {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
    gap: 0.5rem;
  }

  .back-icon, .delete-button svg {
    width: 16px;
    height: 16px;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .title-icon {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }

  .stats-badge {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
  }

  .search-input {
    font-size: 0.8rem;
    padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  }

  .search-icon, .clear-search {
    width: 16px;
    height: 16px;
  }

  .invoice-card {
    padding: 1rem;
  }

  .date-primary {
    font-size: 1rem;
  }

  .time-secondary {
    font-size: 0.75rem;
  }

  .amount-badge {
    font-size: 0.9rem;
    padding: 0.3rem 0.6rem;
  }

  .admin-name {
    font-size: 0.85rem;
  }

  .view-details {
    font-size: 0.75rem;
  }

  .arrow-icon {
    width: 16px;
    height: 16px;
  }

  /* === MODAL EXTRA PEQUEÑO === */
  .modal-container {
    margin: 0.25rem;
    max-height: 98vh;
    border-radius: 12px;
  }

  .modal-header {
    padding: 1rem 0.875rem;
  }

  .modal-title {
    font-size: 1.2rem;
  }

  .modal-subtitle {
    font-size: 0.8rem;
  }

  .modal-body {
    padding: 0.875rem;
    font-size: 0.85rem;
  }

  .invoice-summary {
    padding: 1rem;
  }

  .summary-grid {
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }

  .summary-item {
    padding: 0.6rem;
  }

  .summary-label {
    font-size: 0.7rem;
  }

  .summary-value {
    font-size: 0.8rem;
  }

  .totals-grid {
    gap: 0.6rem;
  }

  .total-item {
    padding: 0.75rem;
  }

  .total-label {
    font-size: 0.75rem;
  }

  .total-amount {
    font-size: 1rem;
  }

  .total-neto-special {
    padding: 0.875rem;
  }

  .gastos-title, .products-title {
    font-size: 1rem;
    margin-bottom: 0.875rem;
  }

  .gastos-list {
    max-height: 25vh;
    gap: 0.6rem;
  }

  .gasto-item {
    padding: 0.6rem 0.875rem;
  }

  .gasto-name, .gasto-price {
    font-size: 0.8rem;
  }

  .products-list {
    max-height: 40vh;
    gap: 0.875rem;
  }

  .product-item {
    padding: 0.875rem;
    gap: 0.875rem;
  }

  .product-image {
    width: 45px;
    height: 45px;
  }

  .product-name {
    font-size: 0.85rem;
    margin-bottom: 0.6rem;
  }

  .product-metrics {
    gap: 0.3rem;
  }

  .metric-row {
    padding: 0.2rem 0.4rem;
  }

  .metric-row.highlight, .metric-row.total {
    padding: 0.35rem 0.5rem;
  }

  .metric-label {
    font-size: 0.65rem;
  }

  .metric-value {
    font-size: 0.7rem;
  }

  .metric-value.sold, .metric-value.subtotal {
    font-size: 0.75rem;
  }

  .modal-footer {
    padding: 0.875rem;
  }

  .close-modal-button {
    padding: 0.75rem;
    font-size: 0.85rem;
  }
}

/* --- Scrollbar personalizado para móviles --- */
@media (max-width: 768px) {
  .products-list::-webkit-scrollbar, .gastos-list::-webkit-scrollbar {
    width: 4px;
  }

  .products-list::-webkit-scrollbar-track, .gastos-list::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
  }

  .products-list::-webkit-scrollbar-thumb, .gastos-list::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #e91e63, #3f51b5);
    border-radius: 4px;
  }

  /* Mejora el contraste de texto */
  .modal-container {
    background: linear-gradient(135deg, #1e1e2e 0%, #1a1a2e 100%);
  }
}
/* --- Banner informativo elegante --- */
.info-banner {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem 2rem;
  background: linear-gradient(135deg, rgba(63, 81, 181, 0.3), rgba(233, 30, 99, 0.3));
  border: 1px solid rgba(233, 30, 99, 0.4);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  max-width: 480px;
  animation: float 6s ease-in-out infinite;
}

.info-icon {
  font-size: 2.2rem;
  filter: drop-shadow(0 0 8px rgba(255,255,255,0.4));
}

.info-text {
  color: white;
  font-size: 1rem;
  line-height: 1.5;
}

.info-text .highlight {
  color: #e91e63;
  font-weight: 700;
}

.info-text .secondary {
  font-size: 0.92rem;
  opacity: 0.9;
  display: block;
  margin-top: 0.4rem;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

/* Responsive del banner */
@media (max-width: 768px) {
  .info-banner {
    max-width: none;
    width: 100%;
    padding: 1rem 1.5rem;
    flex-direction: column;
    text-align: center;
  }
  
  .info-icon {
    font-size: 2.5rem;
  }
}
</style>