<template>
  <div class="login-container">
    <div class="background-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
      <div class="floating-particles">
        <div
          v-for="n in 20"
          :key="n"
          class="particle"
          :style="{
            '--delay': Math.random() * 3 + 's',
            '--x': Math.random() * 100 + '%',
            '--y': Math.random() * 100 + '%',
          }"
        ></div>
      </div>
    </div>

    <!-- HEADER MEJORADO CON BOTONES DE NAVEGACIÓN -->
    <header class="header">
      <div class="header-content">
        <div class="logo-section">
          <div class="logo-placeholder">
            <div class="logo-icon"></div>
          </div>
          <h1 class="brand-name">Control AS</h1>
        </div>
        
        <!-- BOTONES DE NAVEGACIÓN -->
        <nav class="header-nav">
          <button 
            @click="setActiveView('login')"
            :class="['nav-button', { active: activeView === 'login' }]"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
            <span>Iniciar Sesión</span>
          </button>
          
          <button 
            @click="setActiveView('about')"
            :class="['nav-button', { active: activeView === 'about' }]"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
            <span>Sobre Nosotros</span>
          </button>
        </nav>
      </div>
    </header>

    <!-- CONTENIDO PRINCIPAL CON RENDERIZADO CONDICIONAL -->
    <main class="main-content">
      
      <!-- VISTA DE LOGIN -->
      <div v-if="activeView === 'login'" class="login-view">
        <div class="login-card" :class="{ shake: isShaking }">
          <div class="card-glow"></div>
          <div class="login-header">
            <h2 class="login-title">Bienvenido de vuelta</h2>
            <p class="login-subtitle">Accede a tu cuenta Control AS</p>
          </div>

          <form @submit.prevent="handleLogin" class="login-form">
            <div class="user-type-selector">
              <div class="selector-label">Iniciar sesión como:</div>
              <div class="type-buttons">
                <button
                  type="button"
                  class="type-button"
                  :class="{ active: userType === 'dueno' }"
                  @click="userType = 'dueno'"
                >
                  <div class="button-icon">👔</div>
                  <span>Dueño</span>
                </button>
                <button
                  type="button"
                  class="type-button"
                  :class="{ active: userType === 'administrador' }"
                  @click="userType = 'administrador'"
                >
                  <div class="button-icon">👨‍💼</div>
                  <span>Administrador</span>
                </button>
              </div>
            </div>
            
            <div
              class="input-group"
              :class="{ focused: usernameFocused, filled: username }"
            >
              <label for="username" class="input-label">Usuario</label>
              <input
                id="username"
                v-model="username"
                type="text"
                class="form-input"
                @focus="usernameFocused = true"
                @blur="usernameFocused = false"
                required
              />
              <div class="input-border"></div>
              <div class="input-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                  />
                </svg>
              </div>
            </div>

            <div
              class="input-group"
              :class="{ focused: passwordFocused, filled: password }"
            >
              <label for="password" class="input-label">Contraseña</label>
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                @focus="passwordFocused = true"
                @blur="passwordFocused = false"
                required
              />
              <div class="input-border"></div>
              <div class="input-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12,17A2,2 0 0,0 14,15C14,13.89 13.1,13 12,13A2,2 0 0,0 10,15A2,2 0 0,0 12,17M18,8A2,2 0 0,1 20,10V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V10C4,8.89 4.9,8 6,8H7V6A5,5 0 0,1 12,1A5,5 0 0,1 17,6V8H18M12,3A3,3 0 0,0 9,6V8H15V6A3,3 0 0,0 12,3Z"
                  />
                </svg>
              </div>
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
              >
                <svg v-if="showPassword" viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z"
                  />
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M11.83,9L15,12.16C15,12.11 15,12.05 15,12A3,3 0 0,0 12,9C11.94,9 11.89,9 11.83,9M7.53,9.8L9.08,11.35C9.03,11.56 9,11.77 9,12A3,3 0 0,0 12,15C12.22,15 12.44,14.97 12.65,14.92L14.2,16.47C13.53,16.8 12.79,17 12,17A5,5 0 0,1 7,12C7,11.21 7.2,10.47 7.53,9.8M2,4.27L4.28,6.55L4.73,7C3.08,8.3 1.78,10 1,12C2.73,16.39 7,19.5 12,19.5C13.55,19.5 15.03,19.2 16.38,18.66L16.81,19.09L19.73,22L21,20.73L3.27,3M12,7A5,5 0 0,1 17,12C17,12.64 16.87,13.26 16.64,13.82L19.57,16.75C21.07,15.5 22.27,13.86 23,12C21.27,7.61 17,4.5 12,4.5C10.6,4.5 9.26,4.75 8,5.2L10.17,7.35C10.76,7.13 11.38,7 12,7Z"
                  />
                </svg>
              </button>
            </div>
            
            <div
              v-if="userType === 'administrador'"
              class="input-group"
              :class="{ focused: barIdFocused, filled: barId }"
            >
              <label for="bar-id" class="input-label">ID del Local</label>
              <input
                id="bar-id"
                v-model="barId"
                type="number"
                class="form-input"
                @focus="barIdFocused = true"
                @blur="barIdFocused = false"
                required
              />
              <div class="input-border"></div>
              <div class="input-icon">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path
                    d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"
                  />
                </svg>
              </div>
            </div>
            
            <button
              type="submit"
              class="login-button"
              :class="{ loading: isLoading }"
              :disabled="isLoading"
            >
              <span v-if="!isLoading" class="button-text">Iniciar Sesión</span>
              <div v-else class="button-loader">
                <div class="loader-dot"></div>
                <div class="loader-dot"></div>
                <div class="loader-dot"></div>
              </div>
            </button>
            
            <!-- ✅ SOLO SE MUESTRA SI userType ES 'dueno' -->
            <router-link 
              v-if="userType === 'dueno'" 
              to="/recuperar" 
              class="forgot-password-link"
            >
              ¿Olvidaste tu contraseña? 💫
            </router-link>
          </form>
        </div>
      </div>

      <!-- VISTA DE SOBRE NOSOTROS / CONTACTO -->
      <div v-if="activeView === 'about'" class="about-view">
        <sobre_nosotros />
      </div>

    </main>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h3>Control AS BAR</h3>
          <p>La mejor experiencia </p>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2024 Control AS Bar. Todos los derechos reservados.</p>
      </div>
    </footer>

    <!-- Modal de cuenta bloqueada -->
    <teleport to="body">
      <transition name="modal-fade">
        <div
          v-if="showPaymentBlockedModal"
          class="payment-blocked-overlay"
          @click.self="showPaymentBlockedModal = false"
        >
          <div class="payment-blocked-modal" @click.stop>
            <button class="modal-close-btn" @click="showPaymentBlockedModal = false">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>

            <div class="blocked-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M12,17A2,2 0 0,0 14,15C14,13.89 13.1,13 12,13A2,2 0 0,0 10,15A2,2 0 0,0 12,17M18,8A2,2 0 0,1 20,10V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V10C4,8.89 4.9,8 6,8H7V6A5,5 0 0,1 12,1A5,5 0 0,1 17,6V8H18M12,3A3,3 0 0,0 9,6V8H15V6A3,3 0 0,0 12,3Z"/>
              </svg>
              <div class="lock-slash">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round">
                  <path d="M3 3L21 21"/>
                </svg>
              </div>
            </div>

            <h2 class="modal-title">Cuenta Bloqueada</h2>
            <p class="modal-subtitle">
              Tu cuenta ha sido bloqueada por <span class="highlight">falta de pago</span>.
            </p>

            <div class="contact-card">
              <p>Para reactivarla, comunícate con nosotros:</p>
              <div class="contact-item whatsapp">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 5.44h-.005c-1.58-.315-3.017-1.042-4.137-2.183-2.218-2.26-2.218-5.297 0-7.557a4.84 4.84 0 0 1 3.61-1.615h.002c.913 0 1.783.363 2.428 1.01.645.647 1.008 1.518 1.008 2.432 0 2.36-1.922 4.282-4.29 4.282zM12.004 0C5.377 0 .003 5.374.003 12c0 2.098.543 4.09 1.504 5.82L.003 24l6.305-1.492c1.696.93 3.6 1.42 5.52 1.42 6.627 0 12-5.373 12-12 0-3.224-1.262-6.247-3.558-8.52C18.246 1.262 15.223.004 12.004.004z"/></svg>
                <span>WhatsApp: <strong>+57 3213686373</strong></span>
              </div>
            </div>

            <p class="modal-footer-text">Gracias por tu comprensión</p>

            <button class="modal-understand-btn" @click="showPaymentBlockedModal = false">
              Entendido
            </button>
          </div>
        </div>
      </transition>
    </teleport>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Swal from 'sweetalert2';
import { useUserStore } from '@/stores/user';
import { useAdminStore } from '@/stores/admin';
import { API_BASE_URL } from '../config/api';
import sobre_nosotros from './sobre_nosotros.vue';

export default {
  name: 'Control AS',
  components: {
    sobre_nosotros
  },
  setup() {
    const activeView = ref('login');
    const userType = ref('dueno');
    const barId = ref('');
    const barIdFocused = ref(false);
    const username = ref('');
    const password = ref('');
    const usernameFocused = ref(false);
    const passwordFocused = ref(false);
    const showPassword = ref(false);
    const isLoading = ref(false);
    const isShaking = ref(false);
    const router = useRouter();
    const userStore = useUserStore();
    const adminStore = useAdminStore();
    const showPaymentBlockedModal = ref(false);

    const setActiveView = (view) => {
      activeView.value = view;
    };

    const handleLogin = async () => {
      if (!username.value || !password.value) {
        isShaking.value = true;
        setTimeout(() => (isShaking.value = false), 500);
        Swal.fire({
          icon: 'warning',
          title: 'Campos Vacíos',
          text: 'Por favor, ingresa todos los campos requeridos.',
          customClass: { popup: 'swal2-dark-popup', confirmButton: 'swal2-confirm-button' },
        });
        return;
      }

      if (userType.value === 'administrador' && !barId.value) {
        isShaking.value = true;
        setTimeout(() => (isShaking.value = false), 500);
        Swal.fire({
          icon: 'warning',
          title: 'ID del Local Requerido',
          text: 'Por favor, ingresa el ID del local.',
          customClass: { popup: 'swal2-dark-popup', confirmButton: 'swal2-confirm-button' },
        });
        return;
      }

      isLoading.value = true;
      isShaking.value = false;

      try {
        const requestBody = {
          nombre: username.value,
          contraseña: password.value,
        };

        if (userType.value === 'administrador') {
          requestBody.bar_id = parseInt(barId.value);
        }

        const response = await fetch(`${API_BASE_URL}/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(requestBody),
        });

        if (response.ok) {
          const data = await response.json();

          if (data.tipo === 'dueno') {
            userStore.setDueno(data);
            await Swal.fire({
              icon: 'success',
              title: 'Bienvenido de vuelta',
              text: `¡Hola, ${data.nombre}! Acceso como Dueño`,
              timer: 2000,
              showConfirmButton: false,
              customClass: { popup: 'swal2-dark-popup' },
            });
            router.push('/locales');
          } else if (data.tipo === 'administrador') {
            adminStore.setAdmin(data);
            await Swal.fire({
              icon: 'success',
              title: 'Acceso concedido',
              text: `¡Bienvenido, ${data.nombre}!`,
              timer: 2000,
              showConfirmButton: false,
              customClass: { popup: 'swal2-dark-popup' },
            });
            router.push('/administrador_parte');
          }
        } else {
          const errorData = await response.json();

          if (response.status === 403) {
            showPaymentBlockedModal.value = true;
            isShaking.value = true;
            setTimeout(() => (isShaking.value = false), 600);
            return;
          } else {
            const title = response.status === 401 ? "Credenciales Incorrectas" : "Error de Acceso";
            await Swal.fire({
              icon: 'error',
              title,
              text: errorData.detail || "Ocurrió un error inesperado.",
              customClass: { popup: 'swal2-dark-popup', confirmButton: 'swal2-confirm-button' },
            });
          }

          isShaking.value = true;
          setTimeout(() => (isShaking.value = false), 600);
        }
      } catch (error) {
        console.error('Error durante el login:', error);
        await Swal.fire({
          icon: 'error',
          title: 'Error de Conexión',
          text: 'No se pudo conectar con el servidor. Verifica tu conexión e inténtalo de nuevo.',
          customClass: { popup: 'swal2-dark-popup', confirmButton: 'swal2-confirm-button' },
        });
      } finally {
        isLoading.value = false;
      }
    };

    return {
      username,
      password,
      usernameFocused,
      passwordFocused,
      showPassword,
      isLoading,
      isShaking,
      handleLogin,
      userType,
      barId,
      barIdFocused,
      showPaymentBlockedModal,
      activeView,
      setActiveView,
    };
  },
};
</script>

<style>
/* ... (Estilos SweetAlert2) ... */
.swal2-popup {
  background: linear-gradient(145deg, #1a1a2e, #161625) !important;
  color: #e0e0e0 !important;
  border: 1px solid rgba(132, 70, 240, 0.4) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6) !important;
  backdrop-filter: blur(8px) !important;
  -webkit-backdrop-filter: blur(8px) !important;
  animation: fadeInPop 0.3s ease-out forwards;
}

@keyframes fadeInPop {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.swal2-title {
  color: #f0f0f0 !important;
  font-family: 'Montserrat', sans-serif !important;
  font-weight: 700 !important;
  padding-bottom: 10px !important;
  border-bottom: 1px solid rgba(132, 70, 240, 0.2) !important;
  margin-bottom: 20px !important;
}

.swal2-html-container {
  color: #c0c0c0 !important;
  font-family: 'Open Sans', sans-serif !important;
  font-size: 1.1em !important;
  line-height: 1.6em !important;
}

.swal2-icon {
  margin-bottom: 20px !important;
  border-width: 3px !important;
}

.swal2-icon.swal2-success {
  border-color: #4CAF50 !important;
}
.swal2-icon.swal2-success [class^='swal2-success-line'] {
  background-color: #4CAF50 !important;
}

.swal2-icon.swal2-error {
  border-color: #f44336 !important;
}
.swal2-icon.swal2-error [class^='swal2-x-mark'] {
  color: #f44336 !important;
}

.swal2-icon.swal2-warning {
  border-color: #ffeb3b !important;
}
.swal2-icon.swal2-warning [class^='swal2-icon-content'] {
  color: #ffeb3b !important;
}

.swal2-confirm.swal2-styled {
  background: linear-gradient(90deg, #8446f0, #a06dfa) !important;
  color: white !important;
  border: none !important;
  font-weight: bold !important;
  padding: 12px 30px !important;
  border-radius: 25px !important;
  font-size: 1.1em !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 15px rgba(132, 70, 240, 0.4) !important;
}

.swal2-confirm.swal2-styled:focus {
  box-shadow: 0 0 0 3px rgba(132, 70, 240, 0.6) !important;
  outline: none !important;
}

.swal2-confirm.swal2-styled:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(132, 70, 240, 0.6) !important;
  background: linear-gradient(90deg, #6a34cc, #8446f0) !important;
}

.swal2-actions {
  margin-top: 30px !important;
}

.swal2-cancel.swal2-styled {
  background-color: #555 !important;
  color: white !important;
  border-radius: 25px !important;
  transition: background-color 0.3s ease !important;
}
.swal2-cancel.swal2-styled:hover {
  background-color: #777 !important;
}

.swal2-backdrop-show {
  background: rgba(0, 0, 0, 0.7) !important;
}

.swal2-loading {
  color: #8446f0 !important;
}
</style>
<style scoped>
/* Estilos generales para el contenedor del grupo de entrada */
.input-group {
  position: relative;
  margin-bottom: 25px;
}
/* Se mejoró el estilo del enlace para que sea más visual y funcional */
.forgot-password-link {
  display: block;
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.95rem;
  font-weight: 500;
  color: #a0a0a0;
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
  /* Se añadió un efecto de brillo */
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  /* Se ajustó la posición para que no se superponga */
  z-index: 10;
}

.forgot-password-link:hover {
  transform: scale(1.05);
  filter: drop-shadow(0 0 8px rgba(255, 105, 180, 0.5));
  text-decoration: none;
}

.forgot-password-link:active {
  transform: scale(0.95);
}

.remove-image-button:hover {
  background-color: rgba(233, 30, 99, 0.8);
}

.remove-image-button svg {
  width: 18px;
  height: 18px;
  color: #fff;
}
/* ... (Estilos del login-container, backgrounds, header, etc. sin cambios) ... */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #16213e 100%);
  position: relative;
  overflow-x: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Background animations */
.background-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
}

.shape {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(45deg, rgba(255, 105, 180, 0.1), rgba(30, 144, 255, 0.1));
  animation: float 20s infinite linear;
}

.shape-1 {
  width: 300px;
  height: 300px;
  top: 10%;
  right: -150px;
  animation-delay: 0s;
}

.shape-2 {
  width: 200px;
  height: 200px;
  bottom: 20%;
  left: -100px;
  animation-delay: -7s;
}

.shape-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  left: 80%;
  animation-delay: -14s;
}

@keyframes float {
  0% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-30px) rotate(120deg); }
  66% { transform: translateY(30px) rotate(240deg); }
  100% { transform: translateY(0px) rotate(360deg); }
}

.floating-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  left: var(--x);
  top: var(--y);
  animation: particleFloat 6s infinite ease-in-out;
  animation-delay: var(--delay);
}

@keyframes particleFloat {
  0%, 100% { transform: translateY(0px) translateX(0px) scale(1); opacity: 0; }
  50% { transform: translateY(-100px) translateX(50px) scale(1.5); opacity: 1; }
}

/* Header */
.header {
  position: relative;
  z-index: 10;
  padding: 2rem 2rem 1rem;
  background: rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
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
  width: 50px;
  height: 50px;
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: logoGlow 2s infinite alternate;
}
.login-title {
    font-size: 2rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.5rem;
    background: linear-gradient(45deg, #ffffff, #ff69b4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.logo-icon {
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 50%;
}

@keyframes logoGlow {
  0% { box-shadow: 0 0 20px rgba(255, 105, 180, 0.5); }
  100% { box-shadow: 0 0 30px rgba(30, 144, 255, 0.8); }
}

.brand-name {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}

.header-tagline {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  font-style: italic;
}

/* Main Content */
.main-content {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 2rem;
}

.login-card {
  position: relative;
  width: 100%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 3rem 2rem;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.5),
    0 0 60px rgba(255, 105, 180, 0.1);
  transition: all 0.3s ease;
  animation: slideUp 0.8s ease-out;
  z-index: 20; /* Se corrigió el z-index para que esté por encima del fondo */
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 35px 60px -12px rgba(0, 0, 0, 0.6),
    0 0 80px rgba(255, 105, 180, 0.2);
}

.login-card.shake {
  animation: shake 0.5s ease-in-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 24px;
  background: linear-gradient(45deg, rgba(255, 105, 180, 0.1), rgba(30, 144, 255, 0.1));
  opacity: 0;
  transition: opacity 0.3s ease;
}

.login-card:hover .card-glow {
  opacity: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

/* Form styles */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.input-group {
  position: relative;
}

.input-label {
  position: absolute;
  left: 3.5rem;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.6);
  font-size: 1rem;
  pointer-events: none;
  transition: all 0.3s ease;
  background: transparent;
  z-index: 2;
}

.input-group.focused .input-label,
.input-group.filled .input-label {
  top: -0.5rem;
  left: 1rem;
  font-size: 0.8rem;
  color: #ff69b4;
  background: rgba(0, 0, 0, 0.8);
  padding: 0 0.5rem;
  border-radius: 4px;
}

.form-input {
  width: 100%;
  padding: 1rem 3.5rem 1rem 3.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
}

.form-input:focus {
  border-color: #ff69b4;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 20px rgba(255, 105, 180, 0.3);
}

.input-border {
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  transition: all 0.3s ease;
  transform: translateX(-50%);
  border-radius: 1px;
}

.input-group.focused .input-border {
  width: 100%;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: rgba(255, 255, 255, 0.6);
  transition: color 0.3s ease;
}

.input-group.focused .input-icon {
  color: #ff69b4;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  cursor: pointer;
  width: 20px;
  height: 20px;
  transition: color 0.3s ease;
}

.password-toggle:hover {
  color: #ff69b4;
}

/* Button */
.login-button {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  border: none;
  border-radius: 16px;
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  margin-top: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.login-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 15px 30px rgba(255, 105, 180, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.login-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.login-button:hover::before {
  left: 100%;
}

.button-loader {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.loader-dot {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  animation: loaderBounce 1.4s infinite ease-in-out both;
}

.loader-dot:nth-child(1) { animation-delay: -0.32s; }
.loader-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes loaderBounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.login-footer {
  text-align: center;
  margin-top: 2rem;
}

.forgot-password {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: #ff69b4;
}

/* Footer */
.footer {
  position: relative;
  z-index: 10;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: center;
}

.footer-section h3 {
  color: white;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-section p {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
}

.social-links {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.social-link {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  text-decoration: none;
}

.social-link:hover {
  background: rgba(255, 105, 180, 0.2);
  color: #ff69b4;
  transform: translateY(-3px);
}

.social-link svg {
  width: 18px;
  height: 18px;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 1rem;
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
}

.footer-links {
  display: flex;
  gap: 1.5rem;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #ff69b4;
}

/* Modal Transition */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.5s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}

@keyframes modalSlideDown {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .brand-name {
    font-size: 1.5rem;
  }
  
  .login-card {
    margin: 1rem;
    padding: 2rem 1.5rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 1rem;
  }
  
  .social-links {
    justify-content: center;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .shape-1, .shape-2, .shape-3 {
    opacity: 0.3;
  }


}

@media (max-width: 480px) {
  .main-content {
    padding: 1rem;
  }
  
  .login-card {
    padding: 1.5rem 1rem;
  }
  
  .form-input {
    padding: 0.8rem 3rem 0.8rem 3rem;
  }
  
  .login-button, .create-dueno-button {
    padding: 0.8rem;
    font-size: 1rem;
  }
  
  .header {
    padding: 1rem;
  }
  
  .footer {
    padding: 1.5rem 1rem;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .login-card, .modal-content {
    background: rgba(0, 0, 0, 0.9);
    border: 2px solid #ffffff;
  }
  
  .form-input {
    background: rgba(0, 0, 0, 0.8);
    border-color: #ffffff;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  .floating-particles {
    display: none;
  }
}

/* Dark mode enhancement */
@media (prefers-color-scheme: dark) {
  .login-container {
    background: linear-gradient(135deg, #000000 0%, #0d0d1a 50%, #1a0a2e 100%);
  }
}
/* Agregar al final del <style scoped> */

/* Selector de tipo de usuario */
.user-type-selector {
  margin-bottom: 2rem;
  text-align: center;
}

.selector-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
  margin-bottom: 1rem;
  font-weight: 500;
}

.type-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.type-button {
  flex: 1;
  max-width: 150px;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.6);
  position: relative;
  overflow: hidden;
}

.type-button::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.type-button:hover {
  border-color: rgba(255, 105, 180, 0.5);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(255, 105, 180, 0.2);
}

.type-button.active {
  border-color: #ff69b4;
  background: rgba(255, 105, 180, 0.1);
  color: white;
  box-shadow: 0 0 30px rgba(255, 105, 180, 0.4);
}

.type-button.active::before {
  opacity: 0.1;
}

.button-icon {
  font-size: 2rem;
  filter: grayscale(100%);
  transition: filter 0.3s ease;
  position: relative;
  z-index: 1;
}

.type-button.active .button-icon,
.type-button:hover .button-icon {
  filter: grayscale(0%);
}

.type-button span {
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: relative;
  z-index: 1;
}

/* Animación de entrada para el campo bar_id */
.input-group {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Reemplaza estos estilos en tu <style scoped> */

/* Selector de tipo de usuario */
.user-type-selector {
  margin-bottom: 1.5rem;
  text-align: center;
}

.selector-label {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  margin-bottom: 0.8rem;
  font-weight: 500;
}

.type-buttons {
  display: flex;
  gap: 0.8rem;
  justify-content: center;
}

.type-button {
  flex: 1;
  max-width: 100px; /* 🔧 Reducido de 150px a 100px */
  padding: 0.8rem; /* 🔧 Reducido de 1rem a 0.8rem */
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.3rem; /* 🔧 Reducido de 0.5rem a 0.3rem */
  cursor: pointer;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.6);
  position: relative;
  overflow: hidden;
}

.type-button::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.type-button:hover {
  border-color: rgba(255, 105, 180, 0.5);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(255, 105, 180, 0.2);
}

.type-button.active {
  border-color: #ff69b4;
  background: rgba(255, 105, 180, 0.1);
  color: white;
  box-shadow: 0 0 30px rgba(255, 105, 180, 0.4);
}

.type-button.active::before {
  opacity: 0.1;
}

.button-icon {
  font-size: 1.5rem; /* 🔧 Reducido de 2rem a 1.5rem */
  filter: grayscale(100%);
  transition: filter 0.3s ease;
  position: relative;
  z-index: 1;
}

.type-button.active .button-icon,
.type-button:hover .button-icon {
  filter: grayscale(0%);
}

.type-button span {
  font-size: 0.75rem; /* 🔧 Reducido de 0.9rem a 0.75rem */
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: relative;
  z-index: 1;
}

/* Animación de entrada para el campo bar_id */
.input-group {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive para los botones circulares */
@media (max-width: 480px) {
  .type-buttons {
    gap: 0.5rem;
  }
  
  .type-button {
    max-width: 85px; /* 🔧 Reducido de 120px a 85px */
    padding: 0.6rem; /* 🔧 Reducido de 0.8rem a 0.6rem */
  }
  
  .button-icon {
    font-size: 1.2rem; /* 🔧 Reducido de 1.5rem a 1.2rem */
  }
  
  .type-button span {
    font-size: 0.7rem; /* 🔧 Reducido de 0.8rem a 0.7rem */
  }
}
/* Modal personalizado de pago bloqueado */
.payment-blocked-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1rem;
}

.payment-blocked-modal {
  position: relative;
  max-width: 420px;
  width: 100%;
  background: linear-gradient(145deg, #1a1a2e, #161625);
  border: 1px solid rgba(255, 105, 180, 0.4);
  border-radius: 24px;
  padding: 2.5rem 2rem;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7), 0 0 60px rgba(255, 105, 180, 0.2);
  animation: modalSlideDown 0.5s ease-out;
}

.modal-close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  color: #ff6b6b;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-close-btn:hover {
  background: rgba(255, 107, 107, 0.2);
  transform: rotate(90deg);
}

.blocked-icon {
  position: relative;
  display: inline-block;
  width: 100px;
  height: 100px;
  margin: 0 auto 1.5rem;
  color: #ff6b6b;
}

.blocked-icon svg:first-child {
  width: 100px;
  height: 100px;
  filter: drop-shadow(0 0 20px rgba(255, 107, 107, 0.5));
}

.lock-slash {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 120px;
}

.lock-slash svg {
  width: 120px;
  height: 120px;
  color: #ff6b6b;
}

.modal-title {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.modal-subtitle {
  font-size: 1.1rem;
  color: #ddd;
  margin-bottom: 1.5rem;
}

.modal-subtitle .highlight {
  color: #ff6b6b;
  font-weight: 600;
}

.contact-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 1.5rem;
  margin: 1.5rem 0;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.contact-card p {
  color: #ccc;
  margin-bottom: 1rem;
}

.contact-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  margin: 0.8rem 0;
  font-size: 1rem;
  color: #4dabf7;
}

.contact-item.whatsapp {
  color: #51cf66;
}

.contact-item svg {
  width: 20px;
  height: 20px;
}

.modal-footer-text {
  color: #888;
  font-size: 0.9rem;
  margin: 1.5rem 0 2rem;
}

.modal-understand-btn {
  background: linear-gradient(45deg, #ff6b6b, #ff8e8e);
  color: white;
  border: none;
  padding: 0.9rem 2.5rem;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
}

.modal-understand-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(255, 107, 107, 0.6);
}

/* Animación de entrada */
.modal-fade-enter-active, .modal-fade-leave-active {
  transition: opacity 0.4s ease;
}
.modal-fade-enter-from, .modal-fade-leave-to {
  opacity: 0;
}

@keyframes modalSlideDown {
  from {
    transform: translateY(-60px) scale(0.95);
    opacity: 0;
  }
  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}
</style>
<style scoped>
/* ========================================
   🆕 ESTILOS NUEVOS PARA EL HEADER MEJORADO
   ======================================== */

/* Navegación del header */
.header-nav {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 50px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-button svg {
  width: 20px;
  height: 20px;
  transition: transform 0.3s ease;
}

.nav-button::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 50px;
}

.nav-button span {
  position: relative;
  z-index: 1;
}

.nav-button:hover {
  border-color: rgba(255, 105, 180, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 5px 20px rgba(255, 105, 180, 0.3);
}

.nav-button:hover svg {
  transform: scale(1.1);
}

/* 🎯 Botón activo - ESTILO CLAVE */
.nav-button.active {
  background: linear-gradient(45deg, #ff69b4, #1e90ff);
  border-color: transparent;
  color: white;
  box-shadow: 0 8px 25px rgba(255, 105, 180, 0.4);
}

.nav-button.active::before {
  opacity: 1;
}

.nav-button.active svg {
  transform: scale(1.15);
}



@keyframes fadeInView {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive para botones de navegación */
@media (max-width: 768px) {
  .header-nav {
    flex-direction: column;
    gap: 0.6rem;
    width: 100%;
  }
  
  .nav-button {
    width: 100%;
    justify-content: center;
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .nav-button span {
    display: none;
  }
  
  .nav-button {
    padding: 0.6rem;
    min-width: 45px;
    justify-content: center;
  }
  
  .header-nav {
    flex-direction: row;
    justify-content: center;
  }
}

</style>
<style scoped>

/* ========================================
   🔧 FIX PARA CENTRADO EN MOBILE
   ======================================== */

/* Asegurar que el contenedor principal no tenga overflow horizontal */
.login-container {
  overflow-x: hidden;
  width: 100%;
}

/* Centrado perfecto del main-content */
.main-content {
  width: 100%;
  max-width: 100%;
  padding-left: 1rem;
  padding-right: 1rem;
}

/* Contenedores de vistas con ancho completo */
.login-view,
.about-view {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeInView 0.5s ease-out;
}

@keyframes fadeInView {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Ajustes específicos para móviles */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
    justify-content: center;
    align-items: center;
  }
  
  .login-view {
    width: 100%;
    max-width: 100%;
  }
  
  .login-card {
    margin: 0 auto;
    max-width: 100%;
    width: 100%;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 0.5rem;
  }
  
  .login-card {
    padding: 1.5rem 1rem;
    margin: 0;
    width: 100%;
    max-width: 100%;
  }
  
  /* Asegurar que el formulario también esté centrado */
  .login-form {
    width: 100%;
  }
  
  /* Ajustar inputs en móvil */
  .form-input {
    width: 100%;
    font-size: 16px; /* Previene zoom en iOS */
  }
}

/* Fix para pantallas muy pequeñas */
@media (max-width: 360px) {
  .login-card {
    padding: 1rem 0.75rem;
  }
  
  .type-button {
    max-width: 75px;
    padding: 0.5rem;
  }
  
  .button-icon {
    font-size: 1rem;
  }
  
  .type-button span {
    font-size: 0.65rem;
  }
} 
</style>