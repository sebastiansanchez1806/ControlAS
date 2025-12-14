<template>
  <div class="panel-de-control">
    <!-- Header fijo con navegación integrada -->
    <header class="header">
      <div class="header-left">
        <h1 class="header-title">
          <span class="pink-text">P</span>anel de <span class="cyan-text">G</span>estión
        </h1>
      </div>
      
      <nav class="header-nav">
        <button 
          @click="setView('administradores')" 
          :class="['nav-button', { active: currentView === 'administradores' }]"
        >
          <i class="fas fa-user-shield"></i> 
          <span class="nav-text">Administradores</span>
        </button>
        <button 
          @click="setView('productos')" 
          :class="['nav-button', { active: currentView === 'productos' }]"
        >
          <i class="fas fa-boxes"></i> 
          <span class="nav-text">Productos</span>
        </button>
        <button 
          @click="setView('mujeres')" 
          :class="['nav-button', { active: currentView === 'mujeres' }]"
        >
          <i class="fas fa-female"></i> 
          <span class="nav-text">Mujeres</span>
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
            <i class="fas fa-user-shield"></i> Gestión de Administradores
          </h2>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Foto</th>
                <th>Nombre</th>
                <th>Correo</th>
                <th>Documento</th>
                <th>Teléfono</th>
                <th>Agregado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="admin in administradoresData" :key="admin.id">
                <td><img :src="admin.foto" alt="Foto Admin" class="profile-thumb" /></td>
                <td class="text-white">{{ admin.nombre }}</td>
                <td class="text-muted">{{ admin.correo }}</td>
                <td class="text-muted">{{ admin.documento }}</td>
                <td class="text-muted">{{ admin.telefono }}</td>
                <td class="text-muted">{{ admin.fecha_agregado }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-if="administradoresData.length === 0" class="no-data">No hay administradores registrados.</p>
      </div>

      <!-- PRODUCTOS -->
      <div v-else-if="currentView === 'productos'" class="list-section">
        <div class="section-header">
          <h2 class="section-title cyan-gradient">
            <i class="fas fa-boxes"></i> Inventario de Productos
          </h2>
        </div>

        <!-- CARD DE VALOR TOTAL DEL INVENTARIO -->
        <div class="inventory-summary">
          <div class="summary-card">
            <div class="summary-icon">
              <i class="fas fa-money-bill-wave"></i>
            </div>
            <div class="summary-content">
              <p class="summary-label">Valor Total del Inventario</p>
              <p class="summary-value">{{ formatPrice(calcularValorInventario()) }}</p>
            </div>
          </div>
          <div class="summary-card">
            <div class="summary-icon cyan">
              <i class="fas fa-box"></i>
            </div>
            <div class="summary-content">
              <p class="summary-label">Total de Productos</p>
              <p class="summary-value">{{ calcularTotalProductos() }} unidades</p>
            </div>
          </div>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Imagen</th>
                <th>Nombre</th>
                <th>Cantidad</th>
                <th>Precio Unit.</th>
                <th>Valor Total</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prod in productosData" :key="prod.id">
                <td><img :src="prod.imagen" alt="Imagen Producto" class="product-thumb" /></td>
                <td class="text-white">{{ prod.nombre }}</td>
                <td class="text-cyan">{{ prod.cantidad }}</td>
                <td class="text-muted">{{ formatPrice(prod.precio) }}</td>
                <td class="text-pink font-bold">{{ formatPrice(prod.cantidad * prod.precio) }}</td>
                <td><span :class="['estado-badge', prod.estado]">{{ prod.estado }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-if="productosData.length === 0" class="no-data">No hay productos registrados.</p>
      </div>

      <!-- MUJERES -->
      <div v-else-if="currentView === 'mujeres'" class="list-section">
        <div class="section-header">
          <h2 class="section-title pink-gradient">
            <i class="fas fa-female"></i> Registro de Empleadas/Personal
          </h2>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Foto</th>
                <th>Nombre</th>
                <th>Teléfono</th>
                <th>Agregado</th>
                <th>Examen Médico</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="mujer in mujeresData" :key="mujer.id">
                <td><img :src="mujer.foto" alt="Foto Mujer" class="profile-thumb" /></td>
                <td class="text-white">{{ mujer.nombre }}</td>
                <td class="text-muted">{{ mujer.telefono || 'N/A' }}</td>
                <td class="text-muted">{{ mujer.fecha_agregado }}</td>
                <td>
                  <span :class="{'examen-ok': mujer.fecha_examen, 'examen-pend': !mujer.fecha_examen}">
                    {{ mujer.fecha_examen ? '✅ Realizado' : '⚠️ Pendiente' }}
                  </span>
                </td>
                <td>
                  <button 
                    v-if="mujer.foto_examen" 
                    @click="openExamModal(mujer)" 
                    class="btn-action"
                  >
                    <i class="fas fa-eye"></i> Ver
                  </button>
                  <span v-else class="text-muted">Sin documento</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-if="mujeresData.length === 0" class="no-data">No hay personal registrado.</p>
      </div>
    </main>

    <!-- Modal -->
    <div v-if="showExamModal" class="modal-overlay" @click.self="closeExamModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="modal-title">Examen Médico de {{ selectedMujer.nombre }}</h3>
          <button @click="closeExamModal" class="btn-close-modal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-body">
          <img 
            :src="selectedMujer.foto_examen" 
            alt="Imagen del Examen Médico" 
            class="full-image" 
            v-if="isImage(selectedMujer.foto_examen)"
          >
          <p v-else class="no-data-modal">El documento no es una imagen o no está disponible.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentView: 'administradores',
      administradoresData: [],
      productosData: [],
      mujeresData: [],
      showExamModal: false,
      selectedMujer: null,
      defaultProfilePhoto: 'https://static.vecteezy.com/system/resources/thumbnails/065/748/662/small_2x/gray-placeholder-man-and-woman-avatar-default-user-icon-set-social-media-user-profile-icon-free-vector.jpg',
      defaultProductPhoto: 'https://shop.farmranchstore.com/cdn/shop/products/noimage-found_ae031b94-ce16-49e4-9d55-c0993c30e771_500x.png?v=1697660801',
      simulatedExamImage: 'https://via.placeholder.com/800x600/1a1a1a/00d4ff?text=Examen+Médico'
    };
  },

  methods: {
    goBack() {
      window.history.back();
    },

    setView(viewName) {
      this.currentView = viewName;
    },

    openExamModal(mujer) {
      this.selectedMujer = mujer;
      this.showExamModal = true;
    },

    closeExamModal() {
      this.showExamModal = false;
      this.selectedMujer = null;
    },

    isImage(url) {
      return url && (url.startsWith('http') || url.startsWith('data:image/'));
    },

    formatPrice(value) {
      return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      }).format(value);
    },

    calcularValorInventario() {
      return this.productosData.reduce((total, producto) => {
        return total + (producto.cantidad * producto.precio);
      }, 0);
    },

    calcularTotalProductos() {
      return this.productosData.reduce((total, producto) => {
        return total + producto.cantidad;
      }, 0);
    },

    async fetchAdministradores() {
      await new Promise(resolve => setTimeout(resolve, 500));
      this.administradoresData = [
        { id: 1, nombre: 'Juan Pérez', correo: 'juan@bar.com', documento: '100123456', telefono: '3001112233', fecha_agregado: '2024-10-01', foto: this.defaultProfilePhoto },
        { id: 2, nombre: 'María López', correo: 'maria@bar.com', documento: '100654321', telefono: '3004445566', fecha_agregado: '2024-10-15', foto: this.defaultProfilePhoto },
         { id: 2, nombre: 'María López', correo: 'maria@bar.com', documento: '100654321', telefono: '3004445566', fecha_agregado: '2024-10-15', foto: this.defaultProfilePhoto },
      ];
    },

    async fetchProductos() {
      await new Promise(resolve => setTimeout(resolve, 500));
      this.productosData = [
        { id: 101, nombre: 'Cerveza Corona', cantidad: 5, precio: 1000, estado: 'activo', imagen: this.defaultProductPhoto },
        { id: 102, nombre: 'Agua Embotellada', cantidad: 5, precio: 1000, estado: 'activo', imagen: this.defaultProductPhoto },
        { id: 103, nombre: 'Ron Viejo de Caldas', cantidad: 80, precio: 95000, estado: 'activo', imagen: this.defaultProductPhoto },
        { id: 104, nombre: 'Whisky Jack Daniels', cantidad: 15, precio: 180000, estado: 'activo', imagen: this.defaultProductPhoto },
      ];
    },

    async fetchMujeres() {
      await new Promise(resolve => setTimeout(resolve, 500));
      this.mujeresData = [
        { id: 201, nombre: 'Ana Gómez', telefono: '3101112233', fecha_agregado: '2024-11-01', fecha_examen: '2024-12-01', foto: this.defaultProfilePhoto, foto_examen: "https://medlineplus.gov/images/WomensHealthCheckup.jpg" },
        { id: 202, nombre: 'Luisa Torres', telefono: '3104445566', fecha_agregado: '2024-11-15', fecha_examen: null, foto: this.defaultProfilePhoto, foto_examen: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTs86OgihrChzCicuvCaKe1VG99ulSqmdqung&s" },
        { id: 203, nombre: 'Sofia Rojas', telefono: '3107778899', fecha_agregado: '2024-12-05', fecha_examen: '2024-12-10', foto: this.defaultProfilePhoto, foto_examen: "https://www.clinicauandes.cl/images/default-source/365/novedad_mujer-exa-menes-(1).webp?sfvrsn=cf726d9e_2" },
      ];
    },
  },

  mounted() {
    this.fetchAdministradores();
    this.fetchProductos();
    this.fetchMujeres();
  }
};
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
  box-sizing: border-box;
}

/* COLORES PRINCIPALES */
.pink-text { color: #FF1493; }
.cyan-text { color: #00d4ff; }
.text-white { color: #ffffff; font-weight: 500; }
.text-muted { color: #9ca3af; }
.text-cyan { color: #00d4ff; font-weight: 600; }
.text-pink { color: #FF1493; }
.font-bold { font-weight: 700; }

/* CONTENEDOR PRINCIPAL */
.panel-de-control {
  min-height: 100vh;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
  color: #ffffff;
}

/* HEADER FIJO CON NAVEGACIÓN */
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
  min-width: 700px;
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

.profile-thumb, .product-thumb {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 12px;
  border: 2px solid #00d4ff;
  background-color: #1a1a1a;
}

.product-thumb {
  object-fit: contain;
  padding: 4px;
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

.examen-ok { 
  color: #00d4ff; 
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0, 212, 255, 0.5);
}

.examen-pend { 
  color: #ffc107; 
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(255, 193, 7, 0.5);
}

.btn-action {
  padding: 0.6rem 1rem;
  background: linear-gradient(135deg, #00d4ff, #0099cc);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5);
}

.no-data {
  text-align: center;
  padding: 3rem;
  color: #9ca3af;
  font-size: 1.1rem;
}

/* MODAL */
.modal-overlay {
  position: fixed;
  top: 0; 
  left: 0;
  width: 100%; 
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: linear-gradient(135deg, #1a1a1a, #0f0f0f);
  border: 2px solid #FF1493;
  border-radius: 20px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(255, 20, 147, 0.5);
}

.modal-header {
  padding: 1.5rem 2rem;
  border-bottom: 2px solid #2d2d2d;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #1f1f1f, #151515);
}

.modal-title {
  margin: 0;
  font-size: 1.3rem;
  color: #00d4ff;
  font-weight: 700;
}

.btn-close-modal {
  background: rgba(255, 20, 147, 0.2);
  border: 2px solid #FF1493;
  color: #FF1493;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close-modal:hover {
  background: #FF1493;
  color: white;
  transform: rotate(90deg);
}

.modal-body {
  padding: 2rem;
  text-align: center;
  overflow-y: auto;
  max-height: calc(90vh - 100px);
}

.full-image {
  max-width: 100%;
  max-height: 70vh;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

.no-data-modal {
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
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }
  
  .header-left {
    text-align: center;
  }
  
  .header-title {
    font-size: 1.3rem;
  }
  
  .header-nav {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .nav-button {
    justify-content: center;
    padding: 0.8rem;
  }
  
  .btn-volver {
    justify-content: center;
  }
  
  .section-title {
    font-size: 1.3rem;
    padding: 1rem;
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
  
  .data-table {
    font-size: 0.9rem;
  }
  
  .data-table th,
  .data-table td {
    padding: 0.7rem 0.5rem;
  }
  
  .profile-thumb, .product-thumb {
    width: 40px;
    height: 40px;
  }
  
  .modal-content {
    width: 95%;
    max-height: 95vh;
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-title {
    font-size: 1.1rem;
  }
  
  .modal-body {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .header-title {
    font-size: 1.1rem;
  }
  
  .nav-button {
    font-size: 0.85rem;
    padding: 0.7rem;
  }
  
  .nav-button i {
    font-size: 1rem;
  }
  
  .nav-text {
    display: none;
  }
  
  .btn-volver {
    font-size: 0.9rem;
    padding: 0.6rem 1rem;
  }
  
  .btn-text {
    display: none;
  }
  
  .section-title {
    font-size: 1.1rem;
    padding: 0.8rem;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .summary-card {
    flex-direction: column;
    text-align: center;
    padding: 1rem;
  }
  
  .summary-icon {
    width: 50px;
    height: 50px;
    font-size: 1.3rem;
  }
  
  .summary-value {
    font-size: 1.3rem;
  }
  
  .data-table {
    min-width: 600px;
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
    font-size: 0.75rem;
    padding: 0.3rem 0.6rem;
  }
  
  .btn-action {
    padding: 0.5rem 0.8rem;
    font-size: 0.85rem;
  }
}
</style>