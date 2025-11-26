<template>
  <div id="app">
    <header class="header">
      <div class="header-content">
        <button class="back-button" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5M12 19l-7-7 7-7" />
          </svg>
          Volver
        </button>

        <div class="logo-section">
          <div class="logo-container">
            <div class="logo-placeholder">
              <img :src="activeBarStore.image" alt="Valka Logo" />
            </div>
            <div class="brand-text">
              <h1 class="brand-name glitch">{{ activeBarStore.name }}</h1>

              <span class="brand-subtitle">ID del Local: {{ activeBarStore.id }}</span>
            </div>
          </div>
        </div>

        <nav class="nav-buttons">
          <button class="nav-btn admin-btn" @click="irAAdministradores">
            <span class="btn-icon">👥</span>
            <span class="btn-text">Administradores</span>
          </button>

          <button class="nav-btn admin-btn" @click="irhistorial">
            <span>
              🧾
            </span>
            <span class="btn-text">Movimientos</span>
          </button>

          <button class="nav-btn admin-btn" @click="irAFacturas">
            <span class="btn-icon">📄</span>
            <span class="btn-text">Facturas</span>
          </button>
        </nav>
      </div>
    </header>
    <button class="floating-add-btn" @click="openAddProductModal">
      <span class="btn-icon">➕</span>
      <span class="btn-text">Agregar Producto</span>
    </button>
    <main class="main-content">
      <div class="container">
       <div class="page-title">
  <h2 class="title-text">Gestión de Inventario</h2>
  <div class="title-decoration"></div>
</div>

<!-- NUEVO: Valor Total del Inventario -->
<div class="inventory-total-card">
  <div class="total-label">
    <span class="icon">💰</span>
    Valor Total del Inventario
  </div>
  <div class="total-amount">
    ${{ totalInventoryValue.toLocaleString('es-CO') }}
  </div>
  <div class="total-subtitle">
    {{ products.length }} producto{{ products.length !== 1 ? 's' : '' }} de inventario
  </div>
</div>

        <div class="search-and-filters">
          <div class="search-section">
            <div class="search-inputs">
              <input type="text" v-model="searchTerm" placeholder="Buscar producto por nombre..." class="search-input">
              <button @click="clearSearch" class="clear-search-btn" v-if="searchTerm">
                Limpiar Búsqueda
              </button>
            </div>
          </div>

          <div class="filters">
            <button class="filter-btn" @click="showAllProducts = true" :class="{ active: showAllProducts }">
              <span class="filter-icon">📦</span>
              <span>Todos los Productos</span>
              <span class="filter-count">({{ products.length }})</span>
            </button>
            <button class="filter-btn sold-out-btn" @click="showAllProducts = false"
              :class="{ active: !showAllProducts }">
              <span class="filter-icon">⚠️</span>
              <span>Ver Agotados</span>
              <span class="filter-count">({{ soldOutCount }})</span>
            </button>
          </div>

        </div>

        <div class="products-grid">
          <div v-for="product in filteredProducts" :key="product.id" class="product-card"
            :class="{ 'sold-out': product.cantidad === 0 }">
            <div class="product-image">
              <img :src="product.imagen" :alt="product.nombre" />
              <div class="product-overlay">
                <div class="product-status" :class="{ 'out-of-stock': product.cantidad === 0 }">
                  {{ product.cantidad === 0 ? 'AGOTADO' : 'DISPONIBLE' }}
                </div>
              </div>

            </div>

            <div class="product-info">
              <h3 class="product-name">{{ product.nombre }}</h3>
              <div class="product-price">
                <span class="currency">$</span>
                <span class="amount">{{ product.precio.toLocaleString('es-CO') }}</span>
              </div>


              <div class="product-details">
                <div class="product-quantity">
                  <span class="quantity-label">Stock:</span>
                  <span v-if="product.cantidad > 0" class="quantity-value available">
                    {{ product.cantidad }} unidades
                  </span>
                  
                  <span v-else class="quantity-value sold-out-text">
                    AGOTADO
                  </span>
                  
                </div>

                  <div class="product-total-value">
  <span class="total_jaja">Valor total:</span>
  <span class="total-value">
    ${{ (product.cantidad * product.precio).toLocaleString('es-CO') }}
  </span>
</div>
                <button class="action-btn edit-btn product-image-edit-btn" @click="openEditProductModal(product)"
                  title="Editar producto">
                  <span class="btn-icon">✏️</span>
                </button>
              </div>

              <div class="product-actions">
                <button class="action-btn decrease-btn" @click="openUpdateModal(product, 'decrease')"
                  :disabled="product.cantidad === 0" title="Disminuir stock">
                  <span class="btn-icon">➖</span>
                </button>
                <div class="stock-display">
                  <span class="stock-number">{{ product.cantidad }}</span>
                </div>
                <button class="action-btn increase-btn" @click="openUpdateModal(product, 'increase')"
                  title="Aumentar stock">
                  <span class="btn-icon">➕</span>
                </button>
                <button class="action-btn delete-btn" @click="confirmDelete(product)" title="Eliminar producto">
                  <span class="btn-icon">🗑️</span>
                </button>
              </div>


            </div>
          </div>
        </div>
        
        <div v-if="isFetching" class="loading-more-products">
            <span class="loading-spinner"></span>
            Cargando más productos...
        </div>
        
        <div v-if="!isFetching && !hasMore && products.length > 0" class="end-of-list">
            <span class="end-icon">🏁</span>
            Has llegado al final del inventario activo.
        </div>
        <div v-if="filteredProducts.length === 0 && !isFetching && searchTerm.length === 0" class="empty-state">
          <div class="empty-animation">
            <div class="empty-icon">📦</div>
            <div class="empty-particles">
              <div class="particle"></div>
              <div class="particle"></div>
              <div class="particle"></div>
            </div>
          </div>
          <h3>{{ showAllProducts ? 'No hay productos registrados' : 'No hay productos agotados' }}</h3>
          <p>{{ showAllProducts ? 'Comienza agregando tu primer producto' : 'Todos los productos tienen stock disponible'
            }}</p>
          <button v-if="showAllProducts" class="cta-btn" @click="openAddProductModal">
            Agregar Primer Producto
          </button>
        </div>
        
        <div v-if="filteredProducts.length === 0 && searchTerm.length > 0 && !isFetching" class="empty-state">
            <h3>No se encontraron resultados para "{{ searchTerm }}"</h3>
            <p>Intenta con otro nombre o limpia la búsqueda.</p>
        </div>


      </div>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <div class="business-info">
          <h3 class="business-name">🌸 Control AS</h3>
          <div class="business-details">
            <span class="detail-item">✨ Desde 2025</span>
          </div>
        </div>
        <div class="footer-links">
          <div class="copyright">
            <span>© 2025 Control AS. Todos los derechos reservados.</span>
          </div>
        </div>
      </div>
    </footer>

    <div v-if="showAddProductModal || showEditProductModal" class="modal-overlay" @click.self="closeProductFormModal">
      <div class="modal-content-wrapper modal-add-product" @click.stop>
        <div class="modal-header">
          <div class="modal-title">
            <span class="modal-icon">{{ isEditing ? '📝' : '✨' }}</span>
            <h2>{{ isEditing ? 'Editar Producto' : 'Agregar Nuevo Producto' }}</h2>
          </div>
          <button class="close-btn" @click="closeProductFormModal" :disabled="isLoading">
            <span>✖️</span>
          </button>
        </div>

        <form @submit.prevent="isEditing ? saveEditedProduct() : addProduct()" class="product-form">
          <label class="form-label">
            <span class="label-icon">📸</span>
            <span class="label-text">Foto del producto</span>
          </label>
          <div class="form-group image-upload-area">


            <div class="image-preview" v-if="currentProduct.imagen">
              <img :src="currentProduct.imagen" :alt="currentProduct.nombre" />
            </div>

            <div class="file-input-wrapper">
              <label class="file-label" for="file-upload">
                <span class="upload-icon">📂</span>
                Seleccionar desde tu equipo
              </label>
              <input id="file-upload" type="file" @change="handleImageUpload" accept="image/*" class="file-input"
                :required="!isEditing && !currentProduct.imagen" :disabled="isLoading">
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">
              <span class="label-icon">🏷️</span>
              <span class="label-text">Nombre del producto</span>
            </label>
            <input type="text" v-model="currentProduct.nombre" required placeholder="nombre del producto"
              class="form-input" :disabled="isLoading">
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">📦</span>
                <span class="label-text">Cantidad inicial</span>
              </label>
              <input type="number" v-model="currentProduct.cantidad" required min="0" placeholder="0" class="form-input"
                :disabled="isEditing || isLoading">
              <div class="form-hint" v-if="isEditing">La cantidad se edita con los botones de +/- en la tarjeta.</div>
            </div>

            <div class="form-group">
              <label class="form-label">
                <span class="label-icon">💰</span>
                <span class="label-text">Precio</span>
              </label>
              <input type="text" v-model="formattedPrice" @input="formatInputPrice" required placeholder="0.00"
                class="form-input" :disabled="isLoading">
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="closeProductFormModal" :disabled="isLoading">
              <span class="btn-icon">❌</span>
              <span>Cancelar</span>
            </button>
            <button type="submit" class="submit-btn" :disabled="!isFormValid || isLoading">
              <span class="btn-icon">
                <span v-if="isLoading" class="loading-spinner"></span>
                <span v-else>{{ isEditing ? '💾' : '✅' }}</span>
              </span>
              <span>{{ isEditing ? 'Guardar Cambios' : 'Agregar Producto' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showUpdateModal" class="modal-overlay" @click.self="closeUpdateModal">
      <div class="modal-content-wrapper modal-update-quantity" @click.stop>
        <div class="modal-header">
          <div class="modal-title">
            <span class="modal-icon">{{ updateType === 'increase' ? '📈' : '📉' }}</span>
            <h2>{{ updateType === 'increase' ? 'Aumentar Stock' : 'Disminuir Stock' }}</h2>
          </div>
          <button class="close-btn" @click="closeUpdateModal" :disabled="isLoading">
            <span>✖️</span>
          </button>
        </div>

        <div class="update-product-info">
          <div class="product-preview">
            <img :src="selectedProduct?.imagen" :alt="selectedProduct?.nombre" class="preview-image">
            <div class="preview-details">
              <h3 class="preview-name">{{ selectedProduct?.nombre }}</h3>
              <div class="preview-current-stock">
                <span class="stock-label">Stock actual:</span>
                <span class="stock-value">{{ selectedProduct?.cantidad }} unidades</span>
              </div>
            </div>
          </div>
        </div>

        <form @submit.prevent="updateProductQuantity" class="update-form">
          <div class="form-group">
            <label class="form-label">
              <span class="label-icon">{{ updateType === 'increase' ? '➕' : '➖' }}</span>
              <span class="label-text">
                {{ updateType === 'increase' ? 'Cantidad a agregar' : 'Cantidad a quitar' }}
              </span>
            </label>
            <input type="number" v-model="quantityToUpdate" required min="1"
              :max="updateType === 'decrease' ? selectedProduct?.cantidad : undefined" placeholder="1"
              class="form-input quantity-input" :disabled="isLoading">
          </div>

          <div class="quantity-preview">
            <div class="preview-calculation">
              <span class="calculation-current">{{ selectedProduct?.cantidad }}</span>
              <span class="calculation-operator">{{ updateType === 'increase' ? '+' : '-' }}</span>
              <span class="calculation-input">{{ quantityToUpdate || 0 }}</span>
              <span class="calculation-equals">=</span>
              <span class="calculation-result">
                {{ updateType === 'increase'
                  ? (selectedProduct?.cantidad || 0) + (parseInt(quantityToUpdate) || 0)
                  : Math.max(0, (selectedProduct?.cantidad || 0) - (parseInt(quantityToUpdate) || 0))
                }}
              </span>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="closeUpdateModal" :disabled="isLoading">
              <span class="btn-icon">❌</span>
              <span>Cancelar</span>
            </button>
            <button type="submit" class="submit-btn" :class="updateType" :disabled="!isUpdateFormValid || isLoading">
              <span class="btn-icon">
                <span v-if="isLoading" class="loading-spinner"></span>
                <span v-else>{{ updateType === 'increase' ? '📈' : '📉' }}</span>
              </span>
              <span>{{ updateType === 'increase' ? 'Aumentar' : 'Disminuir' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useActiveBarStore } from '@/stores/activeBar';
import axios from 'axios';
import Swal from 'sweetalert2';
import { API_BASE_URL } from '../config/api';
const API_PAGE_LIMIT = 20; // Coincide con el 'limit' por defecto de tu endpoint
// ***********************************************************

export default {
  name: 'Control AS',
  setup() {
    const router = useRouter();
    const activeBarStore = useActiveBarStore();

    const products = ref([]);
    const showAddProductModal = ref(false);
    const showEditProductModal = ref(false);
    const showUpdateModal = ref(false);
    const showAllProducts = ref(true);
    const selectedProduct = ref(null);

    const isLoading = ref(false);
    
    // ** NUEVAS variables para Scroll Infinito **
    const currentPage = ref(0);
    const hasMore = ref(true); // Indica si quedan más productos por cargar
    const isFetching = ref(false); // Bandera para evitar llamadas concurrentes
    // *******************************************


    // --- Funciones de navegación (Sin cambios) ---
    const irAAdministradores = () => { router.push({ name: 'administradores' }); };
    const irhistorial = () => { router.push({ name: 'historial' }); };
    const irAFacturas = () => { router.push({ name: 'facturas' }); };
    const goBack = () => { router.back(); };

    const currentProduct = ref({
      id: null,
      nombre: '',
      precio: 0,
      cantidad: 0,
      imagen: '',
      bar_id: activeBarStore.id,
      estado: 'activo'
    });
    const formattedPrice = ref('');

    const isEditing = computed(() => currentProduct.value.id !== null);
    const updateType = ref('increase');
    const quantityToUpdate = ref(1);

    const searchTerm = ref('');
    // --- Validaciones (Sin cambios) ---
    const isFormValid = computed(() => {
      if (isEditing.value) {
        return !!currentProduct.value.nombre && currentProduct.value.precio > 0;
      }
      return !!currentProduct.value.nombre && currentProduct.value.precio > 0 && !!currentProduct.value.imagen;
    });

    const isUpdateFormValid = computed(() => {
      const quantity = parseInt(quantityToUpdate.value);
      return quantity > 0 &&
        (updateType.value === 'increase' || (selectedProduct.value && quantity <= selectedProduct.value.cantidad));
    });
    const totalInventoryValue = computed(() => {
  return products.value.reduce((total, product) => {
    return total + (product.cantidad * product.precio);
  }, 0);
});
    const loadInitialProducts = async () => {
        currentPage.value = 0;
        products.value = []; // Limpia la lista actual
        hasMore.value = true;
        await fetchProductsByBar(0, true); // Carga la primera página y reemplaza
    }

    /**
     * Carga una página específica de productos.
     * @param {number} page - La página a cargar (0, 1, 2, ...).
     * @param {boolean} [replace=false] - Si es true, reemplaza la lista, si es false, concatena.
     */
    const fetchProductsByBar = async (page = currentPage.value, replace = false) => {
      if (!activeBarStore.id || isFetching.value || (!hasMore.value && !replace)) {
        console.warn("Advertencia: No hay ID de bar, ya está cargando o no hay más productos.");
        return;
      }

      isFetching.value = true;
      const skipValue = page * API_PAGE_LIMIT;
      
      console.log(`Cargando productos - Página: ${page}, Skip: ${skipValue}, Limit: ${API_PAGE_LIMIT}`);

      try {
        const response = await axios.get(`${API_BASE_URL}/productos_por_bar/${activeBarStore.id}`, {
          params: {
            skip: skipValue,
            limit: API_PAGE_LIMIT
          }
        });

        const newProducts = response.data || [];
        
        if (replace) {
            products.value = newProducts; // Reemplaza para la carga inicial o reseteo
        } else {
            products.value = products.value.concat(newProducts); // Concatena para scroll infinito
        }

        // Determina si hay más productos para la próxima llamada
        hasMore.value = newProducts.length === API_PAGE_LIMIT;

        if (hasMore.value) {
            currentPage.value = page + 1; // Prepara el número de la siguiente página
        }
        
        console.log(`Productos cargados. Total: ${products.value.length}. Hay más: ${hasMore.value}`);

      } catch (error) {
        console.error("Error al obtener los productos del bar:", error);
        // Si hay un error, asumimos que no hay más productos para evitar loops
        hasMore.value = false; 
        Swal.fire({
          icon: 'error',
          title: 'Error de conexión',
          text: 'No se pudo cargar el inventario. Por favor, revisa tu conexión e intenta de nuevo.'
        });
      } finally {
        isFetching.value = false;
      }
    };
    
    /**
     * Manejador del evento scroll de la ventana.
     */
    const handleScroll = () => {
      // Calculamos la distancia desde el fondo del viewport
      const nearBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 500; // 500px antes del final
      
      // Solo cargamos si estamos cerca del fondo, hay más productos por cargar y no estamos ya cargando
      if (nearBottom && hasMore.value && !isFetching.value && showAllProducts.value && searchTerm.value === '') {
        fetchProductsByBar(currentPage.value);
      }
    };
    // ----------------------------------------------------------------------------------

    // --- Ciclo de vida ---
    onMounted(() => {
        // Carga inicial de la primera página
        loadInitialProducts();
        
        // Agrega el listener de scroll para el scroll infinito
        window.addEventListener('scroll', handleScroll);
    });

    onUnmounted(() => {
        // Remueve el listener de scroll cuando el componente se destruye
        window.removeEventListener('scroll', handleScroll);
    });

    // --- Lógica de filtrado y conteo (Modificada para usar la paginación solo cuando no hay búsqueda) ---
    const filteredProducts = computed(() => {
      let currentProductsList = products.value;

      // Importante: Si hay un término de búsqueda, se asume que la lista 'products.value'
      // ya tiene todos los productos relevantes cargados (o suficientes para la búsqueda)
      // Si la búsqueda es muy extensiva, deberías implementar paginación también en la búsqueda
      // pero por simplicidad, aquí solo filtramos lo que ya está cargado.

      if (!showAllProducts.value) {
        currentProductsList = currentProductsList.filter(product => product.cantidad === 0);
      }

      if (searchTerm.value) {
        const lowerCaseSearchTerm = searchTerm.value.toLowerCase();
        currentProductsList = currentProductsList.filter(product =>
          product.nombre.toLowerCase().includes(lowerCaseSearchTerm)
        );
      }
      return currentProductsList;
    });

    const soldOutCount = computed(() => {
      // El conteo se hace sobre todos los productos cargados
      return products.value.filter(product => product.cantidad === 0).length;
    });

    const clearSearch = () => {
      searchTerm.value = '';
      // Opcional: Si el scroll infinito se interrumpió por la búsqueda, reiniciar la carga
      // Si el usuario borra la búsqueda y 'products.value' no está completo, recargar.
      if (products.value.length < (currentPage.value * API_PAGE_LIMIT)) {
          loadInitialProducts();
      }
    };
    
    // --- Funciones de UI y Lógica de formularios (Ligeramente modificadas) ---

    const handleImageUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          currentProduct.value.imagen = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };

    const openAddProductModal = () => {
      currentProduct.value = {
        id: null, nombre: '', precio: 0, cantidad: 0, imagen: '',
        bar_id: activeBarStore.id, estado: 'activo'
      };
      formattedPrice.value = '';
      showAddProductModal.value = true;
      showEditProductModal.value = false;
      document.body.style.overflow = 'hidden';
    };

    const openEditProductModal = (product) => {
      currentProduct.value = {
        id: product.id,
        nombre: product.nombre,
        precio: product.precio,
        cantidad: product.cantidad,
        imagen: product.imagen,
        bar_id: product.bar_id,
        estado: product.estado
      };
      formattedPrice.value = product.precio.toLocaleString('es-CO');
      showEditProductModal.value = true;
      showAddProductModal.value = false;
      document.body.style.overflow = 'hidden';
    };

    const closeProductFormModal = () => {
      if (isLoading.value) return;
      showAddProductModal.value = false;
      showEditProductModal.value = false;
      document.body.style.overflow = '';
      resetCurrentProduct();
    };

    const formatInputPrice = () => {
      const numericValue = formattedPrice.value.replace(/\D/g, '');
      if (numericValue) {
        formattedPrice.value = Number(numericValue).toLocaleString('es-CO');
        currentProduct.value.precio = Number(numericValue);
      } else {
        formattedPrice.value = '';
        currentProduct.value.precio = 0;
      }
    };

    const resetCurrentProduct = () => {
      currentProduct.value = {
        id: null,
        nombre: '',
        precio: 0,
        cantidad: 0,
        imagen: '',
        estado: 'activo'
      };
      formattedPrice.value = '';
    };

    const openUpdateModal = (product, type) => {
      selectedProduct.value = product;
      updateType.value = type;
      quantityToUpdate.value = 1;
      showUpdateModal.value = true;
      document.body.style.overflow = 'hidden';
    };

    const closeUpdateModal = () => {
      if (isLoading.value) return;
      showUpdateModal.value = false;
      selectedProduct.value = null;
      quantityToUpdate.value = 1;
      document.body.style.overflow = '';
    };


    // --- Funciones de CRUD (Modificadas para llamar a loadInitialProducts) ---

    const addProduct = async () => {
      if (isLoading.value) return;

      const swalLoading = Swal.fire({
        title: 'Agregando producto...',
        text: 'Por favor, espera un momento.',
        allowOutsideClick: false,
        didOpen: () => { Swal.showLoading(); }
      });

      isLoading.value = true;

      try {
        const newProduct = {
          nombre: currentProduct.value.nombre,
          precio: currentProduct.value.precio,
          cantidad: parseInt(currentProduct.value.cantidad),
          imagen: currentProduct.value.imagen,
          bar_id: currentProduct.value.bar_id
        };

        await axios.post(`${API_BASE_URL}/crear_productos`, newProduct);

        swalLoading.close();
        Swal.fire('¡Producto agregado!', 'El producto se ha añadido a tu inventario.', 'success');

        // ** Importante: Recargar la lista desde la primera página **
        await loadInitialProducts(); 
        
      } catch (error) {
        console.error("Error al agregar el producto:", error);
        const errorMessage = error.response?.data?.detail || 'Hubo un error al agregar el producto. Por favor, intenta de nuevo.';
        swalLoading.close();
        Swal.fire('Error', errorMessage, 'error');
      } finally {
        isLoading.value = false;
        closeProductFormModal();
        document.body.style.overflow = '';
      }
    };

    const saveEditedProduct = async () => {
      if (isLoading.value) return;

      const swalLoading = Swal.fire({
        title: 'Guardando cambios...',
        text: 'Por favor, espera un momento.',
        allowOutsideClick: false,
        didOpen: () => { Swal.showLoading(); }
      });

      isLoading.value = true;

      try {
        const updatedFields = {};
        if (currentProduct.value.nombre) { updatedFields.nombre = currentProduct.value.nombre; }
        if (currentProduct.value.precio) { updatedFields.precio = currentProduct.value.precio; }
        if (currentProduct.value.imagen) { updatedFields.imagen = currentProduct.value.imagen; }

        await axios.patch(`${API_BASE_URL}/actualizar_productos/${currentProduct.value.id}`, updatedFields);

        swalLoading.close();
        Swal.fire('¡Cambios guardados!', 'El producto ha sido actualizado.', 'success');

        // ** Importante: Recargar la lista desde la primera página **
        await loadInitialProducts(); 
        
      } catch (error) {
        console.error("Error al guardar los cambios del producto:", error);
        const errorMessage = error.response?.data?.detail || 'Hubo un error al guardar los cambios. Por favor, intenta de nuevo.';
        swalLoading.close();
        Swal.fire('Error', errorMessage, 'error');
      } finally {
        isLoading.value = false;
        closeProductFormModal();
        document.body.style.overflow = '';
      }
    };


    const updateProductQuantity = async () => {
      if (!isUpdateFormValid.value || isLoading.value) return;

      const swalLoading = Swal.fire({
        title: 'Actualizando stock...',
        text: 'Por favor, espera un momento.',
        allowOutsideClick: false,
        didOpen: () => { Swal.showLoading(); }
      });

      isLoading.value = true;
      const quantity = parseInt(quantityToUpdate.value);
      const productId = selectedProduct.value.id;

      const payload = {
        cantidad: updateType.value === 'increase'
          ? selectedProduct.value.cantidad + quantity
          : selectedProduct.value.cantidad - quantity
      };

      try {
        await axios.patch(`${API_BASE_URL}/actualizar_productos/${productId}`, payload);
        
        // ** Importante: Recargar la lista desde la primera página **
        await loadInitialProducts();

        swalLoading.close();
        Swal.fire({
          title: '¡Stock actualizado!',
          text: 'La cantidad del producto se ha modificado correctamente.',
          icon: 'success'
        });
      } catch (error) {
        console.error("Error al actualizar la cantidad:", error);
        const errorMessage = error.response?.data?.detail || 'Hubo un error al actualizar el stock. Por favor, intenta de nuevo.';
        swalLoading.close();
        Swal.fire({ title: 'Error', text: errorMessage, icon: 'error' });
      } finally {
        isLoading.value = false;
        closeUpdateModal();
        document.body.style.overflow = '';
      }
    };


    const confirmDelete = (product) => {
      selectedProduct.value = product;
      Swal.fire({
        title: '¿Estás seguro?',
        html: `Vas a eliminar el producto **${product.nombre}**.<br>Podrás verlo en el historial si lo necesitas.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, Eliminar producto',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6'
      }).then((result) => {
        if (result.isConfirmed) {
          deleteProduct();
        }
      });
    };

    const deleteProduct = async () => {
      if (selectedProduct.value) {
        try {
          await axios.delete(`${API_BASE_URL}/eliminar_producto/${selectedProduct.value.id}`);
          Swal.fire('¡Eliminado!', `El producto '${selectedProduct.value.nombre}' ha sido marcado como eliminado.`, 'success');
          
          // ** Importante: Recargar la lista desde la primera página **
          await loadInitialProducts();
          
        } catch (error) {
          console.error("Error al eliminar el producto:", error);
          const errorMessage = error.response?.data?.detail || 'Hubo un error al eliminar el producto. Por favor, intenta de nuevo.';
          Swal.fire('Error', errorMessage, 'error');
        }
      }
    };
    
    // Las funciones de formato de fecha no se usan en el template proporcionado, 
    // pero se mantienen por si son necesarias en el futuro.
    const formatDate = (date) => { /* ... */ };
    const formatFullDate = (date) => { /* ... */ };
    const toggleDateDisplay = (productId) => { /* ... */ };


    return {
      products,
      irhistorial,
      irAFacturas,
      filteredProducts,
      soldOutCount,
      showAddProductModal,
      totalInventoryValue,
      showEditProductModal,
      showUpdateModal,
      showAllProducts,
      selectedProduct,
      currentProduct,
      isEditing,
      updateType,
      quantityToUpdate,
      searchTerm,
      activeBarStore,
      irAAdministradores,
      goBack,
      formatDate,
      formatFullDate,
      toggleDateDisplay,
      openAddProductModal,
      openEditProductModal,
      closeProductFormModal,
      addProduct,
      saveEditedProduct,
      openUpdateModal,
      closeUpdateModal,
      updateProductQuantity,
      confirmDelete,
      deleteProduct,
      clearSearch,
      handleImageUpload,
      formattedPrice,
      formatInputPrice,
      isLoading,
      isFormValid,
      isUpdateFormValid,
      
      // ** NUEVAS variables devueltas **
      isFetching,
      hasMore,
      // **********************************
    };
  }
};
</script>
<style scoped>
/* ============================================
   GENERAL STYLES
   ============================================ */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #16213e 100%);
  min-height: 100vh;
  color: #ffffff;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #16213e 100%);
}

/* ============================================
   HEADER STYLES
   ============================================ */
.header {
  background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
  border-bottom: 2px solid #e91e63;
  box-shadow: 0 4px 20px rgba(233, 30, 99, 0.3);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.back-button {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
}

.back-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
}

.logo-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.logo-placeholder {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(233, 30, 99, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(26, 26, 46, 0.8);
}

.logo-placeholder img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.brand-text {
  text-align: left;
}

.brand-name {
  font-size: 2.5rem;
  font-weight: 900;
  background: linear-gradient(135deg, #e91e63, #f06292, #2196f3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 4px 20px rgba(233, 30, 99, 0.5);
  margin: 0;
  letter-spacing: 2px;
}

.glitch {
  position: relative;
  animation: glitch 2s infinite;
}

@keyframes glitch {
  0%, 100% {
    transform: translate(0);
  }
  20% {
    transform: translate(-2px, 2px);
  }
  40% {
    transform: translate(-2px, -2px);
  }
  60% {
    transform: translate(2px, 2px);
  }
  80% {
    transform: translate(2px, -2px);
  }
}

.brand-subtitle {
  color: #b3b3b3;
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 0.5rem;
  letter-spacing: 1px;
}

.nav-buttons {
  display: flex;
  gap: 1rem;
}

.nav-btn {
  background: linear-gradient(135deg, #e91e63, #f06292);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
  white-space: nowrap;
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(233, 30, 99, 0.4);
}

.admin-btn {
  background: linear-gradient(135deg, #673ab7, #9c27b0);
  box-shadow: 0 4px 15px rgba(103, 58, 183, 0.3);
}

.admin-btn:hover {
  box-shadow: 0 6px 20px rgba(103, 58, 183, 0.4);
}

/* ============================================
   MAIN CONTENT
   ============================================ */
.main-content {
  flex: 1;
  padding: 2rem 0;
  background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #16213e 100%);
  min-height: 100vh;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.page-title {
  text-align: center;
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.title-text {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #ffffff, #e91e63);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}

.title-decoration {
  width: 100px;
  height: 4px;
  background: linear-gradient(135deg, #e91e63, #2196f3);
  margin: 0 auto;
  border-radius: 2px;
}

/* ============================================
   INVENTORY TOTAL CARD - CORREGIDO
   ============================================ */
.inventory-total-card {
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
  backdrop-filter: blur(12px);
  border: 2px solid rgba(233, 30, 99, 0.5);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  margin: 2rem auto;
  max-width: 600px;
  box-shadow: 0 12px 40px rgba(233, 30, 99, 0.3);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.inventory-total-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.05) 50%, transparent 70%);
  transform: translateX(-100%);
  transition: transform 0.8s;
}

.inventory-total-card:hover::before {
  transform: translateX(100%);
}

.inventory-total-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(233, 30, 99, 0.5);
  border-color: #e91e63;
}

.total-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 1rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.total-label .icon {
  font-size: 2rem;
  filter: drop-shadow(0 0 10px #e91e63);
  animation: pulse-glow 2s infinite;
}

.total-amount {
  font-size: 3rem;
  font-weight: 900;
  background: linear-gradient(135deg, #e91e63, #f06292, #2196f3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0.5rem 0;
  letter-spacing: -1px;
  text-shadow: 0 4px 20px rgba(233, 30, 99, 0.6);
}

.total-subtitle {
  color: #cccccc;
  font-size: 1.1rem;
  font-weight: 500;
}

@keyframes pulse-glow {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

/* ============================================
   SEARCH AND FILTERS - CORREGIDO
   ============================================ */
.search-and-filters {
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(233, 30, 99, 0.3);
  border-radius: 20px;
  padding: 2rem;
  margin-bottom: 3rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.search-section {
  margin-bottom: 2rem;
}

.search-inputs {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}

.search-input {
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(233, 30, 99, 0.4);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  color: white;
  font-size: 1rem;
  min-width: 200px;
  transition: all 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #e91e63;
  box-shadow: 0 0 20px rgba(233, 30, 99, 0.4);
  background: rgba(26, 26, 46, 0.95);
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.clear-search-btn {
  background: linear-gradient(135deg, #f44336, #e53935);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(244, 67, 54, 0.3);
}

.clear-search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(244, 67, 54, 0.4);
}

.filters {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.filter-btn {
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(233, 30, 99, 0.4);
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: rgba(233, 30, 99, 0.2);
  transform: translateY(-2px);
  border-color: #e91e63;
}

.filter-btn.active {
  background: linear-gradient(135deg, #e91e63, #f06292);
  border-color: #e91e63;
  box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4);
}

.filter-icon {
  font-size: 1.2rem;
}

.filter-count {
  background: rgba(0, 0, 0, 0.3);
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  font-size: 0.85rem;
}

.sold-out-btn.active {
  background: linear-gradient(135deg, #ff9800, #f57c00);
  border-color: #ff9800;
  box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
}

/* ============================================
   PRODUCTS GRID - CORREGIDO
   ============================================ */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.product-card {
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.95) 0%, rgba(22, 33, 62, 0.95) 100%);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(233, 30, 99, 0.3);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(233, 30, 99, 0.3);
  border-color: rgba(233, 30, 99, 0.5);
}

.product-card.sold-out {
  opacity: 0.8;
  border-color: rgba(255, 67, 54, 0.5);
}

.product-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.3);
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent, rgba(0, 0, 0, 0.7));
  display: flex;
  align-items: flex-end;
  padding: 1rem;
}

.product-status {
  background: linear-gradient(135deg, #4caf50, #43a047);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.product-status.out-of-stock {
  background: linear-gradient(135deg, #e53935, #d32f2f);
  color: white;
  text-shadow: 0 0 10px #e53935;
  animation: pulse-red 2s infinite;
}

@keyframes pulse-red {
  0% {
    box-shadow: 0 0 0 0 rgba(229, 57, 53, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(229, 57, 53, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(229, 57, 53, 0);
  }
}

.product-image-edit-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  border: none;
  padding: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  z-index: 10;
}

.product-image-edit-btn:hover {
  background: white;
  transform: scale(1.1);
}

.product-info {
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
}

.product-name {
  font-size: 1.3rem;
  font-weight: 700;
  color: white;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.product-price {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.currency {
  font-size: 1.2rem;
  color: #e91e63;
  font-weight: 600;
}

.amount {
  font-size: 1.8rem;
  font-weight: 800;
  color: #e91e63;
}

.product-details {
  margin-bottom: 1.5rem;
  position: relative;
}

.product-quantity {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.quantity-label {
  color: #b3b3b3;
  font-weight: 500;
}

.quantity-value.available {
  color: #4caf50;
  font-weight: 600;
}

.quantity-value.sold-out-text {
  color: #e53935;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.9rem;
  text-shadow: 0 0 5px #e53935;
}

/* Valor total por producto - CORREGIDO */
.product-total-value {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0.75rem 0 0 0;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(233, 30, 99, 0.3);
  font-size: 0.95rem;
}

.total_jaja {
  color: #b3b3b3;
  font-weight: 500;
}

.total-value {
  color: #e91e63;
  font-weight: 700;
  font-size: 1rem;
}

.product-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: space-between;
}

.action-btn {
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(233, 30, 99, 0.4);
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  height: 40px;
  position: relative;
  overflow: hidden;
}

.action-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(233, 30, 99, 0.3);
  border-radius: 50%;
  transition: width 0.4s ease, height 0.4s ease;
  transform: translate(-50%, -50%);
  z-index: 0;
}

.action-btn:hover::before {
  width: 150px;
  height: 150px;
}

.action-btn span {
  position: relative;
  z-index: 1;
}

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  background: rgba(26, 26, 46, 0.5);
  border-color: rgba(255, 255, 255, 0.2);
}

.action-btn:disabled::before {
  width: 0;
  height: 0;
}

.btn-icon {
  font-size: 1.2rem;
  line-height: 1;
}

.decrease-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #f57c00, #ff9800);
  border-color: #f57c00;
}

.increase-btn:hover {
  background: linear-gradient(135deg, #43a047, #4caf50);
  border-color: #43a047;
}

.delete-btn:hover {
  background: linear-gradient(135deg, #e53935, #f44336);
  border-color: #e53935;
}

.edit-btn:hover {
  background: linear-gradient(135deg, #2196f3, #1976d2);
  border-color: #2196f3;
}

.stock-display {
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(233, 30, 99, 0.4);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  min-width: 60px;
  text-align: center;
}

.stock-number {
  font-weight: 700;
  font-size: 1.1rem;
  color: white;
}

/* ============================================
   FLOATING ADD BUTTON
   ============================================ */
.floating-add-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  background: linear-gradient(135deg, #e91e63, #f06292);
  border: none;
  padding: 1rem 1.5rem;
  border-radius: 50px;
  color: white;
  font-weight: 700;
  font-size: 1.1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(233, 30, 99, 0.5);
  z-index: 999;
  animation: pulse-float 2s ease-in-out infinite;
}

.floating-add-btn:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 12px 35px rgba(233, 30, 99, 0.7);
}

.floating-add-btn .btn-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.floating-add-btn .btn-text {
  font-size: 1rem;
  letter-spacing: 0.5px;
}

@keyframes pulse-float {
  0%, 100% {
    box-shadow: 0 8px 25px rgba(233, 30, 99, 0.5);
  }
  50% {
    box-shadow: 0 8px 35px rgba(233, 30, 99, 0.8);
  }
}

/* ============================================
   LOADING & EMPTY STATES - CORREGIDO
   ============================================ */
.loading-more-products {
  text-align: center;
  padding: 2rem;
  color: #e91e63;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.end-of-list {
  text-align: center;
  padding: 2rem;
  color: #b3b3b3;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.end-icon {
  font-size: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: white;
}

.empty-animation {
  position: relative;
  margin-bottom: 2rem;
  display: inline-block;
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.7;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.empty-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #e91e63;
  border-radius: 50%;
  animation: particle 2s infinite;
}

.particle:nth-child(1) {
  top: 20%;
  left: 20%;
  animation-delay: 0s;
}

.particle:nth-child(2) {
  top: 30%;
  right: 20%;
  animation-delay: 0.5s;
}

.particle:nth-child(3) {
  bottom: 20%;
  left: 50%;
  animation-delay: 1s;
}

@keyframes particle {
  0%, 100% {
    opacity: 0;
    transform: scale(0);
  }
  50% {
    opacity: 1;
    transform: scale(1);
  }
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: white;
}

.empty-state p {
  color: #b3b3b3;
  margin-bottom: 2rem;
}

.cta-btn {
  background: linear-gradient(135deg, #e91e63, #f06292);
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  font-size: 1.1rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
}

.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(233, 30, 99, 0.4);
}

/* ============================================
   FOOTER
   ============================================ */
.footer {
  background: linear-gradient(135deg, #000000 0%, #1a1a2e 100%);
  border-top: 2px solid #e91e63;
  margin-top: auto;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.business-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.business-name {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #e91e63, #f06292);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.business-details {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.detail-item {
  color: #b3b3b3;
  font-size: 0.9rem;
}

.copyright {
  color: #b3b3b3;
  font-size: 0.9rem;
}

/* ============================================
   MODAL STYLES - CORREGIDO
   ============================================ */
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
  z-index: 2000;
  padding: 1rem;
  overflow-y: auto;
  overflow-x: hidden;
  -webkit-overflow-scrolling: touch;
}

.modal-content-wrapper {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border: 2px solid rgba(233, 30, 99, 0.5);
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  overflow-x: hidden;
  animation: modalEnter 0.3s ease-out;
  position: relative;
}

@keyframes modalEnter {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid rgba(233, 30, 99, 0.3);
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.modal-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.modal-icon {
  font-size: 2rem;
}

.modal-title h2 {
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.close-btn {
  background: rgba(26, 26, 46, 0.8);
  border: 1px solid rgba(233, 30, 99, 0.4);
  padding: 0.5rem;
  border-radius: 8px;
  cursor: pointer;
  color: white;
  font-size: 1.2rem;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(233, 30, 99, 0.3);
  transform: scale(1.1);
}

.close-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ============================================
   FORM STYLES
   ============================================ */
.product-form,
.update-form {
  padding: 2rem;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  color: white;
  font-weight: 600;
  font-size: 1rem;
}

.label-icon {
  font-size: 1.2rem;
}

.label-text {
  font-size: 1rem;
}

.form-input {
  width: 100%;
  background: rgba(26, 26, 46, 0.9);
  border: 2px solid rgba(233, 30, 99, 0.4);
  border-radius: 12px;
  padding: 0.75rem 1rem;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  border-color: #e91e63;
  box-shadow: 0 0 20px rgba(233, 30, 99, 0.4);
  background: rgba(26, 26, 46, 1);
}

.form-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background: rgba(26, 26, 46, 0.6);
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-hint {
  font-size: 0.85rem;
  color: #b3b3b3;
  margin-top: 0.5rem;
  font-style: italic;
}

/* ============================================
   IMAGE UPLOAD AREA
   ============================================ */
.image-upload-area {
  border: 2px dashed rgba(233, 30, 99, 0.5);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  background: rgba(26, 26, 46, 0.5);
}

.image-upload-area:hover {
  border-color: #e91e63;
  background: rgba(233, 30, 99, 0.1);
}

.image-preview {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

.image-preview img {
  max-width: 200px;
  max-height: 200px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.file-input-wrapper {
  position: relative;
  display: inline-block;
}

.file-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #2196f3, #1976d2);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(33, 150, 243, 0.3);
  font-weight: 600;
}

.file-label:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(33, 150, 243, 0.4);
}

.file-input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
  width: 0;
  height: 0;
}

.upload-icon {
  font-size: 1.2rem;
}

/* ============================================
   UPDATE MODAL SPECIFIC
   ============================================ */
.update-product-info {
  padding: 0 2rem;
  margin-bottom: 1rem;
}

.product-preview {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: rgba(26, 26, 46, 0.8);
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid rgba(233, 30, 99, 0.3);
}

.preview-image {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.preview-details {
  flex: 1;
}

.preview-name {
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.preview-current-stock {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.stock-label {
  color: #b3b3b3;
  font-size: 0.9rem;
}

.stock-value {
  color: #4caf50;
  font-weight: 600;
  font-size: 0.95rem;
}

.quantity-input {
  text-align: center;
  font-size: 1.3rem;
  font-weight: 700;
}

.quantity-preview {
  background: rgba(26, 26, 46, 0.8);
  padding: 1.5rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  border: 1px solid rgba(233, 30, 99, 0.3);
}

.preview-calculation {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 1.3rem;
  font-weight: 700;
}

.calculation-current,
.calculation-input,
.calculation-result {
  color: white;
  font-size: 1.5rem;
}

.calculation-operator {
  color: #e91e63;
  font-size: 2rem;
  font-weight: 900;
}

.calculation-equals {
  color: #2196f3;
  font-size: 2rem;
  font-weight: 900;
}

.calculation-result {
  background: linear-gradient(135deg, #4caf50, #43a047);
  padding: 0.5rem 1rem;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
}

/* ============================================
   FORM ACTIONS
   ============================================ */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(233, 30, 99, 0.3);
}

.cancel-btn {
  background: rgba(26, 26, 46, 0.8);
  border: 2px solid rgba(233, 30, 99, 0.4);
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: rgba(233, 30, 99, 0.2);
  border-color: #e91e63;
  transform: translateY(-2px);
}

.cancel-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn {
  background: linear-gradient(135deg, #4caf50, #43a047);
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.5);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.submit-btn.decrease {
  background: linear-gradient(135deg, #ff9800, #f57c00);
  box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
}

.submit-btn.decrease:hover {
  box-shadow: 0 6px 20px rgba(255, 152, 0, 0.5);
}

.submit-btn.increase {
  background: linear-gradient(135deg, #4caf50, #43a047);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.4);
}

.submit-btn.increase:hover {
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.5);
}

/* ============================================
   LOADING SPINNER
   ============================================ */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */
@media (max-width: 1200px) {
  .header-content {
    padding: 1.5rem 1rem;
  }

  .container {
    padding: 0 1rem;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }
}

@media (max-width: 900px) {
  .header-content {
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem;
  }

  .nav-buttons {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
  }

  .logo-section {
    flex: none;
    width: 100%;
  }

  .logo-container {
    flex-direction: row;
    gap: 1rem;
    text-align: left;
  }

  .brand-text {
    text-align: left;
  }

  .nav-btn {
    flex: 1;
    min-width: 120px;
    justify-content: center;
  }

  .search-and-filters {
    padding: 1.5rem;
  }

  .search-inputs {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    min-width: auto;
    width: 100%;
  }

  .inventory-total-card {
    max-width: 100%;
    padding: 1.5rem;
  }

  .total-amount {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .header-content {
    padding: 1rem;
  }

  .logo-placeholder {
    width: 60px;
    height: 60px;
  }

  .brand-name {
    font-size: 2rem;
  }

  .brand-subtitle {
    font-size: 0.8rem;
  }

  .nav-btn .btn-text {
    display: none;
  }

  .nav-btn .btn-icon {
    font-size: 1.3rem;
  }

  .nav-btn {
    padding: 0.75rem;
    min-width: auto;
  }

  .floating-add-btn {
    bottom: 1rem;
    right: 1rem;
    padding: 0.75rem 1.25rem;
    font-size: 1rem;
  }

  .floating-add-btn .btn-icon {
    font-size: 1.3rem;
  }

  .floating-add-btn .btn-text {
    font-size: 0.9rem;
  }

  .title-text {
    font-size: 2rem;
  }

  .inventory-total-card {
    padding: 1.25rem;
    margin: 1.5rem auto;
  }

  .total-label {
    font-size: 1.1rem;
  }

  .total-amount {
    font-size: 2.2rem;
  }

  .total-subtitle {
    font-size: 0.95rem;
  }

  .products-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .product-card {
    padding: 0;
  }

  .product-info {
    padding: 1rem;
  }

  .product-actions {
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .action-btn {
    min-width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }

  .stock-display {
    min-width: 50px;
    order: -1;
    flex-grow: 1;
    text-align: center;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }

  .business-details {
    flex-direction: column;
    gap: 0.5rem;
  }

  .modal-content-wrapper {
    margin: 0.5rem;
    max-width: calc(100% - 1rem);
    max-height: calc(100vh - 1rem);
  }

  .modal-header {
    padding: 1.5rem 1rem 1rem;
    position: sticky;
    top: 0;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    z-index: 10;
  }

  .modal-title {
    gap: 0.5rem;
  }

  .modal-title h2 {
    font-size: 1.2rem;
  }

  .modal-icon {
    font-size: 1.5rem;
  }

  .product-form,
  .update-form {
    padding: 1rem;
  }

  .image-upload-area {
    padding: 1.5rem 1rem;
  }

  .image-preview img {
    max-width: 150px;
    max-height: 150px;
  }

  .file-label {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
    gap: 0.75rem;
  }

  .cancel-btn,
  .submit-btn {
    width: 100%;
    justify-content: center;
  }

  .product-preview {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }

  .preview-image {
    width: 80px;
    height: 80px;
  }

  .preview-calculation {
    flex-wrap: wrap;
    gap: 0.5rem;
    font-size: 1.1rem;
  }

  .calculation-current,
  .calculation-input,
  .calculation-result {
    font-size: 1.2rem;
  }

  .calculation-operator,
  .calculation-equals {
    font-size: 1.5rem;
  }
}

/* ============================================
   SCROLLBAR STYLING
   ============================================ */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(26, 26, 46, 0.5);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #e91e63, #f06292);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #c2185b, #e91e63);
}

/* ============================================
   ACCESSIBILITY
   ============================================ */
button:focus-visible,
input:focus-visible {
  outline: 2px solid #e91e63;
  outline-offset: 2px;
}

/* ============================================
   PRINT STYLES
   ============================================ */
@media print {
  .header,
  .footer,
  .modal-overlay,
  .action-btn,
  .search-and-filters,
  .floating-add-btn {
    display: none !important;
  }

  .main-content {
    padding: 0;
  }

  .product-card {
    break-inside: avoid;
    margin-bottom: 1rem;
  }
}

/* ============================================
   SWEETALERT2 Z-INDEX
   ============================================ */
:root {
  --swal2-z-index: 10000;
}
</style>