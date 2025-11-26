<template>
  <header class="elegant-header-wrapper">
    <button class="back-button" @click="goBack">Volver</button>

    <div class="tabs-container">
      <button 
        :class="['tab-button', { 'active': activeTab === 'owner' }]"
        @click="setActiveTab('owner')"
      >
        Mis Movimientos
      </button>
      
      <button 
        :class="['tab-button', { 'active': activeTab === 'admin' }]"
        @click="setActiveTab('admin')"
      >
        Movimientos Admin
      </button>
    </div>
  </header>

  <div class="main-content">
    <div class="content-container">
      <div v-if="activeTab === 'owner'" class="movimientos-dueño">
        <movimientos />
      </div>
      
      <div v-if="activeTab === 'admin'" class="movimientos-admin">
        <MovimientosdeInventario />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import movimientos from './movimientos.vue'; 
import MovimientosdeInventario from './MovimientosdeInventario.vue'; 

const router = useRouter();

// ----------------------------------------------------
// Lógica de Pestañas y localStorage
// ----------------------------------------------------

const activeTab = ref('owner'); 
const LOCAL_STORAGE_KEY = 'lastActiveMovimientoTab';

const setActiveTab = (tab) => {
  activeTab.value = tab;
  localStorage.setItem(LOCAL_STORAGE_KEY, tab);
};

onMounted(() => {
  const storedTab = localStorage.getItem(LOCAL_STORAGE_KEY);
  
  if (storedTab && (storedTab === 'owner' || storedTab === 'admin')) {
    activeTab.value = storedTab;
  } else {
    activeTab.value = 'owner';
    localStorage.setItem(LOCAL_STORAGE_KEY, 'owner'); 
  }
});


// ----------------------------------------------------
// Lógica de Navegación
// ----------------------------------------------------

const goBack = () => {
  router.back();
};

</script>

<style scoped>
/* 🎨 Definición de variables y paleta de colores oscura */
.elegant-header-wrapper, .main-content, .content-container {
  --color-dark-bg: #121212; /* Fondo Negro Oscuro */
  --color-light-text: #e0e0e0; /* Texto Gris Claro */
  --color-highlight-pink: #ff4081; /* Resaltado Rosa Fuerte */
  --color-highlight-blue: #448aff; /* Resaltado Azul Vívido */
  --color-gray-border: #333; /* Bordes Grises Oscuros */
  --color-divider: #282828; /* Gris más claro para la línea divisoria */
  
  /* Se reducen las alturas para hacer el header más compacto */
  --header-height-desktop: 10px; /* Reducido de 150px */
  --header-height-mobile: 10px; /* Reducido de 190px */
}

/* * ----------------------------------------
 * 🖤 CABECERA COMPLETA (ELEGANT HEADER WRAPPER)
 * ----------------------------------------
 */
.elegant-header-wrapper {
  position: sticky;
  top: 0;
  z-index: 1000;
  background-color: var(--color-dark-bg);
  padding: 0.5rem 0; /* Menos padding vertical */
  
  /* Línea divisoria en la parte inferior */
  border-bottom: 2px solid var(--color-divider); 
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5); 
}

/* --- Botón Volver (Ajuste de posición) --- */
.back-button {
  position: absolute; 
  top: 0.8rem; /* Reducido */
  left: 1.5rem;
  background-color: transparent; 
  color: var(--color-highlight-pink);
  border: 2px solid var(--color-highlight-pink);
  border-radius: 20px; 
  padding: 0.3rem 0.8rem; /* Más compacto */
  font-size: 1.3rem; /* Más pequeño */
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 1010; 
}

.back-button:hover {
  background-color: var(--color-highlight-pink);
  color: var(--color-dark-bg);
  box-shadow: 0 0 8px var(--color-highlight-pink);
  transform: scale(1.05);
}

/* --- Contenedor de Pestañas (Ajuste de margen) --- */
.tabs-container {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 3rem; /* Reducido de 4rem */
  padding: 0 1rem 0.5rem 1rem; /* Padding inferior añadido para separación */
}

.tab-button {
  flex-grow: 1; 
  max-width: 300px; 
  padding: 0.6rem 1rem; /* Más compacto */
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid var(--color-gray-border);
  border-radius: 8px;
  background-color: var(--color-dark-bg);
  color: var(--color-light-text);
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
}

/* Estilo cuando el botón está activo (Dueño: Rosa) */
.tab-button.active:nth-child(1) { 
  background-color: var(--color-highlight-pink);
  color: var(--color-dark-bg);
  border-color: var(--color-highlight-pink);
  box-shadow: 0 0 15px rgba(255, 64, 129, 0.7);
  transform: translateY(-2px);
}

/* Estilo cuando el botón está activo (Admin: Azul) */
.tab-button.active:nth-child(2) { 
  background-color: var(--color-highlight-blue);
  color: var(--color-dark-bg);
  border-color: var(--color-highlight-blue);
  box-shadow: 0 0 15px rgba(68, 138, 255, 0.7);
  transform: translateY(-2px);
}

/* Efecto hover general */
.tab-button:not(.active):hover {
  background-color: var(--color-gray-border);
  color: var(--color-white);
  border-color: var(--color-highlight-pink); 
}

/* * ----------------------------------------
 * 🧱 CONTENIDO PRINCIPAL (EL AJUSTE CLAVE)
 * ----------------------------------------
 */
.main-content {
  /* ESTO SE REDUJO SIGNIFICATIVAMENTE: 
     Ahora solo empuja el contenido la cantidad necesaria */
  margin-top: var(--header-height-desktop); 
  padding: 1rem;
}

.content-container {
  background-color: var(--color-white); 
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  margin: 0 auto;
  max-width: 1200px;
  padding: 1rem;
}

/* * ----------------------------------------
 * 📱 RESPONSIVE
 * ----------------------------------------
 */
@media (max-width: 768px) {
  /* Ajuste de Margen para Mobile */
  .main-content {
    margin-top: var(--header-height-mobile); 
  }

  .elegant-header-wrapper {
    padding: 0.5rem 0;
  }
  
  /* Botón Volver */
  .back-button {
    position: static; 
    display: block;
    width: fit-content;
    margin: 0.5rem 1rem 0 1rem;
    padding: 0.4rem 1rem;
    font-size: 1rem;
  }

  /* Pestañas en Columna */
  .tabs-container {
    flex-direction: column; 
    gap: 0.5rem;
    margin-top: 0.5rem; 
  }
  
  .tab-button {
    width: 100%;
    max-width: none;
    font-size: 0.95rem;
    padding: 0.6rem 1rem;
  }
}
</style>