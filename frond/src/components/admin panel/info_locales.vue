<template>
  <div class="panel-de-control">
    <!-- Loader global -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Cargando datos del bar ID: {{ barId || 'detectando...' }}</p>
    </div>

    <!-- Error general -->
    <div v-if="error" class="error-message">
      <p>⚠️ {{ error }}</p>
      <button @click="loadData" class="btn-retry">Reintentar</button>
    </div>

    <!-- Modal de imagen -->
    <div v-if="imageModalOpen" class="image-modal" @click="closeImageModal">
      <div class="modal-content" @click.stop>
        <img :src="modalImageSrc" alt="Imagen ampliada" class="modal-image" />
        <button @click="closeImageModal" class="modal-close">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>

    <!-- Header fijo con navegación integrada -->
    <header class="header">
      <div class="header-left">
        <h1 class="header-title">
          <span class="pink-text">P</span>anel de <span class="cyan-text">G</span>estión
          <small v-if="barId" class="bar-id-info">Bar ID: {{ barId }}</small>
        </h1>
      </div>
      
      <nav class="header-nav">
        <button 
          @click="setView('administradores')" 
          :class="['nav-button', { active: currentView === 'administradores' }]"
        >
          <i class="fas fa-user-shield"></i> 
          <span class="nav-text">Admins</span>
        </button>
        <button 
          @click="setView('productos')" 
          :class="['nav-button', { active: currentView === 'productos' }]"
        >
          <i class="fas fa-boxes"></i> 
          <span class="nav-text">Productos</span>
        </button>
      </nav>

      <button @click="goBack" class="btn-volver">
        <i class="fas fa-arrow-left"></i> 
        <span class="btn-text">Volver</span>
      </button>
    </header>

    <!-- Contenido -->
    <main class="content">
      <!-- ADMINISTRADORES -->
      <div v-if="currentView === 'administradores'" class="list-section">
        <div class="section-header">
          <h2 class="section-title pink-gradient">
            <i class="fas fa-user-shield"></i> 
            <span class="title-text">Gestión de Administradores</span>
          </h2>
        </div>

        <!-- Buscador Administradores -->
        <div class="search-container">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input 
              v-model="searchAdmin" 
              type="text" 
              placeholder="Buscar por nombre, correo o documento..."
              class="search-input"
            />
            <button 
              v-if="searchAdmin" 
              @click="searchAdmin = ''"
              class="clear-btn"
            >
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Foto</th>
                <th>Nombre</th>
                <th class="hide-mobile">Correo</th>
                <th class="hide-mobile">Documento</th>
                <th class="hide-mobile">Teléfono</th>
                <th class="hide-tablet">Agregado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="admin in filteredAdministradores" :key="admin.id">
                <td>
                  <div class="image-zoom-wrapper">
                    <img 
                      :src="admin.foto" 
                      alt="Foto Admin" 
                      class="profile-thumb" 
                      @click="openImageModal(admin.foto)"
                    />
                  </div>
                </td>
                <td class="text-white">
                  <div class="cell-content">
                    <span class="name-text">{{ admin.nombre || 'Sin nombre' }}</span>
                    <div class="mobile-only info-grid">
                      <div class="info-item">
                        <span class="info-label">📧</span>
                        <span class="info-value">{{ admin.correo || '-' }}</span>
                      </div>
                      <div class="info-item">
                        <span class="info-label">🆔</span>
                        <span class="info-value">{{ admin.documento || '-' }}</span>
                      </div>
                      <div class="info-item">
                        <span class="info-label">📱</span>
                        <span class="info-value">{{ admin.telefono || '-' }}</span>
                      </div>
                    </div>
                  </div>
                </td>
                <td class="text-muted hide-mobile">{{ admin.correo || '-' }}</td>
                <td class="text-muted hide-mobile">{{ admin.documento || '-' }}</td>
                <td class="text-muted hide-mobile">{{ admin.telefono || '-' }}</td>
                <td class="text-muted hide-tablet">{{ formatDate(admin.fecha_agregado) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-if="filteredAdministradores.length === 0 && !loading" class="no-data">
          {{ searchAdmin ? 'No se encontraron resultados' : 'No hay administradores registrados.' }}
        </p>
      </div>

      <!-- PRODUCTOS -->
      <div v-else-if="currentView === 'productos'" class="list-section">
        <div class="section-header">
          <h2 class="section-title cyan-gradient">
            <i class="fas fa-boxes"></i> 
            <span class="title-text">Inventario de Productos</span>
          </h2>
        </div>

        <!-- Buscador Productos -->
        <div class="search-container">
          <div class="search-box">
            <i class="fas fa-search search-icon"></i>
            <input 
              v-model="searchProduct" 
              type="text" 
              placeholder="Buscar producto por nombre..."
              class="search-input"
            />
            <button 
              v-if="searchProduct" 
              @click="searchProduct = ''"
              class="clear-btn"
            >
              <i class="fas fa-times"></i>
            </button>
          </div>
        </div>

        <!-- CARD DE VALOR TOTAL DEL INVENTARIO -->
        <div class="inventory-summary">
          <div class="summary-card">
            <div class="summary-icon">
              <i class="fas fa-money-bill-wave"></i>
            </div>
            <div class="summary-content">
              <p class="summary-label">Valor Total</p>
              <p class="summary-value">{{ formatPrice(calcularValorInventario()) }}</p>
            </div>
          </div>
          <div class="summary-card">
            <div class="summary-icon cyan">
              <i class="fas fa-box"></i>
            </div>
            <div class="summary-content">
              <p class="summary-label">Total Productos</p>
              <p class="summary-value">{{ calcularTotalProductos() }}</p>
            </div>
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Imagen</th>
                <th>Nombre</th>
                <th>Cant.</th>
                <th class="hide-mobile">Precio</th>
                <th class="hide-tablet">Total</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prod in filteredProductos" :key="prod.id">
                <td>
                  <div class="image-zoom-wrapper">
                    <img 
                      :src="prod.imagen" 
                      alt="Imagen Producto" 
                      class="product-thumb" 
                      @click="openImageModal(prod.imagen)"
                    />
                  </div>
                </td>
                <td class="text-white">
                  <div class="cell-content">
                    <span class="name-text">{{ prod.nombre || 'Sin nombre' }}</span>
                    <span class="mobile-only subtitle-text">{{ formatPrice(prod.precio) }}</span>
                  </div>
                </td>
                <td class="text-cyan">{{ prod.cantidad ?? 0 }}</td>
                <td class="text-muted hide-mobile">{{ formatPrice(prod.precio) }}</td>
                <td class="text-pink font-bold hide-tablet">{{ formatPrice((prod.cantidad ?? 0) * (prod.precio ?? 0)) }}</td>
                <td><span :class="['estado-badge', prod.estado || 'activo']">{{ (prod.estado || 'activo').charAt(0).toUpperCase() + (prod.estado || 'activo').slice(1) }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-if="filteredProductos.length === 0 && !loading" class="no-data">
          {{ searchProduct ? 'No se encontraron resultados' : 'No hay productos registrados.' }}
        </p>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL } from '@/config/api'

export default {
  data() {
    return {
      currentView: 'administradores',
      administradoresData: [],
      productosData: [],
      searchAdmin: '',
      searchProduct: '',
      loading: true,
      error: null,
      barId: null,
      imageModalOpen: false,
      modalImageSrc: '',
      defaultProfilePhoto: 'https://static.vecteezy.com/system/resources/thumbnails/065/748/662/small_2x/gray-placeholder-man-and-woman-avatar-default-user-icon-set-social-media-user-profile-icon-free-vector.jpg',
      defaultProductPhoto: 'https://shop.farmranchstore.com/cdn/shop/products/noimage-found_ae031b94-ce16-49e4-9d55-c0993c30e771_500x.png?v=1697660801',
    }
  },

  computed: {
    filteredAdministradores() {
      if (!this.searchAdmin) return this.administradoresData
      const search = this.searchAdmin.toLowerCase()
      return this.administradoresData.filter(admin =>
        (admin.nombre || '').toLowerCase().includes(search) ||
        (admin.correo || '').toLowerCase().includes(search) ||
        (admin.documento || '').includes(search) ||
        (admin.telefono || '').includes(search)
      )
    },

    filteredProductos() {
      if (!this.searchProduct) return this.productosData
      const search = this.searchProduct.toLowerCase()
      return this.productosData.filter(prod =>
        (prod.nombre || '').toLowerCase().includes(search)
      )
    }
  },

  methods: {
    openImageModal(imageSrc) {
      this.modalImageSrc = imageSrc
      this.imageModalOpen = true
      document.body.style.overflow = 'hidden'
    },

    closeImageModal() {
      this.imageModalOpen = false
      this.modalImageSrc = ''
      document.body.style.overflow = 'auto'
    },

    goBack() {
      window.history.back()
    },

    setView(viewName) {
      this.currentView = viewName
      this.searchAdmin = ''
      this.searchProduct = ''
    },

    formatPrice(value) {
      if (!value && value !== 0) return '$0'
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(value)
    },

    formatDate(dateStr) {
      if (!dateStr) return '-'
      const date = new Date(dateStr)
      return isNaN(date) ? '-' : date.toLocaleDateString('es-CO')
    },

    calcularValorInventario() {
      return this.productosData.reduce((total, producto) => {
        return total + ((producto.cantidad || 0) * (producto.precio || 0))
      }, 0)
    },

    calcularTotalProductos() {
      return this.productosData.reduce((total, producto) => {
        return total + (producto.cantidad || 0)
      }, 0)
    },

    extractBarIdFromUrl() {
      const path = window.location.pathname
      const match = path.match(/\/info_locales\/(\d+)/)
      if (match) {
        this.barId = parseInt(match[1], 10)
      } else {
        this.error = 'No se pudo detectar el ID del bar en la URL'
        this.loading = false
      }
    },

    async fetchAdministradores() {
      if (!this.barId) return
      try {
        const response = await axios.get(`${API_BASE_URL}/administradores/bar/${this.barId}`)
        const data = Array.isArray(response.data) ? response.data : []
        this.administradoresData = data.map(admin => ({
          ...admin,
          foto: admin.foto || this.defaultProfilePhoto
        }))
      } catch (err) {
        console.error('Error cargando administradores:', err)
        this.error = 'Error al cargar administradores'
        this.administradoresData = []
      }
    },

    async fetchProductos() {
      if (!this.barId) return
      try {
        const response = await axios.get(`${API_BASE_URL}/productos_por_bar/${this.barId}`)
        const data = Array.isArray(response.data) ? response.data : []
        this.productosData = data.map(prod => ({
          ...prod,
          imagen: prod.imagen || this.defaultProductPhoto,
          estado: prod.estado || 'activo'
        }))
      } catch (err) {
        console.error('Error cargando productos:', err)
        this.error = 'Error al cargar productos'
        this.productosData = []
      }
    },

    async loadData() {
      this.loading = true
      this.error = null
      await Promise.all([
        this.fetchAdministradores(),
        this.fetchProductos()
      ])
      this.loading = false
    }
  },

  mounted() {
    this.extractBarIdFromUrl()
    if (this.barId) {
      this.loadData()
    } else {
      this.loading = false
    }
  },

  beforeUnmount() {
    document.body.style.overflow = 'auto'
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { box-sizing: border-box; }

/* COLORES */
.pink-text { color: #FF1493; }
.cyan-text { color: #00d4ff; }
.text-white { color: #ffffff; font-weight: 500; }
.text-muted { color: #9ca3af; }
.text-cyan { color: #00d4ff; font-weight: 600; }
.text-pink { color: #FF1493; }
.font-bold { font-weight: 700; }

/* LAYOUT GENERAL */
.panel-de-control {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  color: #ffffff;
  position: relative;
}

/* LOADER */
.loading-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  color: white;
  font-size: 1.2rem;
}

.spinner {
  width: 60px;
  height: 60px;
  border: 6px solid #333;
  border-top: 6px solid #00d4ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ERROR */
.error-message {
  text-align: center;
  padding: 1.5rem;
  background: rgba(255, 0, 0, 0.2);
  color: #ff6b6b;
  margin: 1rem;
  border-radius: 12px;
  border: 2px solid #ff006e;
}

.btn-retry {
  margin-top: 1rem;
  padding: 0.7rem 1.5rem;
  background: #FF1493;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-retry:hover {
  background: #ff006e;
  transform: translateY(-2px);
}

/* HEADER */
.header {
  position: sticky;
  top: 0;
  background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
  border-bottom: 2px solid #FF1493;
  box-shadow: 0 4px 20px rgba(255, 20, 147, 0.3);
  z-index: 100;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-left {
  flex: 0 0 auto;
}

.header-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #FF1493, #00d4ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.bar-id-info {
  display: block;
  font-size: 0.75rem;
  font-weight: 500;
  color: #9ca3af;
  margin-top: 0.25rem;
  background: none;
  -webkit-text-fill-color: #9ca3af;
}

.header-nav {
  display: flex;
  gap: 0.75rem;
  flex: 1;
  justify-content: center;
  flex-wrap: wrap;
}

.nav-button {
  padding: 0.7rem 1.2rem;
  border: 2px solid #00d4ff;
  background: rgba(0, 212, 255, 0.1);
  color: #00d4ff;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

.nav-button:hover {
  background: rgba(0, 212, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
}

.nav-button.active {
  background: linear-gradient(135deg, #FF1493, #ff006e);
  color: white;
  border-color: #FF1493;
  box-shadow: 0 4px 20px rgba(255, 20, 147, 0.5);
}

.nav-button i {
  font-size: 1.1rem;
}

.btn-volver {
  padding: 0.7rem 1.2rem;
  background: linear-gradient(135deg, #2d2d2d, #1a1a1a);
  color: white;
  border: 2px solid #404040;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

.btn-volver:hover {
  background: linear-gradient(135deg, #404040, #2d2d2d);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(255, 255, 255, 0.1);
}

/* CONTENIDO */
.content {
  padding: 2rem 1.5rem;
  max-width: 1600px;
  margin: 0 auto;
}

.list-section {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.section-header {
  margin-bottom: 2rem;
}

.section-title {
  padding: 1.2rem 2rem;
  border-radius: 16px;
  text-align: center;
  font-size: 1.6rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
}

.pink-gradient {
  background: linear-gradient(135deg, #FF1493, #ff006e);
  color: white;
}

.cyan-gradient {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  color: white;
}

/* BUSCADOR */
.search-container {
  margin-bottom: 2rem;
}

.search-box {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.search-icon {
  position: absolute;
  left: 1.2rem;
  top: 50%;
  transform: translateY(-50%);
  color: #00d4ff;
  font-size: 1.1rem;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 1rem 3.5rem 1rem 3.5rem;
  background: linear-gradient(135deg, #1f1f1f, #151515);
  border: 2px solid #00d4ff;
  border-radius: 16px;
  color: white;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s;
  outline: none;
}

.search-input::placeholder {
  color: #6b7280;
}

.search-input:focus {
  border-color: #FF1493;
  box-shadow: 0 4px 20px rgba(255, 20, 147, 0.3);
}

.clear-btn {
  position: absolute;
  right: 1.2rem;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 20, 147, 0.2);
  border: none;
  color: #FF1493;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.clear-btn:hover {
  background: #FF1493;
  color: white;
}

/* RESUMEN DE INVENTARIO */
.inventory-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: linear-gradient(135deg, #1f1f1f, #151515);
  border: 2px solid #FF1493;
  border-radius: 16px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 8px 30px rgba(255, 20, 147, 0.3);
  transition: all 0.3s;
}

.summary-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(255, 20, 147, 0.5);
}

.summary-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #FF1493, #ff006e);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
  flex-shrink: 0;
}

.summary-icon.cyan {
  background: linear-gradient(135deg, #00d4ff, #0099cc);
}

.summary-content {
  flex: 1;
}

.summary-label {
  font-size: 0.9rem;
  color: #9ca3af;
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.summary-value {
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #FF1493, #00d4ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* TABLAS */
.table-container {
  overflow-x: auto;
  border-radius: 16px;
  background: linear-gradient(135deg, #1a1a1a, #0f0f0f);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
  border: 2px solid #2d2d2d;
}

.data-table {
  width: 100%;
  min-width: 600px;
  border-collapse: collapse;
}

.data-table thead {
  background: linear-gradient(135deg, #FF1493, #ff006e);
  color: white;
}

.data-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.95rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.data-table td {
  padding: 1rem;
  border-bottom: 1px solid #2d2d2d;
}

.data-table tbody tr {
  transition: all 0.3s;
}

.data-table tbody tr:hover {
  background: rgba(0, 212, 255, 0.05);
  transform: scale(1.01);
}

/* MODAL DE IMAGEN */
.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 2rem;
  animation: fadeInModal 0.3s ease-in-out;
  cursor: pointer;
}

@keyframes fadeInModal {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  animation: zoomInImage 0.3s ease-in-out;
}

@keyframes zoomInImage {
  from { 
    transform: scale(0.5);
    opacity: 0;
  }
  to { 
    transform: scale(1);
    opacity: 1;
  }
}

.modal-image {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 16px;
  border: 3px solid #FF1493;
  box-shadow: 0 20px 80px rgba(255, 20, 147, 0.6);
}

.modal-close {
  position: absolute;
  top: -15px;
  right: -15px;
  width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #FF1493, #ff006e);
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 4px 20px rgba(255, 20, 147, 0.6);
}

.modal-close:hover {
  transform: rotate(90deg) scale(1.1);
  background: linear-gradient(135deg, #ff006e, #c9004c);
}

/* WRAPPER DE IMÁGENES */
.image-zoom-wrapper {
  position: relative;
  display: inline-block;
}

.profile-thumb, .product-thumb {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 12px;
  border: 2px solid #00d4ff;
  background-color: #1a1a1a;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
}

.product-thumb {
  object-fit: contain;
  padding: 4px;
}

.profile-thumb:hover,
.product-thumb:hover {
  border-color: #FF1493;
  box-shadow: 0 4px 20px rgba(255, 20, 147, 0.5);
  transform: scale(1.1);
}

.cell-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.name-text {
  font-weight: 600;
  font-size: 1rem;
}

.subtitle-text {
  font-size: 0.85rem;
  color: #9ca3af;
}

.mobile-only {
  display: none;
}

/* GRID DE INFORMACIÓN PARA MÓVIL */
.info-grid {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-top: 0.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 212, 255, 0.08);
  padding: 0.4rem 0.6rem;
  border-radius: 8px;
  border-left: 3px solid #00d4ff;
}

.info-label {
  font-size: 0.9rem;
  flex-shrink: 0;
}

.info-value {
  font-size: 0.85rem;
  color: #e5e7eb;
  font-weight: 500;
  word-break: break-all;
}

.estado-badge {
  padding: 0.4rem 0.9rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.estado-badge.activo { 
  background: linear-gradient(135deg, #00d4ff, #0099cc); 
  color: white;
  box-shadow: 0 4px 15px rgba(0, 212, 255, 0.4);
}

.estado-badge.agotado { 
  background: linear-gradient(135deg, #ff006e, #c9004c); 
  color: white;
  box-shadow: 0 4px 15px rgba(255, 0, 110, 0.4);
}

.no-data {
  text-align: center;
  padding: 3rem;
  color: #9ca3af;
  font-size: 1.1rem;
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .header {
    padding: 1rem;
  }
  
  .header-title {
    font-size: 1.5rem;
  }
  
  .content {
    padding: 1.5rem 1rem;
  }

  .hide-tablet {
    display: none;
  }
}

@media (max-width: 768px) {
  .header {
    padding: 0.75rem;
    gap: 0.5rem;
  }
  
  .header-left {
    width: 100%;
    text-align: center;
  }
  
  .header-title {
    font-size: 1.2rem;
  }

  .bar-id-info {
    font-size: 0.7rem;
  }
  
  .header-nav {
    width: 100%;
    gap: 0.5rem;
  }

  .nav-button {
    flex: 1;
    justify-content: center;
    padding: 0.65rem 0.5rem;
    font-size: 0.85rem;
  }

  .nav-button i {
    font-size: 1rem;
  }

  .nav-text {
    font-size: 0.85rem;
  }
  
  .btn-volver {
    width: 100%;
    justify-content: center;
    padding: 0.65rem;
  }
  
  .section-title {
    font-size: 1.3rem;
    padding: 1rem;
  }

  .title-text {
    display: none;
  }

  .section-title i {
    font-size: 1.5rem;
  }
  
  .inventory-summary {
    grid-template-columns: 1fr;
  }
  
  .summary-card {
    padding: 1.2rem;
  }
  
  .summary-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .summary-value {
    font-size: 1.5rem;
  }

  .summary-label {
    font-size: 0.85rem;
  }
  
  .data-table {
    font-size: 0.9rem;
    min-width: 500px;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.7rem 0.5rem;
  }
  
  .profile-thumb, .product-thumb {
    width: 40px;
    height: 40px;
  }

  .hide-mobile {
    display: none;
  }

  .mobile-only {
    display: block;
  }

  .search-input {
    font-size: 0.9rem;
    padding: 0.9rem 3rem 0.9rem 3rem;
  }

  .search-icon {
    font-size: 1rem;
    left: 1rem;
  }

  .clear-btn {
    width: 28px;
    height: 28px;
    right: 1rem;
  }

  .image-modal {
    padding: 1rem;
  }

  .modal-close {
    width: 40px;
    height: 40px;
    font-size: 1.3rem;
    top: -10px;
    right: -10px;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 0.6rem;
  }

  .header-title {
    font-size: 1.1rem;
  }

  .bar-id-info {
    font-size: 0.65rem;
  }
  
  .nav-button {
    font-size: 0.8rem;
    padding: 0.6rem 0.4rem;
    gap: 0.3rem;
  }
  
  .nav-button i {
    font-size: 0.95rem;
  }
  
  .nav-text {
    font-size: 0.75rem;
  }
  
  .btn-volver {
    font-size: 0.9rem;
    padding: 0.6rem;
  }
  
  .btn-text {
    font-size: 0.85rem;
  }
  
  .section-title {
    font-size: 1.1rem;
    padding: 0.8rem;
  }
  
  .summary-card {
    padding: 1rem;
    gap: 1rem;
  }
  
  .summary-icon {
    width: 50px;
    height: 50px;
    font-size: 1.3rem;
  }
  
  .summary-value {
    font-size: 1.3rem;
  }

  .summary-label {
    font-size: 0.8rem;
  }
  
  .data-table {
    min-width: 450px;
    font-size: 0.85rem;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.6rem 0.4rem;
  }
  
  .profile-thumb, .product-thumb {
    width: 35px;
    height: 35px;
  }
  
  .estado-badge {
    font-size: 0.7rem;
    padding: 0.3rem 0.6rem;
  }

  .name-text {
    font-size: 0.9rem;
  }

  .subtitle-text {
    font-size: 0.75rem;
  }

  .info-item {
    padding: 0.35rem 0.5rem;
    gap: 0.4rem;
  }

  .info-label {
    font-size: 0.85rem;
  }

  .info-value {
    font-size: 0.8rem;
  }

  .search-input {
    font-size: 0.85rem;
    padding: 0.8rem 2.8rem 0.8rem 2.8rem;
  }

  .search-icon {
    font-size: 0.9rem;
    left: 0.9rem;
  }

  .clear-btn {
    width: 26px;
    height: 26px;
    right: 0.9rem;
    font-size: 0.85rem;
  }

  .no-data {
    font-size: 1rem;
    padding: 2rem 1rem;
  }

  .content {
    padding: 1rem 0.5rem;
  }

  .modal-close {
    width: 35px;
    height: 35px;
    font-size: 1.2rem;
    top: -8px;
    right: -8px;
  }
}
</style>