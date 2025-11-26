<template>
  <div class="valka-history-container">
    <header class="valka-header">
      <h1 class="header-title">{{ activeBarStore.name }}</h1>
      <p class="header-subtitle">
  El historial de la nevera se borrará el primer día de cada mes a las 3:00 a.m. y se enviará a tu correo.
</p>

      <div class="search-container">
        <input
          v-model="searchTerm"
          type="text"
          placeholder="Buscar por mensaje, tipo o fecha..."
          class="search-input"
        />
      </div>
    </header>

    <main class="history-main">
      <hr />

      <div v-if="isLoading" class="loading-message">
        <p>Cargando historial...</p>
      </div>

      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>

      <div v-else-if="!activeBarStore.id" class="error-message">
        <p>No se pudo encontrar la información del bar.</p>
      </div>

      <div v-else-if="history.length === 0" class="empty-history-full">
        <p>No tienes historial disponible.</p>
      </div>

      <div v-else-if="filteredHistory.length === 0" class="empty-history">
        <p>No se encontraron resultados para tu búsqueda.</p>
      </div>

      <div v-else class="history-list">
        <div v-for="item in filteredHistory" :key="item.id" class="history-item">
          <div class="history-content">
            <p class="history-message" :class="`message-${item.tipo}`">
              {{ item.mensaje }}
            </p>
            <span
              class="history-timestamp"
              :title="formatFullDate(item.tiempo)"
            >
              {{ formatTimestamp(item.tiempo) }}
            </span>
          </div>
        </div>

        <div class="pagination-controls">
          <button @click="prevPage" :disabled="currentPage === 0" class="pagination-button">
            Anterior
          </button>
          <span class="pagination-page-info">Página {{ currentPage + 1 }}</span>
          <button @click="nextPage" :disabled="!hasMoreHistory" class="pagination-button">
            Siguiente
          </button>
        </div>
      </div>
    </main>

    <footer class="valka-footer">
      <p>&copy; 2025 Control AS Bar. Todos los derechos reservados.</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useActiveBarStore } from '@/stores/activeBar';
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2'; // Importar SweetAlert2
// *** 1. IMPORTACIÓN DE LA CONSTANTE GLOBAL CON RUTA RELATIVA ***
import { API_BASE_URL } from '../config/api';
// *************************************************************

const router = useRouter();
const activeBarStore = useActiveBarStore();

const history = ref([]);
const searchTerm = ref('');
const isLoading = ref(true);
const error = ref(null);

const currentPage = ref(0);
const pageSize = 10;
const hasMoreHistory = ref(true);



const confirmDelete = async () => {
  if (!activeBarStore.id) {
    console.error('ID del bar no disponible. No se puede borrar el historial.');
    return;
  }
  console.log('Iniciando borrado manual y envío de email...');
  try {
    // *** USO DE LA CONSTANTE GLOBAL (API_BASE_URL) ***
    const response = await fetch(`${API_BASE_URL}/historial/bar/${activeBarStore.id}/eliminar-y-enviar-email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }
    history.value = [];
    currentPage.value = 0;
    hasMoreHistory.value = true;
    fetchHistory();
    console.log('Historial borrado y email enviado con éxito.');
    Swal.fire({
      title: '¡Eliminado!',
      text: 'Tu historial ha sido eliminado y enviado a tu correo.',
      icon: 'success',
      background: '#1a1a1a',
      color: '#fff',
      confirmButtonColor: '#57a8f5',
    });
  } catch (err) {
    console.error('Error al borrar el historial:', err);
    error.value = 'Hubo un error al borrar el historial.';
    Swal.fire({
      title: 'Error',
      text: 'Hubo un error al intentar eliminar el historial.',
      icon: 'error',
      background: '#1a1a1a',
      color: '#fff',
      confirmButtonColor: '#ef4444',
    });
  }
};

const fetchHistory = async () => {
  if (!activeBarStore.id) {
    console.error('ID del bar no disponible.');
    error.value = 'No se pudo cargar el historial. El ID del bar no está disponible.';
    isLoading.value = false;
    return;
  }
  isLoading.value = true;
  error.value = null;
  try {
    const skip = currentPage.value * pageSize;
    // *** USO DE LA CONSTANTE GLOBAL (API_BASE_URL). Se corrige el error de URL aquí. ***
    const response = await fetch(`${API_BASE_URL}/historial/bar/${activeBarStore.id}?skip=${skip}&limit=${pageSize}`);
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }
    const data = await response.json();
    history.value = data;
    if (data.length < pageSize) {
      hasMoreHistory.value = false;
    } else {
      hasMoreHistory.value = true;
    }
  } catch (err) {
    console.error('Error al obtener el historial:', err);
    error.value = 'Hubo un error al cargar el historial. Por favor, inténtalo de nuevo más tarde.';
    history.value = [];
    hasMoreHistory.value = false;
  } finally {
    isLoading.value = false;
  }
};

const nextPage = () => {
  if (hasMoreHistory.value) {
    currentPage.value++;
    fetchHistory();
  }
};

const prevPage = () => {
  if (currentPage.value > 0) {
    currentPage.value--;
    fetchHistory();
  }
};

onMounted(() => {
  fetchHistory();
});

watch(() => activeBarStore.id, (newId, oldId) => {
  if (newId !== oldId && newId) {
    currentPage.value = 0;
    hasMoreHistory.value = true;
    fetchHistory();
  }
});

const sortedHistory = computed(() => {
  if (!history.value) return [];
  return history.value;
});

const filteredHistory = computed(() => {
  const query = searchTerm.value.toLowerCase().trim();
  if (!query) {
    return sortedHistory.value;
  }
  return sortedHistory.value.filter(item => {
    return (
      item.mensaje.toLowerCase().includes(query) ||
      item.tipo.toLowerCase().includes(query) ||
      formatFullDate(item.tiempo).toLowerCase().includes(query)
    );
  });
});

const goBack = () => {
  router.back();
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  const now = new Date();
  const diffInSeconds = Math.floor((now - date) / 1000);
  if (diffInSeconds < 60) {
    return `hace ${diffInSeconds} segundo${diffInSeconds > 1 ? 's' : ''}`;
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `hace ${minutes} minuto${minutes > 1 ? 's' : ''}`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `hace ${hours} hora${hours > 1 ? 's' : ''}`;
  } else if (diffInSeconds < 604800) {
    const days = Math.floor(diffInSeconds / 86400);
    return `hace ${days} día${days > 1 ? 's' : ''}`;
  } else {
    return date.toLocaleString('es-ES', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
    });
  }
};

const formatFullDate = (timestamp) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Roboto:wght@400;500&display=swap');
/* --- Estilos Generales y Colores --- */
.valka-history-container {
  font-family: 'Roboto', sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #0d0d0d;
  color: #fff;
  box-sizing: border-box;
  overflow-x: hidden;
}

/* --- Encabezado --- */
.valka-header {
  top: 0;
  left: 0;
  width: 100%;
  text-align: center;
  padding: 3rem 1rem 1rem;
  background: linear-gradient(180deg, #0d0d0d 0%, #1a233b 100%);
  border-bottom: 2px solid #57a8f5;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.header-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2rem, 6vw, 3rem);
  font-weight: 700;
  color: #fff;
  text-shadow: 0 0 10px #fff, 0 0 20px #ff00ff, 0 0 30px #ff00ff;
  margin: 0;
  animation: neon-glow 1.5s ease-in-out infinite alternate;
}

@keyframes neon-glow {
  from {
    text-shadow: 0 0 5px #fff, 0 0 10px #ff00ff, 0 0 15px #ff00ff;
  }
  to {
    text-shadow: 0 0 10px #fff, 0 0 20px #ff00ff, 0 0 30px #ff00ff;
  }
}

.header-subtitle {
  font-size: clamp(0.9rem, 2.5vw, 1.1rem);
  color: #c0c0c0;
  margin-top: 0.25rem;
  letter-spacing: 1px;
}

.search-container {
  width: 90%;
  max-width: 400px;
  margin: 1rem auto 0;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ff00ff;
  border-radius: 20px;
  background-color: #1a1a1a;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 0 10px rgba(255, 0, 255, 0.2);
}

.search-input:focus {
  outline: none;
  border-color: #57a8f5;
  box-shadow: 0 0 15px rgba(87, 168, 245, 0.5);
}

.back-button {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background-color: #ff00ff;
  color: #000;
  border: none;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(255, 0, 255, 0.4);
}

.back-button:hover {
  background-color: #fff;
  color: #ff00ff;
  box-shadow: 0 4px 15px rgba(255, 0, 255, 0.7);
  transform: scale(1.05);
}


/* --- Contenido Principal --- */
.history-main {
  flex-grow: 1;
  padding: 2rem 1rem 6rem;
}

.loading-message, .error-message, .empty-history, .empty-history-full {
  text-align: center;
  padding: 4rem 1rem;
  font-size: clamp(1.2rem, 4vw, 1.5rem);
  color: #c0c0c0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 1.5rem;
  background-color: #1a1a1a;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-left: 5px solid transparent;
}

.history-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
}

.history-content {
  flex-grow: 1;
}

.history-message {
  font-size: clamp(0.9rem, 3vw, 1.1rem);
  margin: 0;
  font-weight: 500;
  line-height: 1.5;
}

.history-timestamp {
  display: block;
  font-size: clamp(0.8rem, 2.5vw, 0.9rem);
  color: #999;
  margin-top: 0.5rem;
}

/* --- Colores de Mensaje Actualizados --- */
.message-elimino {
  border-left-color: #ef4444; /* Rojo */
  color: #ef4444;
}

.message-agrego {
  border-left-color: #a3e635; /* Verde */
  color: #a3e635;
}

.message-aumento {
  border-left-color: #ff00ff; /* Rosado */
  color: #ff00ff;
}

.message-disminuyo {
  border-left-color: #57a8f5; /* Azul */
  color: #57a8f5;
}

/* --- Controles de Paginación --- */
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 2rem;
  padding: 1rem;
}

.pagination-button {
  background-color: #57a8f5;
  color: #000;
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 10px rgba(87, 168, 245, 0.4);
}

.pagination-button:hover:not(:disabled) {
  background-color: #fff;
  color: #57a8f5;
  box-shadow: 0 4px 15px rgba(87, 168, 245, 0.7);
  transform: scale(1.05);
}

.pagination-button:disabled {
  background-color: #333;
  color: #666;
  cursor: not-allowed;
  opacity: 0.6;
}

.pagination-page-info {
  font-size: 1.1rem;
  color: #c0c0c0;
  font-weight: 500;
}

/* --- Pie de Página --- */
.valka-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  text-align: center;
  padding: 1.5rem 1rem;
  background-color: #111;
  border-top: 1px solid #333;
  color: #888;
  font-size: 0.9rem;
  z-index: 10;
}

/* --- Responsive mejorado --- */
@media (max-width: 768px) {
  .valka-header {
    padding: 1rem 0.5rem 0.5rem;
  }
  .header-title {
    font-size: clamp(1.8rem, 8vw, 2.5rem);
  }
  .search-container {
    margin: 0.5rem auto 0;
  }
  .back-button{
    position: static;
    margin: 0.5rem;
  }
  .history-main {
    padding: 2rem 0.5rem 6rem;
  }
  .pagination-controls {
    gap: 1rem;
  }
  .pagination-button {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
}
</style>