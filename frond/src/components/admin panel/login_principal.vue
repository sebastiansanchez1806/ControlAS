<template>
  <div class="login-page-standalone">
    <!-- Efectos de fondo animados -->
    <div class="bg-decoration decoration-1"></div>
    <div class="bg-decoration decoration-2"></div>
    <div class="bg-decoration decoration-3"></div>
    <div class="grid-overlay"></div>
    
    <div class="login-card">
      <div class="card-glow"></div>
      
      <div class="card-header">
        <div class="icon-wrapper">
          <svg class="admin-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 1L9 5h6L12 1zm0 22l3-4.5H9l3 4.5zm-5.5-5.5H1v-3h5.5v3zm11 0V15h5.5v3H17.5zm-4.5-6h-6V9h6v3z"/>
          </svg>
        </div>
        <h1 class="title">Control AS</h1>
        <p class="subtitle">Panel de Administrador</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label for="email">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
            Correo Electrónico
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="admin@controlas.com"
            required
            :disabled="isLoading"
          />
        </div>

        <div class="input-group password-group">
          <label for="password">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            Contraseña
          </label>
          <div class="password-input-container">
            <input
              id="password"
              v-model="password"
              :type="passwordFieldType"
              placeholder="••••••••"
              required
              :disabled="isLoading"
            />
            <button
              type="button"
              @click="togglePasswordVisibility"
              class="toggle-password"
              :aria-label="passwordFieldType === 'password' ? 'Mostrar contraseña' : 'Ocultar contraseña'"
            >
              <svg v-if="passwordFieldType === 'password'" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                <line x1="1" y1="1" x2="23" y2="23"></line>
              </svg>
            </button>
          </div>
        </div>

        <div class="forgot-password-container">
          <button type="button" @click="handleForgotPassword" class="forgot-password-link">
            ¿Olvidaste tu contraseña?
          </button>
        </div>

        <button type="submit" class="btn-continuar" :disabled="isLoading">
          <span v-if="!isLoading">Iniciar Sesión</span>
          <span v-else>Iniciando sesión...</span>
          <svg v-if="!isLoading" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
          <svg v-else class="spinner" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
          </svg>
        </button>
      </form>
    </div>

    <!-- Modal de código de verificación -->
    <div v-if="showCodeModal" class="modal-overlay" @click="closeCodeModal">
      <div class="modal-content" @click.stop>
        <button class="modal-close" @click="closeCodeModal">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>

        <div class="modal-header">
          <div class="modal-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
          </div>
          <h2>Ingresa el código de 6 dígitos</h2>
          <p>Código recibido por correo</p>
        </div>

        <div class="modal-body">
          <div class="code-input-group">
            <input
              v-for="(digit, index) in codeDigits"
              :key="index"
              :ref="el => codeInputs[index] = el"
              v-model="codeDigits[index]"
              type="text"
              maxlength="1"
              class="code-input"
              :class="{ 'error': codeError }"
              @input="handleCodeInput(index, $event)"
              @keydown="handleCodeKeydown(index, $event)"
              @paste="handleCodePaste"
            />
          </div>
          
          <p v-if="codeError" class="error-message">{{ codeError }}</p>
        </div>

        <div class="modal-footer">
          <button @click="closeCodeModal" class="btn-modal btn-secondary" :disabled="isVerifying">
            Cancelar
          </button>
          <button @click="verifyCode" class="btn-modal btn-primary" :disabled="isVerifying || !isCodeComplete">
            <span v-if="!isVerifying">Verificar código</span>
            <span v-else>Verificando...</span>
            <svg v-if="isVerifying" class="spinner-small" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { API_BASE_URL } from '@/config/api';
import { ref, computed, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useGestorPrincipalStore } from '@/stores/gestorPrincipal';
import Swal from 'sweetalert2';

const email = ref('');
const password = ref('');
const passwordFieldType = ref('password');
const isLoading = ref(false);
const showBaresModal = ref(false)
const selectedDueno = ref(null)
const baresDelDueno = ref([])
const isLoadingBares = ref(false)
const showCodeModal = ref(false);
const codeDigits = ref(['', '', '', '', '', '']);
const codeInputs = ref([]);
const codeError = ref('');
const isVerifying = ref(false);
const resetToken = ref('');
const userEmailForReset = ref('');

const router = useRouter();
const gestorStore = useGestorPrincipalStore();

const isCodeComplete = computed(() => {
  return codeDigits.value.every(digit => digit !== '');
});

const togglePasswordVisibility = () => {
  passwordFieldType.value = passwordFieldType.value === 'password' ? 'text' : 'password';
};

const openBaresModal = async (dueno) => {
  selectedDueno.value = dueno
  showBaresModal.value = true
  isLoadingBares.value = true

  try {
    const response = await axios.get(`${API_BASE_URL}/bares/dueno/${dueno.id}`)
    baresDelDueno.value = response.data
  } catch (error) {
    console.error('Error cargando bares:', error)
    Swal.fire('Error', 'No se pudieron cargar los locales de este dueño', 'error')
    baresDelDueno.value = []
  } finally {
    isLoadingBares.value = false
  }
}

const closeBaresModal = () => {
  showBaresModal.value = false
  selectedDueno.value = null
  baresDelDueno.value = []
}

const entrarAlLocal = (barId) => {
  closeBaresModal()
  router.push({ path: `/info_locales/${barId}` })
}

const handleLogin = async () => {
  isLoading.value = true;

  try {
    const response = await fetch(`${API_BASE_URL}/gestor_principal/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        correo: email.value,
        contraseña: password.value
      })
    });

    const data = await response.json();

    if (response.ok) {
      gestorStore.login(data);

      await Swal.fire({
        icon: 'success',
        title: '¡Bienvenido!',
        text: `Hola ${data.nombre || 'Gestor Principal'}`,
        confirmButtonColor: '#ec4899',
        timer: 2000,
        timerProgressBar: true,
        willClose: () => {
          router.push({ name: 'home_admin_principal' });
        }
      });
    } else {
      const errorMessage = data.detail || 'Credenciales incorrectas';
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: errorMessage,
        confirmButtonColor: '#ec4899'
      });
    }
  } catch (error) {
    console.error('Error de conexión:', error);
    Swal.fire({
      icon: 'error',
      title: 'Sin conexión',
      text: 'No se pudo conectar al servidor. Inténtalo más tarde.',
      confirmButtonColor: '#ec4899'
    });
  } finally {
    isLoading.value = false;
  }
};

const handleForgotPassword = async () => {
  const { value: userEmail, isConfirmed } = await Swal.fire({
    title: '¿Olvidaste tu contraseña?',
    input: 'email',
    inputLabel: 'Ingresa tu correo electrónico',
    inputPlaceholder: 'admin@controlas.com',
    inputValue: email.value,
    showCancelButton: true,
    confirmButtonText: 'Enviar código',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: '#ec4899',
    inputValidator: (value) => {
      if (!value) return 'Debes ingresar un correo';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Correo inválido';
    }
  });

  if (!isConfirmed || !userEmail) return;

  userEmailForReset.value = userEmail;

  Swal.fire({
    title: 'Enviando código...',
    text: 'Por favor espera',
    allowOutsideClick: false,
    allowEscapeKey: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  try {
    const response = await fetch(`${API_BASE_URL}/gestor_principal/forgot-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ correo: userEmail })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || data.message || 'Error del servidor');
    }

    await Swal.fire({
      icon: 'success',
      title: '¡Código enviado!',
      text: `Revisa tu bandeja (y spam) en: ${userEmail}`,
      confirmButtonColor: '#ec4899',
      timer: 4000,
      timerProgressBar: true
    });

    openCodeModal();

  } catch (error) {
    console.error('Error en recuperación:', error);
    await Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'No se pudo conectar con el servidor. Verifica tu conexión o intenta más tarde.',
      confirmButtonColor: '#ec4899'
    });
  }
};

const openCodeModal = () => {
  codeDigits.value = ['', '', '', '', '', ''];
  codeError.value = '';
  showCodeModal.value = true;
  
  nextTick(() => {
    if (codeInputs.value[0]) {
      codeInputs.value[0].focus();
    }
  });
};

const closeCodeModal = () => {
  if (isVerifying.value) return;
  showCodeModal.value = false;
  codeDigits.value = ['', '', '', '', '', ''];
  codeError.value = '';
};

const handleCodeInput = (index, event) => {
  const value = event.target.value;
  
  if (value && !/^\d$/.test(value)) {
    codeDigits.value[index] = '';
    return;
  }

  codeError.value = '';

  if (value && index < 5) {
    nextTick(() => {
      codeInputs.value[index + 1]?.focus();
    });
  }
};

const handleCodeKeydown = (index, event) => {
  if (event.key === 'Backspace' && !codeDigits.value[index] && index > 0) {
    nextTick(() => {
      codeInputs.value[index - 1]?.focus();
    });
  }
  
  if (event.key === 'ArrowLeft' && index > 0) {
    event.preventDefault();
    codeInputs.value[index - 1]?.focus();
  }
  if (event.key === 'ArrowRight' && index < 5) {
    event.preventDefault();
    codeInputs.value[index + 1]?.focus();
  }
};

const handleCodePaste = (event) => {
  event.preventDefault();
  const pastedData = event.clipboardData.getData('text').trim();
  
  if (/^\d{6}$/.test(pastedData)) {
    codeDigits.value = pastedData.split('');
    codeError.value = '';
    nextTick(() => {
      codeInputs.value[5]?.focus();
    });
  }
};

const verifyCode = async () => {
  const code = codeDigits.value.join('');
  
  if (code.length !== 6) {
    codeError.value = 'Debes ingresar los 6 dígitos';
    return;
  }

  isVerifying.value = true;
  codeError.value = '';

  try {
    const response = await fetch(`${API_BASE_URL}/gestor_principal/verify-reset-code`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: code })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Código incorrecto o expirado');
    }

    resetToken.value = code;
    showCodeModal.value = false;

    await requestNewPassword();

  } catch (error) {
    codeError.value = error.message;
    codeDigits.value = ['', '', '', '', '', ''];
    nextTick(() => {
      codeInputs.value[0]?.focus();
    });
  } finally {
    isVerifying.value = false;
  }
};

const requestNewPassword = async () => {
  const { value: passwords, isConfirmed: passOk } = await Swal.fire({
    title: 'Crear nueva contraseña',
    html: `
      <input id="swal-pass1" type="password" class="swal2-input" placeholder="Nueva contraseña (mín. 6 caracteres)">
      <input id="swal-pass2" type="password" class="swal2-input" placeholder="Repetir contraseña">
    `,
    showCancelButton: true,
    confirmButtonText: 'Cambiar contraseña',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: '#ec4899',
    preConfirm: () => {
      const p1 = document.getElementById('swal-pass1').value;
      const p2 = document.getElementById('swal-pass2').value;
      if (!p1 || !p2) {
        Swal.showValidationMessage('Ambos campos son obligatorios');
        return false;
      }
      if (p1.length < 6) {
        Swal.showValidationMessage('Mínimo 6 caracteres');
        return false;
      }
      if (p1 !== p2) {
        Swal.showValidationMessage('Las contraseñas no coinciden');
        return false;
      }
      return { nueva_contraseña: p1 };
    }
  });

  if (!passOk) return;

  Swal.fire({
    title: 'Guardando nueva contraseña...',
    allowOutsideClick: false,
    didOpen: () => Swal.showLoading()
  });

  try {
    const finalResponse = await fetch(`${API_BASE_URL}/gestor_principal/reset-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        token: resetToken.value,
        nueva_contraseña: passwords.nueva_contraseña
      })
    });

    if (!finalResponse.ok) {
      const err = await finalResponse.json();
      throw new Error(err.detail || 'Error al cambiar contraseña');
    }

    await Swal.fire({
      icon: 'success',
      title: '¡Contraseña cambiada!',
      text: 'Ya puedes iniciar sesión con tu nueva contraseña.',
      confirmButtonColor: '#ec4899',
      timer: 5000,
      timerProgressBar: true
    });

  } catch (error) {
    await Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'No se pudo cambiar la contraseña',
      confirmButtonColor: '#ec4899'
    });
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.login-page-standalone {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  background: #0a0a0a;
  position: relative;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  padding: 20px;
}

/* Grid overlay animado */
.grid-overlay {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(236, 72, 153, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(236, 72, 153, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
  pointer-events: none;
}

@keyframes gridMove {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(50px, 50px);
  }
}

/* Decoraciones animadas de fondo */
.bg-decoration {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.15;
  animation: float 25s infinite ease-in-out;
  pointer-events: none;
}

.decoration-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #ec4899 0%, transparent 70%);
  top: -150px;
  left: -150px;
  animation-delay: 0s;
}

.decoration-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #f472b6 0%, transparent 70%);
  bottom: -100px;
  right: -100px;
  animation-delay: 8s;
}

.decoration-3 {
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, #ec4899 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 16s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(40px, -40px) scale(1.1);
  }
  66% {
    transform: translate(-30px, 30px) scale(0.9);
  }
}

/* Tarjeta principal */
.login-card {
  background: rgba(20, 20, 20, 0.95);
  backdrop-filter: blur(40px);
  padding: 50px 45px;
  border-radius: 28px;
  border: 1px solid rgba(236, 72, 153, 0.15);
  box-shadow: 
    0 0 0 1px rgba(236, 72, 153, 0.08),
    0 25px 70px rgba(0, 0, 0, 0.5),
    0 0 40px rgba(236, 72, 153, 0.08);
  width: 100%;
  max-width: 480px;
  text-align: center;
  position: relative;
  z-index: 1;
  animation: slideUp 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}

.card-glow {
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, #ec4899, #f472b6, #ec4899);
  border-radius: 28px;
  opacity: 0;
  filter: blur(25px);
  z-index: -1;
  transition: opacity 0.5s ease;
  animation: glowPulse 3s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% {
    opacity: 0.15;
  }
  50% {
    opacity: 0.25;
  }
}

.login-card:hover .card-glow {
  opacity: 0.3;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  margin-bottom: 40px;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 90px;
  height: 90px;
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
  border-radius: 24px;
  margin-bottom: 24px;
  box-shadow: 
    0 15px 35px rgba(236, 72, 153, 0.4),
    0 0 0 4px rgba(236, 72, 153, 0.1);
  animation: iconFloat 3s ease-in-out infinite;
  position: relative;
}

.icon-wrapper::before {
  content: '';
  position: absolute;
  inset: -4px;
  background: linear-gradient(135deg, #ec4899, #f472b6);
  border-radius: 24px;
  opacity: 0;
  filter: blur(15px);
  z-index: -1;
  animation: iconGlow 2s ease-in-out infinite;
}

@keyframes iconFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes iconGlow {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.6;
  }
}

.admin-icon {
  width: 45px;
  height: 45px;
  color: #ffffff;
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3));
}

.title {
  font-size: 36px;
  font-weight: 900;
  background: linear-gradient(135deg, #ffffff 0%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
  letter-spacing: -1px;
  text-shadow: 0 0 30px rgba(236, 72, 153, 0.3);
}

.subtitle {
  font-size: 16px;
  color: #a1a1aa;
  font-weight: 500;
  letter-spacing: 0.5px;
}

/* Formulario */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.input-group {
  text-align: left;
}

.input-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: #e4e4e7;
  margin-bottom: 12px;
  letter-spacing: 0.3px;
}

.input-group label svg {
  color: #ec4899;
}

input {
  width: 100%;
  padding: 16px 18px;
  border: 1.5px solid rgba(236, 72, 153, 0.2);
  border-radius: 14px;
  font-size: 15px;
  font-family: inherit;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  background: rgba(30, 30, 30, 0.5);
  color: #ffffff;
  font-weight: 500;
}

input:focus {
  outline: none;
  border-color: #ec4899;
  background: rgba(30, 30, 30, 0.8);
  box-shadow: 
    0 0 0 4px rgba(236, 72, 153, 0.15),
    0 8px 24px rgba(236, 72, 153, 0.2);
  transform: translateY(-2px);
}

input::placeholder {
  color: #71717a;
}

input:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.password-input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.toggle-password {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #71717a;
  transition: all 0.3s ease;
  border-radius: 10px;
}

.toggle-password:hover {
  color: #ec4899;
  background: rgba(236, 72, 153, 0.1);
  transform: scale(1.1);
}

/* Botón de olvidar contraseña */
.forgot-password-container {
  text-align: right;
  margin-top: -8px;
  animation: fadeIn 0.7s ease-out 0.3s backwards;
}

.forgot-password-link {
  background: none;
  border: none;
  color: #ec4899;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 10px 16px;
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  font-family: inherit;
  position: relative;
  letter-spacing: 0.2px;
}

.forgot-password-link::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(236, 72, 153, 0.1), rgba(244, 114, 182, 0.1));
  border-radius: 10px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.forgot-password-link:hover {
  color: #f472b6;
  transform: translateY(-2px);
}

.forgot-password-link:hover::before {
  opacity: 1;
}

.forgot-password-link:active {
  transform: translateY(0);
}

/* Botón principal */
.btn-continuar {
  width: 100%;
  padding: 18px 28px;
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
  color: #ffffff;
  border: none;
  border-radius: 14px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 
    0 0 0 1px rgba(236, 72, 153, 0.2),
    0 12px 30px rgba(236, 72, 153, 0.4);
  margin-top: 12px;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}

.btn-continuar::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-continuar span,
.btn-continuar svg {
  position: relative;
  z-index: 1;
}

.btn-continuar:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 
    0 0 0 1px rgba(236, 72, 153, 0.3),
    0 18px 40px rgba(236, 72, 153, 0.5);
}

.btn-continuar:hover:not(:disabled)::before {
  opacity: 1;
}

.btn-continuar:active:not(:disabled) {
  transform: translateY(-1px);
}

.btn-continuar:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-continuar svg {
  transition: transform 0.3s ease;
}

.btn-continuar:hover:not(:disabled) svg:not(.spinner) {
  transform: translateX(5px);
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Modal de código */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(12px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background: #141414;
  border: 1px solid rgba(236, 72, 153, 0.2);
  border-radius: 24px;
  padding: 45px 40px;
  width: 100%;
  max-width: 500px;
  box-shadow: 
    0 0 0 1px rgba(236, 72, 153, 0.1),
    0 30px 70px rgba(0, 0, 0, 0.6),
    0 0 80px rgba(236, 72, 153, 0.2);
  position: relative;
  animation: modalSlideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-close {
  position: absolute;
  top: 24px;
  right: 24px;
  background: rgba(236, 72, 153, 0.1);
  border: 1px solid rgba(236, 72, 153, 0.2);
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  color: #ec4899;
}

.modal-close:hover {
  background: rgba(236, 72, 153, 0.2);
  transform: rotate(90deg);
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
}

.modal-header {
  text-align: center;
  margin-bottom: 35px;
}

.modal-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
  border-radius: 20px;
  margin-bottom: 24px;
  box-shadow: 
    0 12px 30px rgba(236, 72, 153, 0.4),
    0 0 0 4px rgba(236, 72, 153, 0.1);
  color: #ffffff;
  animation: iconFloat 3s ease-in-out infinite;
}

.modal-header h2 {
  font-size: 26px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 10px;
  letter-spacing: -0.5px;
}

.modal-header p {
  font-size: 15px;
  color: #a1a1aa;
  font-weight: 500;
}

.modal-body {
  margin-bottom: 35px;
}

.code-input-group {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 20px;
}

.code-input {
  width: 60px;
  height: 72px;
  text-align: center;
  font-size: 28px;
  font-weight: 800;
  border: 2px solid rgba(236, 72, 153, 0.2);
  border-radius: 14px;
  background: rgba(30, 30, 30, 0.5);
  color: #ffffff;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  padding: 0;
}

.code-input:focus {
  outline: none;
  border-color: #ec4899;
  background: rgba(30, 30, 30, 0.8);
  box-shadow: 
    0 0 0 4px rgba(236, 72, 153, 0.2),
    0 8px 24px rgba(236, 72, 153, 0.3);
  transform: scale(1.08);
}

.code-input.error {
  border-color: #ef4444;
  animation: shake 0.4s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  font-weight: 600;
  text-align: center;
  margin-top: 16px;
  animation: fadeIn 0.3s ease-out;
  padding: 12px;
  background: rgba(239, 68, 68, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-modal {
  padding: 14px 28px;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: inherit;
  letter-spacing: 0.3px;
}

.btn-secondary {
  background: rgba(236, 72, 153, 0.1);
  color: #ec4899;
  border: 1px solid rgba(236, 72, 153, 0.2);
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(236, 72, 153, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(236, 72, 153, 0.2);
}

.btn-primary {
  background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
  color: #ffffff;
  box-shadow: 0 6px 20px rgba(236, 72, 153, 0.4);
  min-width: 200px;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.btn-primary::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.btn-primary span,
.btn-primary svg {
  position: relative;
  z-index: 1;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(236, 72, 153, 0.5);
}

.btn-primary:hover:not(:disabled)::before {
  opacity: 1;
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-modal:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.spinner-small {
  animation: spin 1s linear infinite;
}

/* Animaciones para inputs */
.input-group {
  animation: fadeIn 0.7s ease-out backwards;
}

.input-group:nth-child(1) {
  animation-delay: 0.15s;
}

.input-group:nth-child(2) {
  animation-delay: 0.25s;
}

.btn-continuar {
  animation: fadeIn 0.7s ease-out 0.35s backwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(15px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive - Mobile */
@media (max-width: 600px) {
  .login-page-standalone {
    padding: 16px;
  }

  .bg-decoration {
    filter: blur(60px);
  }

  .decoration-1,
  .decoration-2,
  .decoration-3 {
    width: 300px;
    height: 300px;
  }

  .grid-overlay {
    background-size: 30px 30px;
  }

  .login-card {
    padding: 40px 28px;
    border-radius: 24px;
    max-width: 100%;
  }

  .icon-wrapper {
    width: 75px;
    height: 75px;
    border-radius: 20px;
    margin-bottom: 20px;
  }

  .admin-icon {
    width: 38px;
    height: 38px;
  }

  .title {
    font-size: 28px;
    letter-spacing: -0.5px;
  }

  .subtitle {
    font-size: 14px;
  }

  .login-form {
    gap: 20px;
  }

  .input-group label {
    font-size: 13px;
    margin-bottom: 10px;
  }

  input {
    padding: 14px 16px;
    font-size: 14px;
    border-radius: 12px;
  }

  .forgot-password-link {
    font-size: 13px;
    padding: 8px 14px;
  }

  .btn-continuar {
    padding: 16px 24px;
    font-size: 15px;
    border-radius: 12px;
  }

  /* Modal responsive */
  .modal-content {
    padding: 35px 24px;
    border-radius: 20px;
    max-width: 100%;
  }

  .modal-close {
    width: 36px;
    height: 36px;
    top: 20px;
    right: 20px;
  }

  .modal-icon {
    width: 70px;
    height: 70px;
    border-radius: 18px;
    margin-bottom: 20px;
  }

  .modal-icon svg {
    width: 30px;
    height: 30px;
  }

  .modal-header h2 {
    font-size: 22px;
  }

  .modal-header p {
    font-size: 14px;
  }

  .code-input-group {
    gap: 8px;
    margin-bottom: 16px;
  }

  .code-input {
    width: 50px;
    height: 62px;
    font-size: 24px;
    border-radius: 12px;
  }

  .error-message {
    font-size: 13px;
    padding: 10px;
  }

  .modal-footer {
    flex-direction: column;
    gap: 10px;
  }

  .btn-modal {
    width: 100%;
    justify-content: center;
    padding: 14px 24px;
  }

  .btn-primary {
    min-width: auto;
  }
}

/* Responsive - Small Mobile */
@media (max-width: 380px) {
  .login-card {
    padding: 32px 20px;
  }

  .title {
    font-size: 24px;
  }

  .icon-wrapper {
    width: 65px;
    height: 65px;
  }

  .admin-icon {
    width: 32px;
    height: 32px;
  }

  .code-input {
    width: 44px;
    height: 56px;
    font-size: 22px;
  }

  .code-input-group {
    gap: 6px;
  }
}

/* Responsive - Tablets */
@media (min-width: 601px) and (max-width: 900px) {
  .login-card {
    max-width: 460px;
  }

  .modal-content {
    max-width: 480px;
  }

  .code-input {
    width: 56px;
    height: 68px;
    font-size: 26px;
  }
}

/* Animaciones adicionales para mejor UX */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Dark mode enhancements */
@media (prefers-color-scheme: dark) {
  .login-page-standalone {
    background: #0a0a0a;
  }
  
  .login-card {
    background: rgba(20, 20, 20, 0.85);
  }
  
  .modal-content {
    background: #141414;
  }
}
</style>