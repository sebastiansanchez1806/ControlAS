<template>
  <div class="invoice-container">
    <header class="app-header">
      <button @click="goBack" class="back-button">Volver</button>
      <div class="header-content">
        <h1 class="header-title">{{ adminStore.bar_nombre }}</h1>
        <p class="header-subtitle">Gestor de Facturas</p>
      </div>
    </header>

    <div v-if="!isModalOpen" class="main-content">
      <div class="header-section">
        <h1 class="main-title">Control de Inventario</h1>
        <p class="subtitle">
  Genera la factura de {{ adminStore.bar_nombre }}.  
  Las facturas se borrarán el primer día de cada mes a las 3:00 a.m.
</p>

      </div>

      <button @click="startInvoice" class="primary-button">
        <span class="button-icon">📋</span>
        <span class="button-text">Generar Factura</span>
      </button>

      <div class="history-section">
        <h2 class="history-title">Historial de Facturas 📝</h2>
        <div class="search-container">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar por fecha (día/mes) o hora..."
            class="search-input"
          />
          <span class="search-icon">🔍</span>
        </div>

        <div v-if="loadingHistory && invoices.length === 0" class="loading-message">Cargando historial de facturas...</div>
        <div v-else-if="!invoices.length && !loadingHistory" class="no-invoices">
          {{ searchQuery ? 'No se encontraron facturas con esa búsqueda.' : 'No se han generado facturas aún.' }}
        </div>

        <ul v-else class="invoices-list" @scroll="handleScroll">
          <li v-for="invoice in filteredInvoices" :key="invoice.id" @click="viewInvoiceDetails(invoice)" class="invoice-item">
            <div class="invoice-info-header">
              <span class="invoice-date">
  📅 {{ formatInvoiceDate(invoice.fecha) }}
</span>
              <span class="invoice-time">
  🕒 {{ formatInvoiceTime(invoice.hora) }}
</span>
            </div>
            <div class="invoice-total">
              Total Neto: <span class="total-amount">{{ formatCurrency(invoice.total_neto) }}</span>
            </div>
          </li>
          <li v-if="loadingMore" class="loading-more">Cargando más facturas...</li>
        </ul>
      </div>
    </div>
    
    <div v-if="isModalOpen" class="modal-backdrop">
      <div class="modal-container">
        <button @click="closeModal" class="modal-close-button">
          <span class="close-icon">✖️</span>
        </button>

        <div v-if="!isInvoiceGenerated && !isViewingDetails && !isGastosHormigaStep" class="product-section">
          <div class="progress-container">
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: `${((currentProductIndex + 1) / products.length) * 100}%` }"
              ></div>
            </div>
            <p class="progress-text">
              Producto {{ currentProductIndex + 1 }} de {{ products.length }}
            </p>
          </div>
          
          <div class="product-card">
            <div class="product-header">
              <div class="product-image-wrapper">
                <img 
                  :src="currentProduct.imagen || 'https://placehold.co/120x120/cccccc/333333?text=Sin+imagen'" 
                  :alt="currentProduct.nombre" 
                  class="product-image"
                />
              </div>
              <h3 class="product-name">{{ currentProduct.nombre }}</h3>
            </div>
            
            <div class="product-details">
              <div class="detail-row">
                <div class="detail-item">
                  <span class="detail-label">Cantidad Inicial</span>
                  <span class="detail-value">{{ currentProduct.cantidad }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">Precio Unitario</span>
                  <span class="detail-value price">{{ formatCurrency(currentProduct.precio) }}</span>
                </div>
              </div>
              
              <div class="input-section">
                <label class="input-label">¿Cuántos productos quedaron?</label>
                <div class="input-wrapper">
                  <input
                    v-model.number="currentProduct.finalQuantity"
                    type="number"
                    :min="0"
                    :max="currentProduct.cantidad"
                    class="quantity-input"
                    placeholder="0"
                  />
                  <span class="input-border"></span>
                </div>
                <p v-if="currentProduct.finalQuantity > currentProduct.cantidad" class="error-text">
                  ⚠️ Cantidad mayor al inventario disponible
                </p>
              </div>
            </div>
            
            <div class="product-summary">
              <div class="summary-item sold">
                <span class="summary-label">Vendidos</span>
                <span class="summary-value">{{ calculatedSold }}</span>
              </div>
              <div class="summary-item subtotal">
                <span class="summary-label">Subtotal</span>
                <span class="summary-value">{{ formatCurrency(calculatedSubtotal) }}</span>
              </div>
            </div>
          </div>
          
          <div class="navigation-section">
            <button
              @click="previousProduct"
              :disabled="currentProductIndex === 0"
              class="nav-button prev"
            >
              <span class="nav-icon">←</span>
              <span>Anterior</span>
            </button>
            
            <div class="nav-dots">
              <span 
                v-for="(_, index) in products" 
                :key="index"
                class="dot"
                :class="{ active: index === currentProductIndex }"
              ></span>
            </div>
            
            <button
  @click="nextProduct"
  :disabled="isNextDisabled"
  class="nav-button next primary-nav"
>
              <span v-if="currentProductIndex < products.length - 1">Siguiente</span>
              <span v-else>Continuar</span>
              <span class="nav-icon">→</span>
            </button>
          </div>
          
          <div class="action-buttons">
            <button @click="closeModal" class="cancel-button">
              <span class="cancel-icon">✖️</span>
              <span>Cancelar Factura</span>
            </button>
          </div>
        </div>

<div v-if="isGastosHormigaStep" class="gastos-hormiga-section">
  <h2 class="section-title">Gastos del Día</h2>
  <p class="section-subtitle">
    Añade los gastos pequeños del día para un cálculo más exacto.
  </p>

  <!-- Lista de gastos agregados -->
  <div v-if="gastosHormiga.length > 0" class="gastos-added-list">
    <div v-for="(gasto, index) in gastosHormiga" :key="index" class="gasto-added-item">
      <div class="gasto-added-info">
        <span class="gasto-added-desc">{{ gasto.descripcion }}</span>
        <span class="gasto-added-price">{{ formatCurrency(gasto.monto) }}</span>
      </div>
      <div class="gasto-added-actions">
        <button @click="editGasto(index)" class="edit-gasto-btn">
          <span class="edit-icon">✏️</span>
        </button>
        <button @click="removeGastoHormiga(index)" class="remove-gasto-btn-mini">
          <span class="remove-icon">🗑️</span>
        </button>
      </div>
    </div>
  </div>

  <div v-else class="no-gastos-message">
    No has agregado gastos todavía. ¡Agrega uno para comenzar!
  </div>

  <!-- Botón para abrir modal -->
  <button @click="openGastosModal" class="add-gasto-button-main">
    <span class="add-icon">+</span>
    <span>Agregar Gasto</span>
  </button>

  <!-- Resumen de totales -->
  <div class="gastos-summary">
    <div class="summary-item">
      <span class="summary-label">Total Gastos</span>
      <span class="summary-value">{{ formatCurrency(totalGastosHormiga) }}</span>
    </div>
    <div class="summary-item">
      <span class="summary-label">Ingresos de Productos</span>
      <span class="summary-value ingresos">{{ formatCurrency(total_ingresos) }}</span>
    </div>
    <div class="summary-item final-income">
      <span class="summary-label">Ingresos Netos</span>
      <span class="summary-value final">{{ formatCurrency(totalIngresosNetos) }}</span>
    </div>
  </div>

  <!-- Botones de acción -->
  <div class="action-buttons-gastos">
    <button
      @click="generateInvoice"
      :disabled="isGenerating"
      class="generate-button"
    >
      <span class="generate-icon">📝</span>
      <span>{{ isGenerating ? 'Generando...' : 'Generar Factura Final' }}</span>
    </button>

    <button @click="isGastosHormigaStep = false" class="cancel-button">
      <span class="cancel-icon">←</span>
      <span>Volver a productos</span>
    </button>
  </div>

  <!-- Modal para agregar/editar gasto -->
  <div v-if="isGastosModalOpen" class="gastos-modal-backdrop" @click.self="closeGastosModal">
    <div class="gastos-modal-content">
      <button @click="closeGastosModal" class="gastos-modal-close">✖️</button>
      
      <h3 class="gastos-modal-title">Agregar Gasto</h3>
      
      <div class="gastos-modal-form">
        <div class="form-group">
          <label class="form-label">Descripción del gasto</label>
          <input 
            v-model="tempGasto.descripcion" 
            type="text" 
            placeholder="Ej: Servilletas, hielo, limpieza..." 
            class="form-input"
            @keyup.enter="saveGastoFromModal"
          />
        </div>
        
        <div class="form-group">
          <label class="form-label">Monto del gasto</label>
          <input 
            :value="tempGasto.monto ? formatCurrency(tempGasto.monto, false) : ''"
            @input="updateTempGastoMonto" 
            type="text" 
            inputmode="numeric"
            placeholder="0" 
            class="form-input price-input-modal"
            @keyup.enter="saveGastoFromModal"
          />
        </div>
      </div>
      
      <button @click="saveGastoFromModal" class="save-gasto-button">
        <span>💾</span>
        <span>Guardar Gasto</span>
      </button>
    </div>
  </div>
</div>

        <div v-if="isInvoiceGenerated || isViewingDetails" class="invoice-view">
          <div class="invoice-header">
            <div class="invoice-title-section">
              <h2 class="invoice-title">Factura Diaria</h2>
              <div class="invoice-badge">Completada</div>
            </div>
            
            <div class="invoice-info">
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-icon">📅</span>
                  <div class="info-content">
                    <span class="info-label">Fecha</span>
                    <span class="info-value">{{ formatFullInvoiceDate(displayedInvoice.fecha) }}</span>
                  </div>
                </div>
                <div class="info-item">
                  <span class="info-icon">🕐</span>
                  <div class="info-content">
                    <span class="info-label">Hora</span>
                   <span class="info-value">{{ formatInvoiceTime(displayedInvoice.hora) }}</span>
                  </div>
                </div>
                 <div class="info-item">
                  <span class="info-icon">👤</span>
                  <div class="info-content">
                    <span class="info-label">Generada por:</span>
                    <span class="info-value">{{ adminStore.nombre }} </span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="total-section">
              <div class="total-card ingresos-card">
                <span class="total-label">Ingresos de Productos</span>
                <span class="total-amount">{{ formatCurrency(displayedInvoice.total_ingresos) }}</span>
              </div>
              <div class="total-card gastos-card">
                <span class="total-label">Gastos</span>
                <span class="total-amount">{{ formatCurrency(displayedInvoice.total_gastos) }}</span>
              </div>
              <div class="total-card netos-card">
                <span class="total-label">Ingresos Netos</span>
                <span class="total-amount">{{ formatCurrency(displayedInvoice.total_neto) }}</span>
              </div>
            </div>
          </div>
          
          <div v-if="displayedInvoice.gastos && displayedInvoice.gastos.length > 0" class="gastos-summary-view">
            <h3 class="summary-title">Detalle de Gastos</h3>
            <ul class="gastos-list-view">
              <li v-for="gasto in displayedInvoice.gastos" :key="gasto.id" class="gasto-item-view">
                <span class="gasto-description">{{ gasto.nombre }}</span>
                <span class="gasto-amount">{{ formatCurrency(gasto.precio) }}</span>
              </li>
            </ul>
          </div>

          <div class="products-summary">
            <h3 class="summary-title">Detalle de Productos</h3>
            <div class="products-list">
              <div v-for="item in displayedInvoice.detalles_factura" :key="item.id" class="product-summary-card">
                <div class="card-header">
                  <div class="product-summary-name-wrapper">
                    <img
                      :src="item.imagen_producto || 'https://placehold.co/50x50/cccccc/333333?text=Sin+imagen'"
                      :alt="item.nombre_producto"
                      class="product-summary-image"
                    />
                      <h4 class="product-summary-name">{{ item.nombre_producto }}</h4>
                  </div>
                  <span class="product-price">{{ formatCurrency(item.precio_unitario) }}</span>
                </div>
                <div class="card-metrics">
                  <div class="metric">
                    <span class="metric-label">Inicial</span>
                    <span class="metric-value initial">{{ item.cantidad_inicial }}</span>
                  </div>
                  <div class="metric">
                    <span class="metric-label">Final</span>
                    <span class="metric-value final">{{ item.cantidad_final }}</span>
                  </div>
                  <div class="metric highlight">
                    <span class="metric-label">Vendidos</span>
                    <span class="metric-value sold">{{ item.cantidad_vendida }}</span>
                  </div>
                  <div class="metric total">
                    <span class="metric-label">Subtotal</span>
                    <span class="metric-value subtotal">{{ formatCurrency(item.subtotal) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';
import { useAdminStore } from '@/stores/admin';
import axios from 'axios';
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2';
// *** 1. IMPORTACIÓN DE LA CONSTANTE GLOBAL CON RUTA RELATIVA ***
import { API_BASE_URL } from '../config/api';
// *************************************************************

// Estado del componente
const adminStore = useAdminStore();
const isModalOpen = ref(false);
const currentProductIndex = ref(0);
const isInvoiceGenerated = ref(false);
const isViewingDetails = ref(false);
const products = ref([]);
const invoices = ref([]);
const displayedInvoice = ref({});
const loadingHistory = ref(false);
const searchQuery = ref('');
const router = useRouter(); 
// Eliminada: const API_BASE_URL = 'http://192.168.100.37:8000';
const isGenerating = ref(false);

// NUEVO: Estado para "Gastos Hormiga"
const isGastosHormigaStep = ref(false);
const gastosHormiga = ref([{ descripcion: '', monto: null }]);
const isGastosModalOpen = ref(false);
const tempGasto = ref({ descripcion: '', monto: null });
// NUEVO: Estado para el scroll infinito
const page = ref(1); 
const pageSize = 20;
const hasMore = ref(true);
const loadingMore = ref(false);
const formatInvoiceDate = (dateString) => {
  if (!dateString) return '';
  const date = parseISO(dateString);
  return format(date, "d 'de' MMMM 'de' yyyy", { locale: es });
};

// Función para formatear la hora (12 horas con AM/PM)
const formatInvoiceTime = (timeString) => {
  if (!timeString) return '';
  const date = parseISO(timeString);
  return format(date, 'hh:mm a', { 
    locale: es,
    timeZone: 'America/Bogota'  // ← AGREGAR ESTA LÍNEA
  });
};

// Función para fecha completa con día de la semana (solo en detalle)
const formatFullInvoiceDate = (dateString) => {
  if (!dateString) return '';
  const date = parseISO(dateString);
  return format(date, "EEEE, d 'de' MMMM 'de' yyyy", { locale: es });
};
// Propiedad computada para el producto actual
const currentProduct = computed(() => {
  return products.value[currentProductIndex.value];
});

// Propiedad computada para calcular la cantidad vendida
const calculatedSold = computed(() => {
  const product = currentProduct.value;
  if (product.finalQuantity === null || product.finalQuantity > product.cantidad || product.finalQuantity < 0) return 0;
  return product.cantidad - product.finalQuantity;
});

// Propiedad computada para calcular el subtotal
const calculatedSubtotal = computed(() => {
  const product = currentProduct.value;
  if (product.finalQuantity === null || product.finalQuantity > product.cantidad || product.finalQuantity < 0) return 0;
  return calculatedSold.value * product.precio;
});

// Propiedad computada para el total de ingresos de productos
const total_ingresos = computed(() => {
  return products.value.reduce((sum, p) => {
    const sold = p.finalQuantity !== null ? p.cantidad - p.finalQuantity : 0;
    return sum + (sold * p.precio);
  }, 0);
});

// NUEVO: Propiedades computadas para Gastos Hormiga y total neto
const totalGastosHormiga = computed(() => {
  return gastosHormiga.value.reduce((sum, gasto) => {
    return sum + (gasto.monto > 0 ? gasto.monto : 0);
  }, 0);
});
const openGastosModal = () => {
  tempGasto.value = { descripcion: '', monto: null };
  isGastosModalOpen.value = true;
};

const closeGastosModal = () => {
  isGastosModalOpen.value = false;
  tempGasto.value = { descripcion: '', monto: null };
};
const saveGastoFromModal = () => {
  if (tempGasto.value.descripcion && tempGasto.value.monto && tempGasto.value.monto > 0) {
    gastosHormiga.value.push({ ...tempGasto.value });
    closeGastosModal();
  } else {
    Swal.fire({
      title: 'Campos incompletos',
      text: 'Por favor completa la descripción y el monto del gasto.',
      icon: 'warning',
      confirmButtonText: 'Entendido',
      confirmButtonColor: '#ff69b4',
      background: '#1a1a1a',
      color: '#f8fafc',
    });
  }
};
const editGasto = (index) => {
  tempGasto.value = { ...gastosHormiga.value[index] };
  gastosHormiga.value.splice(index, 1);
  isGastosModalOpen.value = true;
};
const totalIngresosNetos = computed(() => {
  return total_ingresos.value - totalGastosHormiga.value;
});

// Propiedad computada para deshabilitar el botón "Siguiente"
const isNextDisabled = computed(() => {
  const product = currentProduct.value;
  // Ahora también valida que el campo no esté vacío (null o undefined)
  return product.finalQuantity === null || 
         product.finalQuantity === undefined || 
         product.finalQuantity === '' ||
         product.finalQuantity > product.cantidad || 
         product.finalQuantity < 0;
});

// Propiedad computada para filtrar las facturas
const filteredInvoices = computed(() => {
  if (!searchQuery.value) {
    return invoices.value;
  }
  const query = searchQuery.value.toLowerCase();
  return invoices.value.filter(invoice => {
    const invoiceDate = formatInvoiceDate(invoice.fecha).toLowerCase();
    const invoiceTime = formatInvoiceTime(invoice.hora).toLowerCase();
    return invoiceDate.includes(query) || invoiceTime.includes(query);
  });
});

// Observar cambios en el campo de búsqueda
watch(searchQuery, (newQuery) => {
  if (newQuery) {
    page.value = 1;
    hasMore.value = false;
  } else {
    page.value = 1;
    invoices.value = [];
    hasMore.value = true;
    fetchInvoices();
  }
});

// Métodos
const formatCurrency = (value, showSymbol = true) => {
  if (value === null || value === undefined || isNaN(value)) return '0';
  const formatter = new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  });
  const formattedValue = formatter.format(value);
  return showSymbol ? formattedValue : formattedValue.replace('$', '').trim();
};

const updateGastoMonto = (event, index) => {
  const value = event.target.value.replace(/\D/g, '');
  const numberValue = parseInt(value, 10);
  gastosHormiga.value[index].monto = isNaN(numberValue) ? null : numberValue;
};


// NUEVO: Métodos para Gastos Hormiga
const addGastoHormiga = () => {
  gastosHormiga.value.push({ descripcion: '', monto: null });
};

const removeGastoHormiga = (index) => {
  gastosHormiga.value.splice(index, 1);
};
const updateTempGastoMonto = (event) => {
  const value = event.target.value.replace(/\D/g, '');
  const numberValue = parseInt(value, 10);
  tempGasto.value.monto = isNaN(numberValue) ? null : numberValue;
};
const fetchProductsForInvoice = async () => {
  if (!adminStore.bar_id) return;
  try {
    const barId = adminStore.bar_id;
    // *** USO DE LA CONSTANTE GLOBAL ***
    const response = await axios.get(`${API_BASE_URL}/productos_por_bar2/${barId}`);
    products.value = response.data.map(p => ({ ...p, finalQuantity: null }));
  } catch (error) {
    console.error('Error al obtener los productos:', error);
    Swal.fire({
      title: 'Error',
      text: 'Error al cargar los productos. Por favor, inténtalo de nuevo.',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ff69b4',
      background: '#1a1a1a',
      color: '#f8fafc',
    });
  }
};

const fetchInvoices = async () => {
  if (!adminStore.id || !adminStore.bar_id || loadingMore.value || !hasMore.value) return;
  
  loadingMore.value = true;
  if (page.value === 1) {
    loadingHistory.value = true;
  }

  try {
    const barId = adminStore.bar_id;
    const adminId = adminStore.id;
    const skip = (page.value - 1) * pageSize;
    
    // *** USO DE LA CONSTANTE GLOBAL ***
    const response = await axios.get(`${API_BASE_URL}/facturas/administrador/${adminId}/bar/${barId}`, {
      params: { skip, limit: pageSize }
    });
    
    const newInvoices = response.data;
    if (newInvoices.length > 0) {
      invoices.value = [...invoices.value, ...newInvoices];
      page.value++;
    } else {
      hasMore.value = false;
    }
  } catch (error) {
    console.error('Error al obtener el historial de facturas:', error);
    Swal.fire({
      title: 'Error',
      text: 'Error al cargar el historial de facturas. Por favor, inténtalo de nuevo.',
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ff69b4',
      background: '#1a1a1a',
      color: '#f8fafc',
    });
  } finally {
    loadingMore.value = false;
    loadingHistory.value = false;
  }
};

const handleScroll = (event) => {
  const { scrollTop, scrollHeight, clientHeight } = event.target;
  const bottomOfWindow = scrollTop + clientHeight >= scrollHeight - 50; 
  if (bottomOfWindow && !loadingMore.value && hasMore.value && !searchQuery.value) {
    fetchInvoices();
  }
};

const startInvoice = async () => {
  await fetchProductsForInvoice();
  if (products.value.length === 0) {
    Swal.fire({
      title: 'No hay productos',
      text: 'No hay productos disponibles para generar una factura.',
      icon: 'info',
      confirmButtonText: 'Entendido',
      confirmButtonColor: '#ff69b4',
      background: '#1a1a1a',
      color: '#f8fafc',
    });
    return;
  }
  currentProductIndex.value = 0;
  isInvoiceGenerated.value = false;
  isViewingDetails.value = false;
  isGastosHormigaStep.value = false;
  gastosHormiga.value = [{ descripcion: '', monto: null }]; // Reiniciar gastos hormiga
  isModalOpen.value = true;
};

const generateInvoice = async () => {
  // 1. Mostrar confirmación con SweetAlert2
  const result = await Swal.fire({
    title: '¿Estás seguro de generar esta factura?',
    text: 'Una vez generada, no podrás modificarla ni volver atrás.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, generar factura',
    cancelButtonText: 'Cancelar',
    reverseButtons: true, // hace que el botón rojo (confirm) esté a la derecha
    confirmButtonColor: '#ff69b4',
    cancelButtonColor: '#6b7280',
    background: '#1a1a1a',
    color: '#f8fafc',
  });

  // 2. Si el usuario cancela, no hacemos nada
  if (!result.isConfirmed) {
    return;
  }

  // 3. Si confirma, procedemos con la generación
  isGenerating.value = true;

  // Mapear los gastos para que coincidan con el esquema de FastAPI
  const gastosParaEnvio = gastosHormiga.value
    .filter(g => g.descripcion && g.monto !== null && g.monto > 0)
    .map(gasto => ({
      nombre: gasto.descripcion,
      precio: gasto.monto
    }));

  const invoicePayload = {
    bar_id: adminStore.bar_id,
    administrador_id: adminStore.id,
    productos: products.value.map(p => ({
      producto_id: p.id,
      cantidad_final: p.finalQuantity,
    })),
    gastos_hormiga: gastosParaEnvio,
  };

  try {
    const response = await axios.post(`${API_BASE_URL}/generar_factura`, invoicePayload);

    displayedInvoice.value = {
      ...response.data,
      detalles_factura: response.data.detalles_factura.map(detail => {
        const originalProduct = products.value.find(p => p.id === detail.producto_id);
        return {
          ...detail,
          imagen_producto: originalProduct ? originalProduct.imagen : null
        };
      }),
      gastos: gastosParaEnvio,
    };

    isInvoiceGenerated.value = true;

    await Swal.fire({
      title: '¡Factura generada!',
      text: 'La factura diaria se ha guardado correctamente.',
      icon: 'success',
      confirmButtonText: 'Entendido',
      confirmButtonColor: '#ff69b4',
      background: '#1a1a1a',
      color: '#f8fafc',
    });

    closeModal();
    invoices.value = [];
    page.value = 1;
    hasMore.value = true;
    await fetchInvoices();

  } catch (error) {
    console.error('Error al generar la factura:', error);
    const errorMessage = error.response?.data?.detail || 'Hubo un error inesperado al generar la factura.';
    Swal.fire({
      title: 'Error',
      text: `Error al generar la factura: ${errorMessage}`,
      icon: 'error',
      confirmButtonText: 'Aceptar',
      confirmButtonColor: '#ff69b4',
      background: '#1a1a1a',
      color: '#f8fafc',
    });
  } finally {
    isGenerating.value = false;
  }
};

const viewInvoiceDetails = (invoice) => {
  // Cuando se ve una factura del historial, los gastos ya vienen del backend
  // en la propiedad `gastos`, así que los asignamos directamente.
  displayedInvoice.value = {
    ...invoice,
    gastos: invoice.gastos,
  };
  isViewingDetails.value = true;
  isInvoiceGenerated.value = true;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  isInvoiceGenerated.value = false;
  isViewingDetails.value = false;
  isGastosHormigaStep.value = false;
};

// Navegación
const nextProduct = () => {
  if (currentProductIndex.value < products.value.length - 1) {
    currentProductIndex.value++;
  } else {
    // Cuando es el último producto, pasar a la pantalla de gastos hormiga
    isGastosHormigaStep.value = true;
  }
};

const previousProduct = () => {
  if (isGastosHormigaStep.value) {
    isGastosHormigaStep.value = false;
  } else if (currentProductIndex.value > 0) {
    currentProductIndex.value--;
  }
};

const goBack = () => {
  router.go(-1);
};

onMounted(() => {
  fetchInvoices();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;600;700&display=swap');

/* ================================================================================================= */
/* --- ESTILOS BASE Y CONTENEDOR PRINCIPAL --- */
/* ================================================================================================= */

.invoice-container {
  min-height: 100vh;
  background-color: #0d0d0d;
  background-image: 
    radial-gradient(at 40% 20%, rgba(255, 105, 180, 0.1) 0px, transparent 50%),
    radial-gradient(at 80% 0%, rgba(255, 105, 180, 0.1) 0px, transparent 50%),
    radial-gradient(at 0% 50%, rgba(255, 105, 180, 0.1) 0px, transparent 50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Inter', sans-serif;
  color: #f8fafc;
  padding: 0 0.5rem;
}

/* ================================================================================================= */
/* --- HEADER PRINCIPAL --- */
/* ================================================================================================= */

.app-header {
  position: sticky;
  top: 0;
  width: 100%;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #0d0d0d;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 40;
}

.header-content {
  display: flex;
  align-items: flex-end;
  gap: 0.75rem;
}

.header-title {
  font-size: 1.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  line-height: 1;
}

.header-subtitle {
  font-size: 0.7rem;
  font-weight: 500;
  color: #a3a3a3;
  margin: 0;
  padding-bottom: 0.25rem;
}

.back-button {
  background: transparent;
  color: #f8fafc;
  border: 1px solid white;
  padding: 0.5rem 1rem;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.8rem;
}

.back-button:hover {
  color: #ff69b4;
  border-color: #ff69b4;
  transform: translateY(-1px);
}

/* ================================================================================================= */
/* --- CONTENIDO PRINCIPAL --- */
/* ================================================================================================= */

.main-content {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 0;
  animation: fadeInUp 0.8s ease-out;
}

.header-section {
  text-align: center;
  margin-bottom: 2rem;
}

.main-title {
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.subtitle {
  font-size: 0.9rem;
  color: #a3a3a3;
  font-weight: 400;
  max-width: 600px;
  line-height: 1.4;
}

.primary-button {
  position: relative;
  padding: 0.8rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: 'Poppins', sans-serif;
  letter-spacing: 0.5px;
  color: white;
  background: transparent;
  border: none;
  border-radius: 50px;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  z-index: 1;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.3s ease;
}

.primary-button::before {
  content: "";
  position: absolute;
  inset: 0;
  padding: 2px;
  border-radius: 50px;
  background: linear-gradient(270deg, #ff69b4, #87cefa, #ff69b4);
  background-size: 400% 400%;
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  animation: borderFlow 6s ease infinite;
}

.primary-button::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 50px;
  background: linear-gradient(270deg, #ff00cc, #3333ff, #00ff99, #ffcc00);
  background-size: 400% 400%;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.5s ease;
}

.primary-button:hover::after {
  opacity: 1;
  animation: waterFlow 5s ease infinite;
}

@keyframes borderFlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes waterFlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.primary-button:hover {
  transform: scale(1.02);
  box-shadow: 0 0 15px rgba(255, 105, 180, 0.4);
  color: #000;
}

.button-icon {
  font-size: 1.2rem;
}

/* ================================================================================================= */
/* --- SECCIÓN HISTORIAL --- */
/* ================================================================================================= */

.history-section {
  margin-top: 2rem;
  width: 100%;
  max-width: 800px;
  background: #1a1a1a;
  border-radius: 1rem;
  border: 1px solid #333333;
  padding: 1rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  animation: fadeInUp 0.8s ease-out 0.4s both;
}

.history-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #f8fafc;
  margin-bottom: 1rem;
  text-align: center;
}

.search-container {
  position: relative;
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #333333;
  border-radius: 0.8rem;
  padding: 0.8rem 1rem;
  padding-left: 2.5rem;
  color: #f8fafc;
  font-size: 0.85rem;
  transition: all 0.2s;
}

.search-input::placeholder {
  color: #a3a3a3;
}

.search-input:focus {
  outline: none;
  border-color: #ff69b4;
  box-shadow: 0 0 0 2px rgba(255, 105, 180, 0.1);
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a3a3a3;
  pointer-events: none;
  font-size: 0.9rem;
}

.loading-message, .no-invoices {
  text-align: center;
  color: #a3a3a3;
  font-size: 0.85rem;
  padding: 1.5rem;
}

.invoices-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 400px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #ff69b4 #1a1a1a;
}

.invoice-item {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #333333;
  border-radius: 0.8rem;
  padding: 0.8rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
}

.invoice-item:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.invoice-info-header {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.invoice-date {
  font-size: 0.8rem;
  font-weight: 600;
  color: #f8fafc;
}

.invoice-time {
  font-size: 0.7rem;
  color: #a3a3a3;
}

.invoice-total {
  font-size: 0.75rem;
  font-weight: 500;
  color: #a3a3a3;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.2rem;
}

.total-amount {
  font-size: 0.9rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.loading-more {
  text-align: center;
  color: #a3a3a3;
  font-size: 0.8rem;
  padding: 1rem;
}

/* ================================================================================================= */
/* --- MODAL --- */
/* ================================================================================================= */

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem;
  z-index: 50;
  animation: fadeIn 0.3s ease-out;
}

.modal-container {
  background: #1a1a1a;
  border-radius: 1rem;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
  border: 1px solid #333333;
  max-width: 500px;
  width: 100%;
  max-height: 95vh;
  overflow-y: auto;
  position: relative;
  animation: modalSlideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-close-button {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: transparent;
  border: none;
  cursor: pointer;
  color: #a3a3a3;
  font-size: 1.2rem;
  transition: color 0.2s;
  z-index: 10;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close-button:hover {
  color: #ff69b4;
}

.product-section, .gastos-hormiga-section, .invoice-view {
  padding: 1rem;
}

/* ================================================================================================= */
/* --- PROGRESS BAR --- */
/* ================================================================================================= */

.progress-container {
  margin-bottom: 1.5rem;
}

.progress-bar {
  width: 100%;
  height: 0.4rem;
  background: #333333;
  border-radius: 0.2rem;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  border-radius: 0.2rem;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  color: #a3a3a3;
  font-weight: 500;
  font-size: 0.8rem;
}

/* ================================================================================================= */
/* --- PRODUCT CARD --- */
/* ================================================================================================= */

.product-card {
  background: #1a1a1a;
  border-radius: 0.8rem;
  padding: 1rem;
  border: 1px solid #333333;
}

.product-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.product-image-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.25);
  border: 2px solid #ff69b4;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-name {
  font-size: 1.3rem;
  font-weight: 700;
  text-align: center;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
  line-height: 1.2;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.8rem 0.5rem;
  background: #2a2a2a;
  border-radius: 0.6rem;
  border: 1px solid #333333;
  text-align: center;
}

.detail-label {
  color: #a3a3a3;
  font-weight: 500;
  font-size: 0.7rem;
  margin-bottom: 0.2rem;
}

.detail-value {
  font-weight: 600;
  color: #f8fafc;
  font-size: 0.9rem;
}

.detail-value.price {
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  font-size: 1rem;
}

.input-section {
  margin-top: 1rem;
}

.input-label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #f8fafc;
  text-align: center;
  font-size: 0.85rem;
}

.input-wrapper {
  position: relative;
}

.quantity-input {
  width: 100%;
  background: #2a2a2a;
  border: 2px solid #333333;
  border-radius: 0.6rem;
  padding: 0.8rem;
  color: #f8fafc;
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
  transition: all 0.2s;
  -moz-appearance: textfield;
}

.quantity-input::-webkit-outer-spin-button,
.quantity-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

.quantity-input:focus {
  outline: none;
  border-color: #ff69b4;
  box-shadow: 0 0 0 2px rgba(255, 105, 180, 0.1);
}

.error-text {
  color: #ef4444;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  justify-content: center;
}

/* ================================================================================================= */
/* --- PRODUCT SUMMARY --- */
/* ================================================================================================= */

.product-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.summary-item {
  padding: 1rem 0.5rem;
  border-radius: 0.8rem;
  text-align: center;
  border: 1px solid #333333;
}

.summary-item.sold {
  background: rgba(255, 105, 180, 0.1);
}

.summary-item.subtotal {
  background: rgba(236, 72, 153, 0.1);
}

.summary-label {
  display: block;
  color: #a3a3a3;
  font-size: 0.7rem;
  font-weight: 500;
  margin-bottom: 0.3rem;
}

.summary-value {
  display: block;
  font-size: 1.1rem;
  font-weight: 700;
  color: #f8fafc;
}

/* ================================================================================================= */
/* --- NAVIGATION --- */
/* ================================================================================================= */

.navigation-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #333333;
  gap: 0.5rem;
}

.nav-button {
background: rgba(255, 255, 255, 0.05);
  border: 1px solid #333333;
  border-radius: 0.6rem;
  padding: 0.6rem 1rem;
  color: #f8fafc;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.2s;
  backdrop-filter: blur(10px);
  font-size: 0.8rem;
}

.nav-button:not(:disabled):hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.nav-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.nav-button.primary-nav {
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  border: 1px solid #ff1493;
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
  position: relative;
  overflow: hidden;
}

.nav-button.primary-nav::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.nav-button.primary-nav:not(:disabled):hover::before {
  left: 100%;
}

.nav-button.primary-nav:not(:disabled):hover {
  background: linear-gradient(135deg, #ff1493 0%, #ff69b4 100%);
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.5);
  transform: translateY(-2px);
}

.nav-button.primary-nav:disabled {
  background: #333333;
  border-color: #555555;
  color: #a3a3a3;
  box-shadow: none;
}
.nav-icon {
  font-size: 1rem;
}

.nav-dots {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  justify-content: center;
}

.dot {
  width: 0.4rem;
  height: 0.4rem;
  border-radius: 50%;
  background: #333333;
  transition: all 0.2s;
}

.dot.active {
  background: #ff69b4;
  transform: scale(1.2);
}

.action-buttons {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #333333;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.generate-button {
  width: 100%;
  background: #ff69b4;
  border: 1px solid #ff1493;
  border-radius: 0.8rem;
  padding: 1rem;
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.2);
}

.generate-button:not(:disabled):hover {
  background: #ff1493;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.3);
}

.generate-button:disabled {
  background: #333333;
  border-color: #555555;
  color: #a3a3a3;
  opacity: 0.7;
  cursor: not-allowed;
  box-shadow: none;
}

.generate-icon {
  font-size: 1rem;
}

.cancel-button {
  width: 100%;
  background: #2a2a2a;
  border: 1px solid #333333;
  border-radius: 0.8rem;
  padding: 1rem;
  color: #f8fafc;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s;
}

.cancel-button:hover {
  background: #333333;
  transform: translateY(-1px);
}

.cancel-icon {
  font-size: 1rem;
}

/* ================================================================================================= */
/* --- GASTOS HORMIGA SECTION --- */
/* ================================================================================================= */

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  text-align: center;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  text-align: center;
  color: #a3a3a3;
  margin-bottom: 1.5rem;
  font-size: 0.8rem;
}

.gastos-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.gasto-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #2a2a2a;
  border: 1px solid #333333;
  border-radius: 0.8rem;
  padding: 0.8rem;
  position: relative;
}

.gasto-inputs {
  display: flex;
  gap: 0.5rem;
  flex-grow: 1;
}

.gasto-input {
  flex-grow: 1;
  background: transparent;
  border: none;
  color: #f8fafc;
  font-size: 0.8rem;
  padding: 0.4rem 0.5rem;
  border-bottom: 1px solid #333333;
  transition: all 0.2s;
}

.gasto-input::placeholder {
  color: #a3a3a3;
  font-size: 0.75rem;
}

.gasto-input:focus {
  outline: none;
  border-bottom-color: #ff69b4;
}

.price-input {
  width: 80px;
}

.remove-gasto-button {
  background: #ff1493;
  border: none;
  color: white;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 1.2rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  flex-shrink: 0;
}

.remove-gasto-button:hover {
  background: #ff4d9c;
  transform: scale(1.05);
}

.add-gasto-button {
  width: 100%;
  background: rgba(255, 105, 180, 0.1);
  border: 1px solid #ff69b4;
  border-radius: 0.8rem;
  padding: 0.8rem;
  color: #ff69b4;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.8rem;
}

.add-gasto-button:hover {
  background: rgba(255, 105, 180, 0.2);
  transform: translateY(-1px);
}

.gastos-summary {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #333333;
}

.gastos-summary .summary-item {
  background: #2a2a2a;
  border: 1px solid #333333;
  border-radius: 0.8rem;
  padding: 1rem;
  text-align: center;
}

.gastos-summary .summary-item.final-income {
  background: #2a2a2a;
  border-color: #ff69b4;
}

.gastos-summary .summary-item.final-income .summary-value {
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 1.3rem;
}

.gastos-summary .summary-item .summary-value.ingresos {
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.action-buttons-gastos {
  margin-top: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* ================================================================================================= */
/* --- INVOICE VIEW --- */
/* ================================================================================================= */

.invoice-view {
  padding: 1rem;
}

.invoice-header {
  margin-bottom: 1.5rem;
}

.invoice-title-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.invoice-title {
  font-size: 1.6rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.invoice-badge {
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 1.5rem;
  font-size: 0.7rem;
  font-weight: 600;
  white-space: nowrap;
}

.invoice-info {
  margin-bottom: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.info-item {
  background: #2a2a2a;
  border: 1px solid #333333;
  border-radius: 0.8rem;
  padding: 0.6rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
  text-align: center;
}

.info-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.info-content {
  flex: 1;
}

.info-label {
  display: block;
  color: #a3a3a3;
  font-size: 0.65rem;
  font-weight: 500;
  line-height: 1.2;
}

.info-value {
  display: block;
  color: #f8fafc;
  font-weight: 600;
  margin-top: 0.1rem;
  font-size: 0.75rem;
  line-height: 1.2;
}

/* Info especial para "Generado por" - ocupa toda la fila */
.info-item.generated-by {
  grid-column: 1 / -1;
}

.total-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
  margin-top: 1rem;
}

.total-card {
  background: #1a1a1a;
  border: 1px solid #333333;
  border-radius: 1rem;
  padding: 0.8rem;
  text-align: center;
}

.total-card.ingresos-card {
  background-color: rgba(255, 105, 180, 0.1);
  border-color: #ff69b4;
}

.total-card.gastos-card {
  background-color: rgba(239, 68, 68, 0.1);
  border-color: #ef4444;
}

.total-card.netos-card {
  grid-column: 1 / -1;
  background-color: #0d0d0d;
  border-color: #fff;
}

.total-card .total-label {
  color: #a3a3a3;
  font-size: 0.7rem;
  margin-bottom: 0.3rem;
  display: block;
}

.total-card .total-amount {
  font-size: 1.2rem;
  font-weight: 800;
  line-height: 1;
}

.total-card.ingresos-card .total-amount {
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.total-card.gastos-card .total-amount {
  color: #ef4444;
}

.total-card.netos-card .total-amount {
  color: white;
  font-size: 1.4rem;
}

/* ================================================================================================= */
/* --- GASTOS SUMMARY VIEW --- */
/* ================================================================================================= */

.gastos-summary-view {
  margin-top: 1.5rem;
}

.summary-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #f8fafc;
}

.gastos-list-view {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.gasto-item-view {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0.8rem;
  background: #2a2a2a;
  border: 1px solid #333333;
  border-radius: 0.6rem;
}

.gasto-description {
  font-weight: 500;
  color: #a3a3a3;
  font-size: 0.8rem;
}

.gasto-amount {
  font-weight: 600;
  color: #ef4444;
  font-size: 0.8rem;
}

/* ================================================================================================= */
/* --- PRODUCTS SUMMARY --- */
/* ================================================================================================= */

.products-summary {
  margin-top: 1.5rem;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 350px;
  overflow-y: auto;
  padding-right: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: #ff69b4 #1a1a1a;
}

.product-summary-card {
  background: #2a2a2a;
  border: 1px solid #333333;
  border-radius: 0.8rem;
  padding: 0.8rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  gap: 0.5rem;
}

.product-summary-name-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  min-width: 0;
}

.product-summary-image {
  width: 35px;
  height: 35px;
  object-fit: cover;
  border-radius: 0.4rem;
  border: 1px solid #ff69b4;
  flex-shrink: 0;
}

.product-summary-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #f8fafc;
  margin: 0;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  color: #f8fafc;
  font-weight: 600;
  font-size: 0.75rem;
  white-space: nowrap;
  flex-shrink: 0;
}

.card-metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.4rem;
}

.metric {
  text-align: center;
  padding: 0.5rem 0.2rem;
  border-radius: 0.4rem;
  background: #333333;
}

.metric.highlight {
  background: rgba(255, 105, 180, 0.1);
  border: 1px solid rgba(255, 105, 180, 0.2);
}

.metric.total {
  background: rgba(255, 105, 180, 0.1);
  border: 1px solid rgba(255, 105, 180, 0.2);
}

.metric-label {
  display: block;
  color: #a3a3a3;
  font-size: 0.6rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.2rem;
  line-height: 1;
}

.metric-value {
  display: block;
  font-weight: 700;
  font-size: 0.8rem;
  color: #f8fafc;
  line-height: 1;
}

.metric-value.initial {
  color: #a3a3a3;
}

.metric-value.final {
  color: #f8fafc;
}

.metric-value.sold {
  color: #ff69b4;
}

.metric-value.subtotal {
  color: #ff1493;
}

/* ================================================================================================= */
/* --- ANIMACIONES --- */
/* ================================================================================================= */

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes modalSlideUp {
  from { opacity: 0; transform: translateY(30px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* ================================================================================================= */
/* --- RESPONSIVE BREAKPOINTS --- */
/* ================================================================================================= */

/* Tablets (768px and up) */
@media (min-width: 768px) {
  .invoice-container {
    padding: 0 1rem;
  }
  
  .app-header {
    padding: 1.5rem 2rem;
  }
  
  .header-title {
    font-size: 2.2rem;
  }
  
  .header-subtitle {
    font-size: 0.8rem;
  }
  
  .main-title {
    font-size: 3.5rem;
  }
  
  .subtitle {
    font-size: 1.1rem;
  }
  
  .primary-button {
    padding: 1rem 2rem;
    font-size: 1rem;
    gap: 0.75rem;
  }
  
  .button-icon {
    font-size: 1.4rem;
  }
  
  .history-section {
    padding: 1.5rem;
  }
  
  .history-title {
    font-size: 1.5rem;
  }
  
  .search-input {
    padding: 1rem 1.5rem;
    padding-left: 3rem;
    font-size: 0.9rem;
  }
  
  .search-icon {
    left: 1.2rem;
  }
  
  .invoice-item {
    padding: 1rem 1.2rem;
  }
  
  .invoice-date {
    font-size: 0.9rem;
  }
  
  .invoice-time {
    font-size: 0.8rem;
  }
  
  .invoice-total {
    font-size: 0.85rem;
  }
  
  .total-amount {
    font-size: 1.1rem;
  }
  
  .modal-container {
    max-width: 600px;
  }
  
  .product-section, .gastos-hormiga-section, .invoice-view {
    padding: 1.5rem;
  }
  
  .product-image-wrapper {
    width: 100px;
    height: 100px;
  }
  
  .product-name {
    font-size: 1.6rem;
  }
  
  .detail-item {
    padding: 1rem;
  }
  
  .detail-value.price {
    font-size: 1.1rem;
  }
  
  .summary-value {
    font-size: 1.3rem;
  }
  
  .nav-button {
    padding: 0.8rem 1.2rem;
    font-size: 0.9rem;
  }
  
  .section-title {
    font-size: 1.8rem;
  }
  
  .gasto-input {
    font-size: 0.9rem;
    padding: 0.5rem 0.6rem;
  }
  
  .price-input {
    width: 100px;
  }
  
  .remove-gasto-button {
    width: 32px;
    height: 32px;
  }
  
  .gastos-summary {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  }
  
  .gastos-summary .summary-item.final-income .summary-value {
    font-size: 1.6rem;
  }
  
  .invoice-title {
    font-size: 2rem;
  }
  
  .invoice-badge {
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
  }
  
  .info-item {
    padding: 0.8rem;
  }
  
  .info-icon {
    font-size: 1.2rem;
  }
  
  .info-label {
    font-size: 0.75rem;
  }
  
  .info-value {
    font-size: 0.85rem;
  }
  
  .total-section {
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 0.75rem;
  }
  
  .total-card {
    padding: 1.2rem;
  }
  
  .total-card .total-label {
    font-size: 0.8rem;
  }
  
  .total-card .total-amount {
    font-size: 1.5rem;
  }
  
  .total-card.netos-card .total-amount {
    font-size: 1.8rem;
  }
  
  .product-summary-image {
    width: 45px;
    height: 45px;
  }
  
  .product-summary-name {
    font-size: 1rem;
  }
  
  .card-metrics {
    grid-template-columns: repeat(4, 1fr);
    gap: 0.6rem;
  }
  
  .metric {
    padding: 0.7rem 0.4rem;
  }
  
  .metric-label {
    font-size: 0.65rem;
  }
  
  .metric-value {
    font-size: 0.9rem;
  }
}

/* Desktop (1024px and up) */
@media (min-width: 1024px) {
  .main-title {
    font-size: 4.5rem;
  }
  
  .subtitle {
    font-size: 1.25rem;
  }
  
  .primary-button {
    padding: 1.2rem 2.5rem;
    font-size: 1.1rem;
  }
  
  .history-section {
    padding: 2rem;
  }
  
  .invoice-item {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  
  .invoice-total {
    align-items: flex-end;
  }
  
  .modal-container {
    max-width: 700px;
  }
  
  .product-section, .gastos-hormiga-section, .invoice-view {
    padding: 2rem;
  }
  
  .product-image-wrapper {
    width: 120px;
    height: 120px;
  }
  
  .product-name {
    font-size: 2rem;
  }
  
  .detail-row {
    grid-template-columns: 1fr 1fr;
  }
  
  .product-summary {
    grid-template-columns: 1fr 1fr;
  }
  
  .navigation-section {
    flex-direction: row;
    justify-content: space-between;
  }
  
  .nav-dots {
    order: unset;
    width: auto;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .gasto-inputs {
    flex-direction: row;
    gap: 1rem;
  }
  
  .price-input {
    width: 120px;
  }
  
  .invoice-title {
    font-size: 2.5rem;
  }
  
  .info-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  }
  
  .total-section {
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  }
  
  .total-card.netos-card {
    grid-column: unset;
  }
  
  .card-header {
    flex-direction: row;
    align-items: center;
  }
  
  .product-summary-name {
    font-size: 1.1rem;
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
  }
}

/* Extra Mobile Adjustments (480px and below) */
@media (max-width: 480px) {
  .app-header {
    padding: 0.75rem;
  }
  
  .header-content {
    align-items: center;
    gap: 0.5rem;
  }
  
  .header-title {
    font-size: 1.5rem;
  }
  
  .header-subtitle {
    font-size: 0.65rem;
  }
  
  .back-button {
    padding: 0.4rem 0.8rem;
    font-size: 0.75rem;
  }
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .subtitle {
    font-size: 0.8rem;
  }
  
  .primary-button {
    padding: 0.7rem 1.2rem;
    font-size: 0.8rem;
    gap: 0.4rem;
  }
  
  .button-icon {
    font-size: 1rem;
  }
  
  .invoice-item {
    padding: 0.6rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.4rem;
  }
  
  .invoice-info-header {
    width: 100%;
  }
  
  .invoice-total {
    width: 100%;
    align-items: flex-start;
    font-size: 0.7rem;
  }
  
  .total-amount {
    font-size: 0.85rem;
  }
  
  .product-image-wrapper {
    width: 70px;
    height: 70px;
  }
  
  .product-name {
    font-size: 1.1rem;
  }
  
  .detail-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .detail-item {
    padding: 0.6rem 0.4rem;
  }
  
  .detail-label {
    font-size: 0.65rem;
  }
  
  .detail-value {
    font-size: 0.8rem;
  }
  
  .product-summary {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .navigation-section {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.75rem;
  }
  
  .nav-dots {
    order: 3;
    width: 100%;
    justify-content: center;
  }
  
  .nav-button.prev { 
    order: 1; 
    font-size: 0.75rem;
    padding: 0.5rem 0.8rem;
  }
  
  .nav-button.next { 
    order: 2; 
    font-size: 0.75rem;
    padding: 0.5rem 0.8rem;
  }
  
  .section-title {
    font-size: 1.3rem;
  }
  
  .section-subtitle {
    font-size: 0.75rem;
  }
  
  .gasto-item {
    padding: 0.6rem;
    position: relative;
  }
  
  .gasto-inputs {
    flex-direction: column;
    gap: 0.5rem;
    padding-right: 35px;
  }
  
  .remove-gasto-button {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    width: 24px;
    height: 24px;
    font-size: 1rem;
  }
  
  .price-input {
    width: 100%;
  }
  
  .gastos-summary .summary-item.final-income .summary-value {
    font-size: 1.2rem;
  }
  
  .invoice-title {
    font-size: 1.4rem;
  }
  
  .invoice-badge {
    padding: 0.25rem 0.6rem;
    font-size: 0.65rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
    gap: 0.4rem;
  }
  
  .info-item {
    padding: 0.5rem;
    flex-direction: row;
    text-align: left;
  }
  
  .info-icon {
    font-size: 0.9rem;
  }
  
  .info-label {
    font-size: 0.6rem;
  }
  
  .info-value {
    font-size: 0.7rem;
  }
  
  .total-section {
    grid-template-columns: 1fr;
    gap: 0.4rem;
  }
  
  .total-card {
    padding: 0.6rem;
  }
  
  .total-card .total-label {
    font-size: 0.65rem;
  }
  
  .total-card .total-amount {
    font-size: 1rem;
  }
  
  .total-card.netos-card .total-amount {
    font-size: 1.2rem;
  }
  
  .product-summary-card {
    padding: 0.6rem;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.4rem;
  }
  
  .product-summary-image {
    width: 30px;
    height: 30px;
  }
  
  .product-summary-name {
    font-size: 0.85rem;
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
  }
  
  .product-price {
    font-size: 0.7rem;
  }
  
  .card-metrics {
    grid-template-columns: 2fr 2fr 2fr 3fr;
    gap: 0.3rem;
  }
  
  .metric {
    padding: 0.4rem 0.2rem;
  }
  
  .metric-label {
    font-size: 0.55rem;
    margin-bottom: 0.15rem;
  }
  
  .metric-value {
    font-size: 0.7rem;
  }
  
  .gasto-item-view {
    padding: 0.5rem 0.6rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.3rem;
  }
  
  .gasto-description, .gasto-amount {
    font-size: 0.75rem;
  }
}
/* ================================================================================================= */
/* --- GASTOS HORMIGA - NUEVA INTERFAZ CON MODAL --- */
/* ================================================================================================= */

.gastos-added-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
  max-height: 300px;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.gasto-added-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #2a2a2a;
  border: 1px solid #333333;
  border-radius: 0.8rem;
  padding: 0.8rem;
  transition: all 0.2s;
}

.gasto-added-item:hover {
  background: #333333;
  transform: translateX(2px);
}

.gasto-added-info {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  flex: 1;
}

.gasto-added-desc {
  font-weight: 600;
  color: #f8fafc;
  font-size: 0.85rem;
}

.gasto-added-price {
  font-weight: 700;
  color: #ef4444;
  font-size: 0.9rem;
}

.gasto-added-actions {
  display: flex;
  gap: 0.4rem;
}

.edit-gasto-btn,
.remove-gasto-btn-mini {
  background: transparent;
  border: none;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-size: 1rem;
}

.edit-gasto-btn:hover {
  background: rgba(255, 105, 180, 0.2);
  transform: scale(1.1);
}

.remove-gasto-btn-mini:hover {
  background: rgba(239, 68, 68, 0.2);
  transform: scale(1.1);
}

.no-gastos-message {
  text-align: center;
  color: #a3a3a3;
  padding: 2rem 1rem;
  background: #2a2a2a;
  border-radius: 0.8rem;
  border: 1px dashed #333333;
  margin-bottom: 1rem;
  font-size: 0.85rem;
}

.add-gasto-button-main {
  width: 100%;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  border: none;
  border-radius: 0.8rem;
  padding: 1rem;
  color: white;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
  margin-bottom: 1.5rem;
}

.add-gasto-button-main:hover {
  background: linear-gradient(135deg, #ff1493 0%, #ff69b4 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.5);
}

.add-icon {
  font-size: 1.2rem;
}

/* Modal de gastos */
.gastos-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  z-index: 100;
  animation: fadeIn 0.3s ease-out;
}

.gastos-modal-content {
  background: #1a1a1a;
  border-radius: 1rem;
  border: 1px solid #333333;
  padding: 1.5rem;
  max-width: 400px;
  width: 100%;
  position: relative;
  animation: modalSlideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
}

.gastos-modal-close {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: transparent;
  border: none;
  color: #a3a3a3;
  cursor: pointer;
  font-size: 1.2rem;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.gastos-modal-close:hover {
  color: #ff69b4;
}

.gastos-modal-title {
  font-size: 1.3rem;
  font-weight: 700;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1.5rem;
  text-align: center;
}

.gastos-modal-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 600;
  color: #f8fafc;
  font-size: 0.85rem;
}

.form-input {
  background: #2a2a2a;
  border: 2px solid #333333;
  border-radius: 0.6rem;
  padding: 0.8rem;
  color: #f8fafc;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.form-input::placeholder {
  color: #666666;
}

.form-input:focus {
  outline: none;
  border-color: #ff69b4;
  box-shadow: 0 0 0 2px rgba(255, 105, 180, 0.1);
}

.price-input-modal {
  font-weight: 600;
}

.save-gasto-button {
  width: 100%;
  background: linear-gradient(135deg, #ff69b4 0%, #ff1493 100%);
  border: none;
  border-radius: 0.8rem;
  padding: 1rem;
  color: white;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.3s;
  font-size: 0.9rem;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
}

.save-gasto-button:hover {
  background: linear-gradient(135deg, #ff1493 0%, #ff69b4 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.5);
}
</style>