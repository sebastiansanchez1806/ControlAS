  <template>
    <div class="inventory-modal-overlay">
      <div class="inventory-modal">

        <!-- BOTÓN SALIR -->
        <button @click="cancelAndExit" class="btn-cancel-exit" title="Cancelar y Salir">
          ❌ Salir
        </button>

        <!-- LOADER GLOBAL -->
        <div v-if="cargando" class="global-loader">
          <p>🔄 Cargando productos del bar...</p>
        </div>

        <!-- ==================== VISTA: OPCIONES ==================== -->
        <div v-if="currentView === 'options'" class="view options-view">
          <h2 class="title-question">Gestión de Inventario: ¿Qué deseas hacer?</h2>

          <div class="options-buttons">
            <button
              @click="viewStockManagement"
              class="btn-option blue-option"
              :disabled="cargando || products.length === 0"
            >
              📈 Aumentar Stock Existente
            </button>

            <button @click="currentView = 'adding'" class="btn-option pink-option">
              📦 Agregar Productos Nuevos
            </button>

            <button @click="currentView = 'summary'" class="btn-option black-option">
              📝 (Finalizar)
            </button>
          </div>

          <!-- Mensaje si no hay productos -->
          <div v-if="!cargando && products.length === 0" class="empty-state mt-20">
            <p>⚠️ No hay productos registrados en este bar</p>
            <button @click="cargarProductos" class="btn-primary">Recargar Productos</button>
          </div>

          <!-- Resumen de movimientos pendientes -->
          <div v-if="Object.keys(stockMovements).length > 0 || newProducts.length > 0" class="stock-history-summary">
            <h3>📈 Movimientos Pendientes:</h3>
            <div class="history-scroll-area">
              <div v-if="Object.keys(stockMovements).length > 0">
                <h4>Aumentos de Stock:</h4>
                <div v-for="(movement, id) in stockMovements" :key="id" class="history-item">
                  <div class="item-visuals">
                    <img :src="movement.productImage" :alt="movement.productName" class="product-thumb-sm" />
                    <span class="history-name">{{ movement.productName }}</span>
                  </div>
                  <span class="history-qty-added">+{{ movement.addedQuantity }}</span>
                  <span class="history-details">(Antes: {{ movement.initialQuantity }})</span>
                </div>
              </div>

              <div v-if="newProducts.length > 0" class="mt-15">
                <h4>Productos Nuevos:</h4>
                <div v-for="product in newProducts" :key="product.id" class="history-item new-item">
                  <div class="item-visuals">
                    <img :src="product.image || 'https://via.placeholder.com/24'" :alt="product.name" class="product-thumb-sm" />
                    <span class="history-name">{{ product.name }}</span>
                  </div>
                  <span class="history-qty-added">Stock: {{ product.quantity }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== VISTA: AUMENTAR STOCK ==================== -->
        <div v-else-if="currentView === 'managing'" class="view managing-view">
          <button @click="goBackToOptions" class="btn-back">← Volver a Opciones</button>

          <!-- Sin productos -->
          <div v-if="products.length === 0 && !cargando" class="empty-state full-center">
            <p>⚠️ No hay productos para aumentar stock</p>
            <button @click="cargarProductos" class="btn-primary">Recargar Productos</button>
          </div>

          <!-- Con productos -->
          <div v-else class="product-card">
            <div class="product-image">
              <img
                :src="currentProduct?.image || 'https://via.placeholder.com/150'"
                :alt="currentProduct?.name || 'Sin nombre'"
              />
  logarithmic
            </div>
            <h2 class="product-name">{{ currentProduct?.name || 'Cargando...' }}</h2>
            <p class="product-price">{{ currentProduct ? formatPrice(currentProduct.price) : '$0 COP' }}</p>

            <div class="quantity-section">
              <p class="current-stock">
                Stock antes del aumento:
                <strong>{{ getInitialQuantity(currentProduct?.id) }}</strong>
              </p>
              <div class="input-group">
                <label>Cantidad a agregar:</label>
              <input
    type="number"
    v-model.number="productQuantities[currentProduct?.id]"
    min="0"
    class="quantity-input"
    placeholder="0"
    @input="markProductTouched(currentProduct?.id)"
  />
              </div>
  <p v-if="!productTouched[currentProduct?.id]" class="validation-warning">
    ⚠️ Debes ingresar una cantidad (incluso si es 0) para continuar
  </p>
              <p v-if="(productQuantities[currentProduct?.id] || 0) > 0" class="total-stock">
                Total después:
                <strong class="highlight">
                  {{ getInitialQuantity(currentProduct?.id) + (productQuantities[currentProduct?.id] || 0) }}
                </strong>
              </p>
            </div>

            <div class="navigation-buttons">
              <button @click="goToPrevious" class="btn-secondary" :disabled="currentProductIndex === 0">
                ← Anterior
              </button>
  <button 
    @click="goToNext" 
    class="btn-primary blue-btn"
    :disabled="!canProceedToNext"
  >
    {{ isLastProduct ? 'Guardar y Volver' : 'Siguiente →' }}
  </button>
            </div>

            <div class="progress-indicator">
              Producto {{ currentProductIndex + 1 }} de {{ products.length }}
            </div>
          </div>
        </div>

        <!-- ==================== VISTA: AGREGAR NUEVOS ==================== -->
        <div v-else-if="currentView === 'adding'" class="view adding-view">
          <button @click="goBackToOptions" class="btn-back">← Volver a Opciones</button>
          <h2>Nuevos Productos</h2>

          <div v-if="newProducts.length === 0" class="empty-state">
            <p>Aún no has agregado productos nuevos.</p>
          </div>

          <div v-else class="products-list">
            <div v-for="product in newProducts" :key="product.id" class="product-item">
              <img :src="product.image || 'https://via.placeholder.com/60'" :alt="product.name" class="product-thumb" />
              <div class="product-info">
                <span class="product-item-name">{{ product.name }}</span>
                <span class="product-item-price">{{ formatPrice(product.price) }}</span>
                <span class="product-item-qty">Stock: <strong>{{ product.quantity }}</strong></span>
              </div>
              <div class="product-actions">
                <button @click="editProduct(product)" class="btn-icon" title="Editar">✏️</button>
                <button @click="confirmDelete(product)" class="btn-icon" title="Eliminar">🗑️</button>
              </div>
            </div>
          </div>

          <button @click="showAddForm = true" class="btn-add-main pink-btn">
            + Agregar Nuevo Producto
          </button>

          <!-- Formulario agregar/editar -->
          <div v-if="showAddForm" class="modal-overlay-inner" @click.self="closeAddForm">
            <div class="modal-content">
              <button @click="closeAddForm" class="btn-close">×</button>
              <h3>{{ editingProduct ? 'Editar Producto' : 'Agregar Nuevo Producto' }}</h3>

              <div class="form-group">
                <label class="file-upload-label">
                  <input type="file" @change="handleProductImageUpload" accept="image/*" hidden />
                  <span class="upload-icon">📷</span>
                  <span v-if="!newProduct.imageFile && !newProduct.image" class="file-name-display">Adjuntar Imagen del Producto</span>
                  <span v-else-if="newProduct.imageFile" class="file-name-display">
                    Imagen cargada: <strong>{{ newProduct.imageFile.name }}</strong>
                  </span>
                  <span v-else class="file-name-display">Imagen actual: Vista previa</span>
                </label>
                <div v-if="newProduct.image" class="image-preview">
                  <img :src="newProduct.image" alt="Previsualización" class="product-thumb-preview" />
                </div>
              </div>

              <div class="form-group">
                <label class="letras">Nombre del producto:</label>
                <input v-model="newProduct.name" type="text" placeholder="Ej: aguardiente" class="form-input" />
              </div>
              <div class="form-group">
                <label class="letras">Precio (COP):</label>
                <input v-model="formattedPrice" type="text" placeholder="50.000" class="form-input" @input="handlePriceInput" />
              </div>
              <div class="form-group">
                <label class="letras">Cantidad inicial:</label>
                <input v-model.number="newProduct.quantity" type="number" min="1" placeholder="10" class="form-input" />
              </div>
              <button @click="saveProduct" class="btn-primary-full black-btn">
                {{ editingProduct ? 'Guardar Cambios' : 'Agregar Producto' }}
              </button>
            </div>
          </div>

          <!-- Confirmar eliminación -->
          <div v-if="showDeleteConfirm" class="modal-overlay-inner" @click.self="showDeleteConfirm = false">
            <div class="modal-content confirm-modal">
              <h3>¿Estás seguro?</h3>
              <p>¿Deseas eliminar <strong>{{ productToDelete?.name }}</strong>?</p>
              <div class="confirm-buttons">
                <button @click="showDeleteConfirm = false" class="btn-secondary">Cancelar</button>
                <button @click="deleteProduct" class="btn-delete">Eliminar</button>
              </div>
            </div>
          </div>
        </div>

        <!-- ==================== VISTA: RESUMEN ==================== -->
        <div v-else-if="currentView === 'summary'" class="view summary-view">
          <button @click="goBackToOptions" class="btn-back">← Volver a Opciones</button>
          <h2 class="summary-title">Resumen de Movimiento (Factura) 📝</h2>
          <p class="summary-subtitle">Confirma los cambios de stock y adjunta la factura si es necesario.</p>

          <div class="summary-content">
            <div v-if="Object.keys(stockMovements).length > 0" class="movement-section">
              <h3>Aumento de Stock Existente</h3>
              <div class="movement-list">
                <div v-for="(move, id) in stockMovements" :key="id" class="movement-item">
                  <div class="item-visuals">
                    <img :src="move.productImage" :alt="move.productName" class="product-thumb-sm" />
                    <span class="item-name">{{ move.productName }}</span>
                  </div>
                  <span class="item-detail">
                    Antes: <strong>{{ move.initialQuantity }}</strong> | Aumento: <strong class="added-qty">+{{ move.addedQuantity }}</strong>
                    | Nuevo Total: <strong>{{ move.finalQuantity }}</strong>
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>No se registraron aumentos de stock existente.</p>
            </div>

            <div v-if="newProducts.length > 0" class="movement-section">
              <h3>Productos Nuevos Agregados</h3>
              <div class="movement-list">
                <div v-for="product in newProducts" :key="product.id" class="movement-item new-product-item">
                  <div class="item-visuals">
                    <img :src="product.image || 'https://via.placeholder.com/24'" :alt="product.name" class="product-thumb-sm" />
                    <span class="item-name">{{ product.name }}</span>
                  </div>
                  <span class="item-detail">
                    Precio: {{ formatPrice(product.price) }} | Cantidad Inicial: <strong>{{ product.quantity }}</strong>
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>No se agregaron productos nuevos.</p>
            </div>
          </div>

          <div class="invoice-section">
            <label class="file-upload">
              <input type="file" @change="handleFileUpload" accept="image/*,application/pdf" hidden />
              <span class="upload-icon">📎</span>
              <span v-if="!invoiceFile">Adjuntar factura (opcional)</span>
              <span v-else class="file-name">Factura cargada: {{ invoiceFile.name }}</span>
            </label>
          </div>

          <button @click="finishInventory" class="btn-primary-full pink-btn" :disabled="!hasMovements">
            Confirmar y Finalizar Operación
          </button>
          <p v-if="!hasMovements" class="warning-text">No hay movimientos registrados para finalizar.</p>
        </div>

        <!-- MODALES DE CONFIRMACIÓN Y ÉXITO -->
        <div v-if="showExitConfirm" class="modal-overlay-inner exit-confirm-overlay" @click.self="showExitConfirm = false">
          <div class="modal-content confirm-modal">
            <h3>🚨 ¿Estás seguro de salir?</h3>
            <p>Hay <strong>movimientos de inventario sin finalizar</strong>. Si sales ahora, <strong>perderás todos los cambios</strong>.</p>
            <div class="confirm-buttons">
              <button @click="showExitConfirm = false" class="btn-secondary">Cancelar y Permanecer</button>
              <button @click="confirmExit" class="btn-delete">Sí, Descartar Cambios y Salir</button>
            </div>
          </div>
        </div>

        <div v-if="showFinishConfirm" class="modal-overlay-inner finish-confirm-overlay" @click.self="showFinishConfirm = false">
          <div class="modal-content confirm-modal">
            <h3>✅ ¿Estás seguro de finalizar?</h3>
            <p>Los cambios se aplicarán permanentemente.</p>
            <div class="confirm-buttons">
              <button @click="showFinishConfirm = false" class="btn-secondary">Revisar de Nuevo</button>
              <button @click="confirmFinish" class="btn-success-finish">Confirmar y Aplicar Cambios</button>
            </div>
          </div>
        </div>

        <div v-if="showSuccessMessage" class="success-overlay" @click="handleSuccessClick">
          <div class="success-modal">
            <div class="success-icon">✓</div>
            <h2>{{ successTitle }}</h2>
            <p>El inventario se ha actualizado correctamente.</p>
            <button @click="handleSuccessClick" class="btn-success">Aceptar y Volver</button>
          </div>
        </div>
      </div>
    </div>
  </template>

  <script setup>
  import { ref, computed, onMounted, nextTick } from 'vue'
  import { useAdminStore } from '@/stores/admin'
  import { API_BASE_URL } from '../config/api'

  const emit = defineEmits(['navigate-out'])
  const adminStore = useAdminStore()
  const productTouched = ref({}) // Nuevo estado para rastrear productos tocados
  const cargando = ref(true)
  const currentView = ref('options')
  const currentProductIndex = ref(0)
  const productQuantities = ref({})
  const stockMovements = ref({})
  const initialProductsState = ref([])
  const showAddForm = ref(false)
  const invoiceFile = ref(null)
  const showSuccessMessage = ref(false)
  const successTitle = ref('')
  const editingProduct = ref(null)
  const showDeleteConfirm = ref(false)
  const productToDelete = ref(null)
  const formattedPrice = ref('')
  const showExitConfirm = ref(false)
  const showFinishConfirm = ref(false)

  const products = ref([])
  const newProducts = ref([])

  const newProduct = ref({
    image: '',
    imageFile: null,
    name: '',
    price: '',
    quantity: 0
  })

  function markProductTouched(productId) {
    productTouched.value[productId] = true
  }
  const canProceedToNext = computed(() => {
    const product = currentProduct.value
    if (!product) return false
    return productTouched.value[product.id] === true
  })
  // ==================== CARGA DE PRODUCTOS (con logs claros y útiles) ====================
  async function cargarProductos() {
    console.log('🔄 Cargando productos para bar_id:', adminStore.bar_id)
    cargando.value = true

    if (!adminStore.bar_id) {
      console.error('❌ No hay bar_id en el store')
      alert('Error: No se detectó el bar. Por favor inicia sesión de nuevo.')
      cargando.value = false
      return
    }

    try {
      const res = await fetch(`${API_BASE_URL}/productos_por_bar/${adminStore.bar_id}`)
      console.log('📡 Respuesta del servidor → status:', res.status)

      if (!res.ok) throw new Error(`Error ${res.status}`)

      const data = await res.json()
      console.log('✅ Productos recibidos:', data.length, 'productos')
      console.log('📋 Ejemplo del primer producto:', data[0] || 'ninguno')

      // 🔑 MAPEAR los campos del servidor a los que espera el componente
      products.value = data.map(p => ({
        id: p.id,
        name: p.nombre,
        image: p.imagen,
        quantity: p.cantidad,
        price: p.precio,
        bar_id: p.bar_id
      }))

      console.log('🔄 Productos mapeados:', products.value[0] || 'ninguno')

    } catch (err) {
      console.error('💥 Falló la carga de productos:', err)
      alert('No se pudieron cargar los productos')
      products.value = []
    } finally {
      cargando.value = false
      console.log('🏁 Carga finalizada → products.length:', products.value.length)
    }
  }

  onMounted(async () => {
    console.log('🚀 Componente montado - iniciando carga de productos')
    await cargarProductos()
    startInventory()
  })

  // ==================== EL RESTO DEL CÓDIGO SIN CAMBIOS (solo logs mínimos clave) ====================
  const currentProduct = computed(() => products.value[currentProductIndex.value] || null)
  const isLastProduct = computed(() => currentProductIndex.value >= products.value.length - 1)
  const hasMovements = computed(() => Object.keys(stockMovements.value).length > 0 || newProducts.value.length > 0)

  function getInitialQuantity(productId) {
    const original = initialProductsState.value.find(p => p.id === productId)
    return original ? original.quantity : 0
  }

  function startInventory() {
    initialProductsState.value = products.value.map(p => ({ ...p }))
    products.value.forEach(p => {
      productQuantities.value[p.id] = stockMovements.value[p.id]?.addedQuantity || 0
      productTouched.value[p.id] = false // ✅ Esta línea es la importante
    })
  }

  function viewStockManagement() {
    if (products.value.length === 0) {
      alert('No hay productos registrados en este bar')
      return
    }
    startInventory()
    currentView.value = 'managing'
    currentProductIndex.value = 0
  }

  function goToNext() {
    const product = currentProduct.value
    if (!product) return

    const qty = Math.max(0, productQuantities.value[product.id] || 0)

    if (qty > 0) {
      stockMovements.value[product.id] = {
        id: product.id,
        productName: product.name,
        productImage: product.image,
        initialQuantity: getInitialQuantity(product.id),
        addedQuantity: qty,
        finalQuantity: getInitialQuantity(product.id) + qty
      }
    } else {
      delete stockMovements.value[product.id]
    }

    if (isLastProduct.value) {
      currentView.value = 'options'
    } else {
      currentProductIndex.value++
    }
  }

  function goToPrevious() {
    if (currentProductIndex.value > 0) currentProductIndex.value--
  }

  function goBackToOptions() {
    currentView.value = 'options'
  }

  function finishInventory() {
    if (!hasMovements.value) return
    showFinishConfirm.value = true
  }

  async function confirmFinish() {
    showFinishConfirm.value = false
    const formData = new FormData()
    formData.append('bar_id', adminStore.bar_id)
    formData.append('tipo_usuario', 'administrador')
    formData.append('usuario_id', adminStore.id)

    // ✅ AUMENTOS DE STOCK (sin cambios)
    if (Object.keys(stockMovements.value).length > 0) {
      formData.append('aumentos', JSON.stringify(
        Object.values(stockMovements.value).map(m => ({ producto_id: m.id, cantidad: m.addedQuantity }))
      ))
    }

    // ✅ PRODUCTOS NUEVOS - ENVIAR SIN LA IMAGEN BASE64 EN EL JSON
    if (newProducts.value.length > 0) {
      // Solo enviamos datos básicos (sin imagen base64)
      const productosData = newProducts.value.map((p, index) => ({
        nombre: p.name,
        precio: p.price,
        cantidad: p.quantity,
        index: index  // Identificador para asociar con la imagen
      }))
      formData.append('nuevos', JSON.stringify(productosData))

      // ✅ ENVIAR CADA IMAGEN COMO ARCHIVO SEPARADO
      newProducts.value.forEach((p, i) => {
        if (p.imageFile) {
          // Si hay un archivo seleccionado, enviarlo
          formData.append(`imagen_${i}`, p.imageFile)
        } else if (p.image && p.image.startsWith('data:image')) {
          // Si solo hay base64, convertirlo a Blob
          const blob = dataURLtoBlob(p.image)
          formData.append(`imagen_${i}`, blob, `producto_${i}.jpg`)
        }
      })
    }

    // FACTURA (sin cambios)
    if (invoiceFile.value) formData.append('factura', invoiceFile.value)

    try {
      const res = await fetch(`${API_BASE_URL}/inventario/guardar-con-factura`, {
        method: 'POST',
        body: formData
      })
      if (!res.ok) throw new Error(await res.text())

      successTitle.value = '¡Inventario Actualizado con Éxito!'
      showSuccessMessage.value = true

      // Actualizar stock local
      Object.values(stockMovements.value).forEach(m => {
        const p = products.value.find(x => x.id === m.id)
        if (p) p.quantity = m.finalQuantity
      })
      newProducts.value.forEach(np => {
        products.value.push({ ...np, id: Date.now() + Math.random() })
      })

    } catch (err) {
      console.error('Error guardando inventario:', err)
      alert('Error al guardar: ' + err.message)
    }
  }

  // ✅ FUNCIÓN AUXILIAR: Convertir data URL a Blob
  function dataURLtoBlob(dataURL) {
    const arr = dataURL.split(',')
    const mime = arr[0].match(/:(.*?);/)[1]
    const bstr = atob(arr[1])
    let n = bstr.length
    const u8arr = new Uint8Array(n)
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n)
    }
    return new Blob([u8arr], { type: mime })
  }

  // ==================== FUNCIONES RESTANTES (sin logs molestos) ====================
  function handleSuccessClick() {
    showSuccessMessage.value = false
    resetInventory()
    emit('navigate-out', 'go-back')
  }

  function cancelAndExit() {
    hasMovements.value ? showExitConfirm.value = true : emit('navigate-out', 'go-back')
  }

  function confirmExit() {
    showExitConfirm.value = false
    resetInventory()
    emit('navigate-out', 'go-back')
  }

  function resetInventory() {
    currentView.value = 'options'
    currentProductIndex.value = 0
    productQuantities.value = {}
    stockMovements.value = {}
    initialProductsState.value = []
    showAddForm.value = false
    invoiceFile.value = null
    showSuccessMessage.value = false
    newProducts.value = []
    editingProduct.value = null
    showDeleteConfirm.value = false
    productToDelete.value = null
    formattedPrice.value = ''
    showExitConfirm.value = false
    showFinishConfirm.value = false
  }

  function formatPrice(price) {
    return `$${Number(price || 0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')} COP`
  }

  function handlePriceInput(e) {
    let value = e.target.value.replace(/\D/g, '')
    formattedPrice.value = value ? value.replace(/\B(?=(\d{3})+(?!\d))/g, '.') : ''
    newProduct.value.price = value ? parseInt(value) : ''
  }

  function handleProductImageUpload(e) {
    const file = e.target.files[0]
    if (file) {
      newProduct.value.imageFile = file
      const reader = new FileReader()
      reader.onload = ev => newProduct.value.image = ev.target.result
      reader.readAsDataURL(file)
    }
  }

  function handleFileUpload(e) {
    const file = e.target.files[0]
    if (file) invoiceFile.value = file
  }

  function closeAddForm() {
    showAddForm.value = false
    editingProduct.value = null
    formattedPrice.value = ''
    newProduct.value = { image: '', imageFile: null, name: '', price: '', quantity: 0 }
  }

  function saveProduct() {
    if (!newProduct.value.name || !newProduct.value.price || newProduct.value.quantity < 1) {
      alert('Completa todos los campos')
      return
    }
    const img = newProduct.value.image || 'https://via.placeholder.com/60'

    if (editingProduct.value) {
      const idx = newProducts.value.findIndex(p => p.id === editingProduct.value.id)
      if (idx > -1) {
        newProducts.value[idx] = {
          ...editingProduct.value,
          name: newProduct.value.name,
          price: newProduct.value.price,
          quantity: newProduct.value.quantity,
          image: img,
          imageFile: newProduct.value.imageFile
        }
      }
    } else {
      newProducts.value.push({
        id: Date.now(),
        name: newProduct.value.name,
        price: newProduct.value.price,
        quantity: newProduct.value.quantity,
        image: img,
        imageFile: newProduct.value.imageFile
      })
    }
    closeAddForm()
  }

  function editProduct(product) {
    editingProduct.value = product
    newProduct.value = {
      image: product.image,
      imageFile: null,
      name: product.name,
      price: product.price,
      quantity: product.quantity
    }
    formattedPrice.value = product.price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.')
    showAddForm.value = true
  }

  function confirmDelete(product) {
    productToDelete.value = product
    showDeleteConfirm.value = true
  }

  function deleteProduct() {
    newProducts.value = newProducts.value.filter(p => p.id !== productToDelete.value.id)
    showDeleteConfirm.value = false
    productToDelete.value = null
  }
  </script>
<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.inventory-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 15px;
  animation: fadeInOverlay 0.3s ease;
}

@keyframes fadeInOverlay {
  from { opacity: 0; }
  to { opacity: 1; }
}

.inventory-modal {
  background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%);
  border-radius: 24px;
  padding: 35px;
  max-width: 800px;
  width: 100%;
  min-height: 520px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.9);
  position: relative;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  animation: modalSlideIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  border: 1px solid #404040;
}

@keyframes modalSlideIn {
  from { 
    transform: translateY(-30px) scale(0.95); 
    opacity: 0; 
  }
  to { 
    transform: translateY(0) scale(1); 
    opacity: 1; 
  }
}

.inventory-modal::-webkit-scrollbar {
  width: 8px;
}

.inventory-modal::-webkit-scrollbar-track {
  background: #2d2d2d;
  border-radius: 10px;
}

.inventory-modal::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 10px;
}

.inventory-modal::-webkit-scrollbar-thumb:hover {
  background: #ff69b4;
}

.view {
  min-height: 440px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  animation: viewFadeIn 0.3s ease;
}

@keyframes viewFadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.btn-cancel-exit {
  position: absolute;
  top: 20px;
  right: 20px;
  background: #000000;
  color: #ffffff;
  border: none;
  padding: 10px 18px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.btn-cancel-exit:hover {
  background: #dc3545;
  transform: scale(1.05) translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4);
}

.btn-cancel-exit:active {
  transform: scale(0.98);
}

.global-loader {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.85);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4em;
  z-index: 9999;
  flex-direction: column;
  gap: 10px;
}

.mt-20 { 
  margin-top: 20px; 
}

.mt-15 {
  margin-top: 20px;
}

.full-center { 
  text-align: center; 
  margin-top: 50px; 
}

.options-view {
  padding-top: 25px;
  justify-content: flex-start;
  gap: 30px;
}

.title-question {
  color: #ffffff;
  font-size: clamp(20px, 5vw, 32px);
  font-weight: 800;
  margin-bottom: 35px;
  letter-spacing: -0.5px;
  line-height: 1.3;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  padding: 0 10px;
}

.options-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(200px, 100%), 1fr));
  gap: 20px;
  width: 100%;
  max-width: 700px;
  margin-bottom: 35px;
}

.btn-option {
  border: none;
  border-radius: 18px;
  padding: 35px 20px;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  font-size: clamp(14px, 3vw, 16px);
  font-weight: 700;
  color: #000000;
  position: relative;
  overflow: hidden;
  min-height: 140px;
}

.btn-option::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, transparent 0%, rgba(255,255,255,0.3) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-option:hover::before {
  opacity: 1;
}

.btn-option .icon {
  font-size: clamp(32px, 8vw, 42px);
  margin-bottom: 5px;
  transition: transform 0.3s ease;
}

.btn-option:hover .icon {
  transform: scale(1.15) rotate(5deg);
}

.blue-option {
  background: linear-gradient(145deg, #1e2840 0%, #2a3550 100%);
  border: 3px solid #667eea;
  color: #ffffff;
}

.blue-option:hover {
  background: #667eea;
  color: #ffffff;
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
}

.pink-option {
  background: linear-gradient(145deg, #3d1f30 0%, #4a2838 100%);
  border: 3px solid #ff69b4;
  color: #ffffff;
}

.pink-option:hover {
  background: #ff69b4;
  color: #ffffff;
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(255, 105, 180, 0.6);
}

.black-option {
  background: linear-gradient(145deg, #2d2d2d 0%, #3a3a3a 100%);
  border: 3px solid #555555;
  color: #ffffff;
}

.black-option:hover {
  background: #000000;
  color: #ffffff;
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(255, 255, 255, 0.2);
}

.stock-history-summary {
  width: 100%;
  max-width: 700px;
  background: linear-gradient(145deg, #2d2d2d 0%, #3a3a3a 100%);
  padding: 25px;
  border-radius: 18px;
  text-align: left;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  border: 2px solid #404040;
}

.history-scroll-area {
  max-height: 220px;
  overflow-y: auto;
  padding-right: 10px;
}

.history-scroll-area::-webkit-scrollbar {
  width: 6px;
}

.history-scroll-area::-webkit-scrollbar-thumb {
  background: #ff69b4;
  border-radius: 10px;
}

.stock-history-summary h3 {
  color: #ffffff;
  margin: 0 0 20px 0;
  font-size: clamp(18px, 4vw, 22px);
  font-weight: 800;
  border-bottom: 3px solid #ff69b4;
  padding-bottom: 10px;
}

.stock-history-summary h4 {
  color: #667eea;
  margin: 18px 0 12px 0;
  font-size: clamp(14px, 3vw, 16px);
  font-weight: 700;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 10px;
  border-bottom: 1px solid #404040;
  font-size: clamp(13px, 2.5vw, 15px);
  transition: background 0.2s ease;
  flex-wrap: wrap;
  gap: 8px;
}

.history-item:hover {
  background: rgba(102, 126, 234, 0.15);
  border-radius: 8px;
}

.history-item:last-child {
  border-bottom: none;
}

.item-visuals {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 2;
  min-width: 0;
}

.product-thumb-sm {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
  border: 2px solid #e8e8e8;
}

.history-name {
  font-weight: 700;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-qty-added {
  color: #ff69b4;
  font-weight: 800;
  font-size: clamp(14px, 3vw, 16px);
  flex: 0 0 auto;
  padding: 0 10px;
}

.history-details {
  color: #6c757d;
  font-size: clamp(12px, 2.5vw, 13px);
  flex: 0 0 auto;
  text-align: right;
}

.new-item .history-qty-added {
  color: #4caf50;
}

.managing-view {
  padding-top: 15px;
  gap: 20px;
  width: 100%;
}

.product-card {
  padding: clamp(20px, 5vw, 35px);
  width: 100%;
  max-width: 500px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
  background: linear-gradient(145deg, #2d2d2d 0%, #3a3a3a 100%);
  border-radius: 20px;
  border: 2px solid #404040;
}

.product-image {
  width: 100%;
  height: clamp(180px, 40vw, 240px);
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-image:hover img {
  transform: scale(1.05);
}

.product-name {
  color: #ffffff;
  font-size: clamp(20px, 5vw, 26px);
  font-weight: 800;
  margin-bottom: 10px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
  word-break: break-word;
}

.product-price {
  color: #667eea;
  font-size: clamp(18px, 4vw, 22px);
  font-weight: 700;
  margin-bottom: 25px;
}

.quantity-section {
  padding: clamp(18px, 4vw, 25px);
  border-radius: 16px;
  margin-bottom: 30px;
  background: linear-gradient(145deg, #1a1a1a 0%, #2d2d2d 100%);
  border: 2px solid #404040;
}

.current-stock {
  font-size: clamp(14px, 3vw, 16px);
  color: #cccccc;
  margin-bottom: 20px;
}

.current-stock strong {
  color: #ffffff;
  font-size: clamp(18px, 4vw, 20px);
  font-weight: 800;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 10px;
  font-size: clamp(13px, 3vw, 15px);
}

.quantity-input {
  width: 100%;
  padding: 14px 16px;
  font-size: clamp(16px, 3.5vw, 18px);
  font-weight: 600;
  border: 2px solid #404040;
  border-radius: 12px;
  transition: all 0.3s ease;
  background: #1a1a1a;
  color: #ffffff;
}

.quantity-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2);
  background: #2d2d2d;
}

.total-stock {
  font-size: clamp(15px, 3.5vw, 17px);
  color: #cccccc;
  margin-top: 15px;
}

.highlight {
  color: #ff69b4;
  font-size: clamp(20px, 5vw, 24px);
  font-weight: 900;
}

.btn-back {
  background: #2d2d2d;
  color: #ffffff;
  border: 2px solid #404040;
  padding: 10px 20px;
  border-radius: 50px;
  font-size: clamp(13px, 2.5vw, 14px);
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: flex-start;
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 15px;
}

.btn-back:hover {
  background: #3a3a3a;
  color: #667eea;
  transform: translateX(-3px);
  border-color: #667eea;
}

.navigation-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  padding: clamp(12px, 3vw, 16px) clamp(24px, 5vw, 32px);
  font-size: clamp(14px, 3vw, 16px);
  font-weight: 800;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex: 1;
  max-width: 200px;
  min-width: 140px;
}

.btn-primary {
  background: #000000;
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-secondary {
  background: #f8f9fa;
  color: #000000;
  border: 2px solid #e0e0e0;
}

.blue-btn:hover {
  background: #667eea;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.btn-secondary:hover {
  background: #e9ecef;
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
}

.progress-indicator {
  text-align: center;
  color: #6c757d;
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 600;
  margin-top: 15px;
}

.adding-view {
  padding-top: 15px;
  width: 100%;
  max-width: 700px;
  gap: 20px;
}

.adding-view h2 {
  color: #ffffff;
  font-size: clamp(22px, 5vw, 28px);
  font-weight: 800;
  margin-bottom: 20px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}

.empty-state {
  padding: 40px 20px;
  background: #2d2d2d;
  border-radius: 16px;
  border: 2px dashed #404040;
  width: 100%;
  margin-bottom: 20px;
}

.empty-state p {
  color: #999999;
  font-size: clamp(14px, 3vw, 16px);
  font-weight: 600;
}

.products-list {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 25px;
  width: 100%;
  padding: 15px;
  background: #2d2d2d;
  border-radius: 16px;
  border: 2px solid #404040;
}

.products-list::-webkit-scrollbar {
  width: 8px;
}

.products-list::-webkit-scrollbar-thumb {
  background: #ff69b4;
  border-radius: 10px;
}

.product-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 18px;
  background: #1a1a1a;
  border-radius: 14px;
  margin-bottom: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  border: 2px solid #2d2d2d;
  flex-wrap: wrap;
}

.product-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
  border-color: #ff69b4;
}

.product-thumb {
  width: clamp(50px, 12vw, 70px);
  height: clamp(50px, 12vw, 70px);
  border-radius: 12px;
  object-fit: cover;
  flex-shrink: 0;
  border: 2px solid #e8e8e8;
}

.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 5px;
  min-width: 0;
}

.product-item-name {
  font-weight: 800;
  color: #ffffff;
  font-size: clamp(14px, 3vw, 16px);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-item-price {
  color: #667eea;
  font-weight: 700;
  font-size: clamp(13px, 2.8vw, 15px);
}

.product-item-qty {
  color: #cccccc;
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 600;
}

.product-item-qty strong {
  color: #ff69b4;
  font-weight: 800;
}

.product-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.btn-icon {
  background: #2d2d2d;
  border: 2px solid #404040;
  width: clamp(36px, 8vw, 40px);
  height: clamp(36px, 8vw, 40px);
  border-radius: 10px;
  font-size: clamp(16px, 3.5vw, 18px);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-icon:hover {
  transform: scale(1.1);
  border-color: #667eea;
  background: #3a3a3a;
}

.btn-add-main {
  width: 100%;
  padding: clamp(14px, 3.5vw, 18px);
  background: #000000;
  color: #ffffff;
  border: none;
  border-radius: 50px;
  font-size: clamp(15px, 3.5vw, 17px);
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.pink-btn:hover {
  background: #ff69b4;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(255, 105, 180, 0.4);
}

.modal-overlay-inner {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1010;
  padding: 20px;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: #ffffff;
  border-radius: 20px;
  padding: clamp(25px, 5vw, 40px);
  max-width: 500px;
  width: 100%;
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  animation: modalPopIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modalPopIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-content::-webkit-scrollbar {
  width: 6px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 10px;
}

.btn-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #2d2d2d;
  border: 2px solid #404040;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 700;
}

.btn-close:hover {
  background: #dc3545;
  color: #ffffff;
  border-color: #dc3545;
  transform: rotate(90deg);
}
.validation-warning {
  color: #ff9800;
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 700;
  margin-top: 12px;
  padding: 10px 14px;
  background: rgba(255, 152, 0, 0.15);
  border-left: 4px solid #ff9800;
  border-radius: 8px;
  animation: pulseWarning 2s ease-in-out infinite;
}

@keyframes pulseWarning {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

button:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
  background: #555555 !important;
}
.modal-content h3 {
  color: #5f5f5f;
  font-size: clamp(20px, 4.5vw, 24px);
  font-weight: 800;
  margin-bottom: 25px;
  text-align: center;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  padding-right: 30px;
}

.form-group {
  margin-bottom: 22px;
}

.form-group label {
  display: block;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 10px;
  font-size: clamp(13px, 3vw, 15px);
}

.letras {
  background-color: #000000;
  padding: 8px 12px;
  border-radius: 8px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  font-size: clamp(14px, 3vw, 16px);
  font-weight: 600;
  border: 2px solid #404040;
  border-radius: 12px;
  transition: all 0.3s ease;
  background: #1a1a1a;
  color: #ffffff;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.2);
  background: #2d2d2d;
}

.file-upload-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  border: 3px dashed #ff69b4;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #ff69b4;
  font-weight: 700;
  background: #fff5fa;
  font-size: clamp(13px, 2.8vw, 15px);
  text-align: center;
  flex-wrap: wrap;
}

.file-upload-label:hover {
  background: #ffe8f5;
  border-color: #ff1493;
  transform: scale(1.02);
}

.upload-icon {
  font-size: clamp(20px, 4vw, 24px);
}

.file-name-display {
  color: #cccccc;
  font-weight: 600;
  word-break: break-word;
}

.image-preview {
  text-align: center;
  margin-top: 15px;
}

.product-thumb-preview {
  width: clamp(100px, 25vw, 120px);
  height: clamp(100px, 25vw, 120px);
  border-radius: 12px;
  object-fit: cover;
  border: 3px solid #ff69b4;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.2);
}

.btn-primary-full {
  width: 100%;
  padding: clamp(14px, 3.5vw, 18px);
  background: #000000;
  color: #ffffff;
  border: none;
  border-radius: 50px;
  font-size: clamp(15px, 3.5vw, 18px);
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-top: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.black-btn:hover {
  background: #667eea;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

.summary-view {
  padding-top: 15px;
  width: 100%;
  max-width: 700px;
  gap: 20px;
}

.summary-title {
  color: #ffffff;
  font-size: clamp(22px, 5vw, 28px);
  font-weight: 800;
  text-align: center;
  margin-bottom: 10px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}

.summary-subtitle {
  color: #999999;
  font-size: clamp(14px, 3vw, 16px);
  text-align: center;
  margin-bottom: 30px;
  font-weight: 600;
  padding: 0 10px;
}

.summary-content {
  width: 100%;
  max-height: 320px;
  overflow-y: auto;
  padding: 15px;
  margin-bottom: 25px;
  background: #2d2d2d;
  border-radius: 16px;
  border: 2px solid #404040;
}

.summary-content::-webkit-scrollbar {
  width: 8px;
}

.summary-content::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 10px;
}

.movement-section {
  margin-bottom: 30px;
  background: #1a1a1a;
  padding: 20px;
  border-radius: 14px;
  border: 2px solid #404040;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
}

.movement-section h3 {
  color: #667eea;
  border-bottom: 3px solid #667eea;
  padding-bottom: 10px;
  margin: 0 0 18px 0;
  font-size: clamp(16px, 3.5vw, 19px);
  font-weight: 800;
}

.movement-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.movement-item {
  display: flex;
  flex-direction: column;
  padding: 14px;
  border: 2px solid #2d2d2d;
  border-radius: 12px;
  background: #252525;
  transition: all 0.3s ease;
}

.movement-item:hover {
  border-color: #667eea;
  background: #2d2d2d;
  transform: translateX(3px);
}

.movement-item .item-visuals {
  justify-content: flex-start;
  margin-bottom: 8px;
}

.item-name {
  font-weight: 800;
  color: #ffffff;
  font-size: clamp(14px, 3vw, 16px);
  word-break: break-word;
}

.item-detail {
  font-size: clamp(12px, 2.5vw, 14px);
  color: #cccccc;
  text-align: left;
  padding-left: clamp(35px, 8vw, 48px);
  font-weight: 600;
  word-break: break-word;
}

.added-qty {
  color: #ff69b4;
  font-weight: 900;
}

.new-product-item {
  border-color: #ffe8f5;
}

.new-product-item:hover {
  border-color: #ff69b4;
  background: #fff5fa;
}

.new-product-item .item-name {
  color: #ff69b4;
}

.invoice-section {
  margin-bottom: 25px;
  width: 100%;
}

.file-upload {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: clamp(14px, 3.5vw, 18px);
  border: 3px dashed #667eea;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #667eea;
  font-weight: 700;
  background: #f0f4ff;
  font-size: clamp(13px, 2.8vw, 15px);
  text-align: center;
  flex-wrap: wrap;
}

.file-upload:hover {
  background: #e8eeff;
  border-color: #4c63d2;
  transform: scale(1.02);
}

.file-name {
  color: #ff69b4;
  font-weight: 800;
  word-break: break-word;
}

.warning-text {
  color: #dc3545;
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: 700;
  margin-top: 15px;
  text-align: center;
}

.confirm-modal {
  text-align: center;
  padding: clamp(25px, 5vw, 35px);
}

.confirm-modal h3 {
  font-size: clamp(20px, 4.5vw, 26px);
  margin-bottom: 20px;
}

.confirm-modal p {
  margin-bottom: 30px;
  color: #333333;
  line-height: 1.6;
  font-size: clamp(14px, 3vw, 16px);
  font-weight: 600;
  padding: 0 10px;
}

.confirm-modal strong {
  font-weight: 800;
}

.confirm-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  flex-wrap: wrap;
}

.confirm-buttons .btn-secondary {
  background: #f8f9fa;
  color: #000000;
  border: 2px solid #e0e0e0;
  padding: clamp(12px, 3vw, 14px) clamp(20px, 4vw, 28px);
  border-radius: 50px;
  font-weight: 800;
  font-size: clamp(13px, 2.8vw, 15px);
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  min-width: clamp(120px, 30vw, 150px);
}

.confirm-buttons .btn-secondary:hover {
  background: #e9ecef;
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
}

.confirm-buttons .btn-delete {
  background: #dc3545;
  color: #ffffff;
  padding: clamp(12px, 3vw, 14px) clamp(20px, 4vw, 28px);
  border: none;
  border-radius: 50px;
  font-weight: 800;
  font-size: clamp(13px, 2.8vw, 15px);
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  min-width: clamp(120px, 30vw, 150px);
  box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
}

.confirm-buttons .btn-delete:hover {
  background: #c82333;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4);
}

.exit-confirm-overlay .modal-content {
  max-width: 520px;
  padding: clamp(25px, 5vw, 35px);
}

.exit-confirm-overlay h3 {
  color: #dc3545;
  font-size: clamp(20px, 4.5vw, 26px);
  margin-bottom: 20px;
  font-weight: 800;
}

.exit-confirm-overlay p {
  margin-bottom: 30px;
  color: #333333;
  line-height: 1.6;
}

.exit-confirm-overlay strong {
  font-weight: 800;
  color: #dc3545;
}

.finish-confirm-overlay .modal-content {
  max-width: 520px;
  padding: clamp(25px, 5vw, 35px);
}

.finish-confirm-overlay h3 {
  color: #4caf50;
  font-size: clamp(20px, 4.5vw, 26px);
  margin-bottom: 20px;
  font-weight: 800;
}

.finish-confirm-overlay p {
  margin-bottom: 30px;
  color: #333333;
  line-height: 1.6;
}

.finish-confirm-overlay strong {
  font-weight: 800;
  color: #4caf50;
}

.btn-success-finish {
  background: #4caf50;
  color: #ffffff;
  padding: clamp(12px, 3vw, 14px) clamp(20px, 4vw, 28px);
  border: none;
  border-radius: 50px;
  font-weight: 800;
  font-size: clamp(13px, 2.8vw, 15px);
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  min-width: clamp(120px, 30vw, 150px);
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.btn-success-finish:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
}

.success-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.92);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  animation: fadeIn 0.3s ease;
  padding: 20px;
}

.success-modal {
  background: #ffffff;
  border-radius: 24px;
  padding: clamp(40px, 8vw, 60px) clamp(30px, 6vw, 50px);
  text-align: center;
  max-width: 450px;
  width: 90%;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.5);
  animation: successBounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes successBounceIn {
  0% { 
    transform: scale(0.3); 
    opacity: 0; 
  }
  50% { 
    transform: scale(1.05); 
  }
  70% { 
    transform: scale(0.95); 
  }
  100% { 
    transform: scale(1); 
    opacity: 1; 
  }
}

.success-icon {
  width: clamp(65px, 15vw, 90px);
  height: clamp(65px, 15vw, 90px);
  background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: clamp(36px, 8vw, 52px);
  font-weight: 900;
  margin: 0 auto 30px;
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
  animation: successPulse 0.8s ease infinite alternate;
}

@keyframes successPulse {
  0% { 
    transform: scale(1); 
    box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
  }
  100% { 
    transform: scale(1.05); 
    box-shadow: 0 12px 35px rgba(76, 175, 80, 0.6);
  }
}

.success-modal h2 {
  color: #000000;
  font-size: clamp(22px, 5vw, 28px);
  font-weight: 800;
  margin-bottom: 15px;
  padding: 0 10px;
}

.success-modal p {
  color: #6c757d;
  font-size: clamp(14px, 3vw, 16px);
  font-weight: 600;
  margin-bottom: 35px;
  line-height: 1.5;
  padding: 0 10px;
}

.btn-success {
  padding: clamp(14px, 3.5vw, 16px) clamp(35px, 7vw, 45px);
  background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
  color: #ffffff;
  border: none;
  border-radius: 50px;
  font-size: clamp(15px, 3.5vw, 17px);
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
}

.btn-success:hover {
  background: linear-gradient(135deg, #45a049 0%, #3d8b40 100%);
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(76, 175, 80, 0.5);
}

.btn-success:active {
  transform: translateY(-1px);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.product-item,
.history-item,
.movement-item {
  animation: fadeInUp 0.3s ease;
}

button:focus-visible,
input:focus-visible {
  outline: 3px solid #667eea;
  outline-offset: 2px;
}

/* ============================================
   MEDIA QUERIES PARA MOBILE
   ============================================ */

@media (max-width: 768px) {
  .inventory-modal-overlay {
    padding: 10px;
  }

  .inventory-modal {
    padding: 25px 20px;
    max-width: 100%;
    min-height: auto;
    border-radius: 20px;
  }

  .btn-cancel-exit {
    top: 12px;
    right: 12px;
    padding: 8px 14px;
    font-size: 13px;
  }

  .options-view {
    padding-top: 15px;
    gap: 20px;
  }

  .title-question {
    margin-bottom: 25px;
  }

  .options-buttons {
    gap: 15px;
  }

  .btn-option {
    padding: 25px 15px;
    min-height: 120px;
  }

  .stock-history-summary {
    padding: 20px;
  }

  .history-scroll-area {
    max-height: 180px;
  }

  .history-item {
    padding: 10px 8px;
  }

  .product-card {
    padding: 25px 20px;
  }

  .quantity-section {
    padding: 20px;
  }

  .navigation-buttons {
    flex-direction: column;
    gap: 12px;
  }

  .btn-primary,
  .btn-secondary {
    max-width: 100%;
    width: 100%;
  }

  .products-list {
    max-height: 250px;
    padding: 12px;
  }

  .product-item {
    padding: 15px;
    gap: 12px;
  }

  .product-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .summary-content {
    max-height: 280px;
    padding: 12px;
  }

  .movement-section {
    padding: 15px;
  }

  .movement-item {
    padding: 12px;
  }

  .confirm-buttons {
    flex-direction: column;
    gap: 12px;
  }

  .confirm-buttons .btn-secondary,
  .confirm-buttons .btn-delete,
  .btn-success-finish {
    width: 100%;
    min-width: auto;
    max-width: 100%;
  }

  .modal-content {
    max-width: 95%;
  }
}

@media (max-width: 480px) {
  .inventory-modal {
    padding: 20px 15px;
    border-radius: 18px;
  }

  .btn-cancel-exit {
    top: 10px;
    right: 10px;
    padding: 7px 12px;
    font-size: 12px;
  }

  .options-view {
    padding-top: 10px;
    gap: 15px;
  }

  .title-question {
    margin-bottom: 20px;
  }

  .options-buttons {
    gap: 12px;
  }

  .btn-option {
    padding: 20px 12px;
    min-height: 110px;
    gap: 8px;
  }

  .stock-history-summary {
    padding: 15px;
  }

  .history-scroll-area {
    max-height: 150px;
  }

  .history-item {
    padding: 8px 6px;
    gap: 6px;
  }

  .product-thumb-sm {
    width: 32px;
    height: 32px;
  }

  .product-card {
    padding: 20px 15px;
  }

  .quantity-section {
    padding: 15px;
  }

  .navigation-buttons {
    gap: 10px;
  }

  .products-list {
    max-height: 220px;
    padding: 10px;
  }

  .product-item {
    padding: 12px;
  }

  .summary-content {
    max-height: 240px;
    padding: 10px;
  }

  .movement-section {
    padding: 12px;
  }

  .movement-item {
    padding: 10px;
  }

  .confirm-modal {
    padding: 20px;
  }

  .success-modal {
    padding: 35px 20px;
  }

  .modal-content {
    max-width: 100%;
  }

  .global-loader {
    font-size: 1.1em;
  }
}

@media (max-width: 360px) {
  .inventory-modal {
    padding: 15px 12px;
  }

  .btn-cancel-exit {
    padding: 6px 10px;
    font-size: 11px;
  }

  .btn-option {
    padding: 18px 10px;
    min-height: 100px;
  }

  .stock-history-summary {
    padding: 12px;
  }

  .product-card {
    padding: 15px 12px;
  }

  .quantity-section {
    padding: 12px;
  }

  .products-list {
    padding: 8px;
  }

  .product-item {
    padding: 10px;
  }

  .summary-content {
    padding: 8px;
  }

  .movement-section {
    padding: 10px;
  }

  .confirm-modal {
    padding: 15px;
  }

  .success-modal {
    padding: 30px 15px;
  }
}

/* ============================================
   LANDSCAPE MOBILE
   ============================================ */

@media (max-height: 600px) and (orientation: landscape) {
  .inventory-modal {
    max-height: 95vh;
    padding: 20px;
  }

  .title-question {
    margin-bottom: 15px;
  }

  .options-buttons {
    gap: 12px;
  }

  .btn-option {
    padding: 15px 12px;
    min-height: 80px;
  }

  .stock-history-summary {
    padding: 15px;
  }

  .history-scroll-area {
    max-height: 120px;
  }

  .product-image {
    height: 150px;
  }

  .quantity-section {
    padding: 15px;
    margin-bottom: 20px;
  }

  .products-list {
    max-height: 180px;
  }

  .summary-content {
    max-height: 200px;
  }

  .success-modal {
    padding: 30px 25px;
  }

  .success-icon {
    width: 60px;
    height: 60px;
    font-size: 32px;
    margin-bottom: 20px;
  }

  .success-modal h2 {
    margin-bottom: 10px;
  }

  .success-modal p {
    margin-bottom: 20px;
  }
}

/* ============================================
   TABLETS
   ============================================ */

@media (min-width: 481px) and (max-width: 768px) {
  .inventory-modal {
    padding: 30px 25px;
    max-width: 95%;
  }

  .options-buttons {
    grid-template-columns: repeat(auto-fit, minmax(min(180px, 100%), 1fr));
  }

  .btn-option {
    min-height: 130px;
  }

  .product-card {
    max-width: 100%;
  }

  .navigation-buttons {
    flex-direction: row;
  }

  .btn-primary,
  .btn-secondary {
    max-width: 48%;
  }

  .confirm-buttons {
    flex-direction: row;
  }

  .confirm-buttons .btn-secondary,
  .confirm-buttons .btn-delete,
  .btn-success-finish {
    min-width: 140px;
    max-width: 48%;
  }
}

/* ============================================
   ACCESIBILIDAD Y PRINT
   ============================================ */

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

@media print {
  .btn-cancel-exit,
  .btn-back,
  .navigation-buttons,
  .btn-add-main,
  .product-actions,
  .invoice-section,
  .confirm-buttons {
    display: none !important;
  }

  .inventory-modal-overlay {
    background: white;
  }

  .inventory-modal {
    box-shadow: none;
    max-width: 100%;
    background: white;
    color: black;
  }

  .summary-content {
    max-height: none;
    overflow: visible;
  }

  .movement-section {
    page-break-inside: avoid;
  }
}

/* ============================================
   SOPORTE PARA PANTALLAS TOUCH
   ============================================ */

@media (hover: none) and (pointer: coarse) {
  .btn-option:hover,
  .btn-primary:hover,
  .btn-secondary:hover,
  .btn-back:hover,
  .btn-icon:hover,
  .file-upload-label:hover,
  .file-upload:hover {
    transform: none;
  }

  .btn-option:active,
  .btn-primary:active,
  .btn-secondary:active {
    transform: scale(0.98);
  }

  button,
  .btn-option,
  .btn-primary,
  .btn-secondary,
  .btn-icon {
    min-height: 44px;
    min-width: 44px;
  }
}
</style>