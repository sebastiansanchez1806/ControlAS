<template>
  <div class="login-page-standalone">
    <!-- Efectos de fondo animados -->
    <div class="bg-decoration decoration-1"></div>
    <div class="bg-decoration decoration-2"></div>
    <div class="bg-decoration decoration-3"></div>
    
    <div class="login-card">
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

// Variables para el modal de código
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
        confirmButtonColor: '#667eea',
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
        confirmButtonColor: '#667eea'
      });
    }
  } catch (error) {
    console.error('Error de conexión:', error);
    Swal.fire({
      icon: 'error',
      title: 'Sin conexión',
      text: 'No se pudo conectar al servidor. Inténtalo más tarde.',
      confirmButtonColor: '#667eea'
    });
  } finally {
    isLoading.value = false;
  }
};

const handleForgotPassword = async () => {
  // Paso 1: Pedir correo
  const { value: userEmail, isConfirmed } = await Swal.fire({
    title: '¿Olvidaste tu contraseña?',
    input: 'email',
    inputLabel: 'Ingresa tu correo electrónico',
    inputPlaceholder: 'admin@controlas.com',
    inputValue: email.value,
    showCancelButton: true,
    confirmButtonText: 'Enviar código',
    cancelButtonText: 'Cancelar',
    confirmButtonColor: '#667eea',
    inputValidator: (value) => {
      if (!value) return 'Debes ingresar un correo';
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return 'Correo inválido';
    }
  });

  if (!isConfirmed || !userEmail) return;

  userEmailForReset.value = userEmail;

  // Mostrar loading
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

    // Éxito: código enviado
    await Swal.fire({
      icon: 'success',
      title: '¡Código enviado!',
      text: `Revisa tu bandeja (y spam) en: ${userEmail}`,
      confirmButtonColor: '#667eea',
      timer: 4000,
      timerProgressBar: true
    });

    // Abrir modal de código
    openCodeModal();

  } catch (error) {
    console.error('Error en recuperación:', error);
    await Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'No se pudo conectar con el servidor. Verifica tu conexión o intenta más tarde.',
      confirmButtonColor: '#667eea'
    });
  }
};

const openCodeModal = () => {
  // Reset
  codeDigits.value = ['', '', '', '', '', ''];
  codeError.value = '';
  showCodeModal.value = true;
  
  // Focus en el primer input después de que el modal se renderice
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
  
  // Solo permitir números
  if (value && !/^\d$/.test(value)) {
    codeDigits.value[index] = '';
    return;
  }

  codeError.value = '';

  // Si hay un valor, moverse al siguiente input
  if (value && index < 5) {
    nextTick(() => {
      codeInputs.value[index + 1]?.focus();
    });
  }
};

const handleCodeKeydown = (index, event) => {
  // Backspace: borrar y volver al anterior
  if (event.key === 'Backspace' && !codeDigits.value[index] && index > 0) {
    nextTick(() => {
      codeInputs.value[index - 1]?.focus();
    });
  }
  
  // Flechas izquierda/derecha
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
  
  // Solo aceptar 6 dígitos
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
    // ✅ NUEVO ENDPOINT solo para verificar
    const response = await fetch(`${API_BASE_URL}/gestor_principal/verify-reset-code`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token: code })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Código incorrecto o expirado');
    }

    // Código válido
    resetToken.value = code;
    showCodeModal.value = false;

    // Pedir nueva contraseña
    await requestNewPassword();

  } catch (error) {
    codeError.value = error.message;
    // Limpiar código para reintentar
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
    confirmButtonColor: '#667eea',
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

  // Enviar cambio final
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
      confirmButtonColor: '#667eea',
      timer: 5000,
      timerProgressBar: true
    });

  } catch (error) {
    await Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message || 'No se pudo cambiar la contraseña',
      confirmButtonColor: '#667eea'
    });
  }
};
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  padding: 20px;
}

/* Decoraciones animadas de fondo */
.bg-decoration {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
  animation: float 20s infinite ease-in-out;
}

.decoration-1 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  top: -100px;
  left: -100px;
  animation-delay: 0s;
}

.decoration-2 {
  width: 350px;
  height: 350px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  bottom: -80px;
  right: -80px;
  animation-delay: 5s;
}

.decoration-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 10s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

/* Tarjeta principal */
.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 50px 45px;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 460px;
  text-align: center;
  position: relative;
  z-index: 1;
  animation: slideUp 0.6s ease-out;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-header {
  margin-bottom: 35px;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  margin-bottom: 20px;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
  }
}

.admin-icon {
  width: 40px;
  height: 40px;
  color: #ffffff;
}

.title {
  font-size: 32px;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 16px;
  color: #6b7280;
  font-weight: 500;
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
  color: #374151;
  margin-bottom: 10px;
}

.input-group label svg {
  color: #667eea;
}

input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  font-size: 15px;
  font-family: inherit;
  transition: all 0.3s ease;
  background: #ffffff;
  color: #1f2937;
}

input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

input::placeholder {
  color: #9ca3af;
}

input:disabled {
  opacity: 0.6;
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
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  transition: color 0.3s ease;
  border-radius: 8px;
}

.toggle-password:hover {
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

/* Botón de olvidar contraseña */
.forgot-password-container {
  text-align: right;
  margin-top: -8px;
  animation: fadeIn 0.6s ease-out 0.25s backwards;
}

.forgot-password-link {
  background: none;
  border: none;
  color: #667eea;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.3s ease;
  font-family: inherit;
  position: relative;
}

.forgot-password-link::after {
  content: '';
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 6px;
  left: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.forgot-password-link:hover {
  color: #764ba2;
  background: rgba(102, 126, 234, 0.05);
  transform: translateY(-2px);
}

.forgot-password-link:hover::after {
  width: 80%;
}

.forgot-password-link:active {
  transform: translateY(0);
}

/* Botón principal */
.btn-continuar {
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
  margin-top: 10px;
}

.btn-continuar:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
}

.btn-continuar:active:not(:disabled) {
  transform: translateY(-1px);
}

.btn-continuar:disabled {
  opacity: 0.7;
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
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background: #ffffff;
  border-radius: 20px;
  padding: 40px 35px;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
  position: relative;
  animation: modalSlideUp 0.4s ease-out;
}

@keyframes modalSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-close {
  position: absolute;
  top: 20px;
  right: 20px;
  background: #f3f4f6;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #6b7280;
}

.modal-close:hover {
  background: #e5e7eb;
  color: #374151;
  transform: rotate(90deg);
}

.modal-header {
  text-align: center;
  margin-bottom: 30px;
}

.modal-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  margin-bottom: 20px;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.25);
  color: #ffffff;
}

.modal-header h2 {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 8px;
}

.modal-header p {
  font-size: 15px;
  color: #6b7280;
  font-weight: 500;
}

.modal-body {
  margin-bottom: 30px;
}

.code-input-group {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 16px;
}

.code-input {
  width: 56px;
  height: 64px;
  text-align: center;
  font-size: 24px;
  font-weight: 700;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  background: #ffffff;
  color: #1f2937;
  transition: all 0.3s ease;
  padding: 0;
}

.code-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.15);
  transform: scale(1.05);
}

.code-input.error {
  border-color: #ef4444;
  animation: shake 0.4s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-8px); }
  75% { transform: translateX(8px); }
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  font-weight: 600;
  text-align: center;
  margin-top: 12px;
  animation: fadeIn 0.3s ease-out;
}

.modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-modal {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: inherit;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
  transform: translateY(-2px);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  min-width: 180px;
  justify-content: center;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-modal:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-small {
  animation: spin 1s linear infinite;
}

/* Animación adicional para inputs */
.input-group {
  animation: fadeIn 0.6s ease-out backwards;
}

.input-group:nth-child(1) {
  animation-delay: 0.1s;
}

.input-group:nth-child(2) {
  animation-delay: 0.2s;
}

.btn-continuar {
  animation: fadeIn 0.6s ease-out 0.3s backwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive - Mobile */
@media (max-width: 600px) {
  .login-page-standalone {
    padding: 15px;
  }

  .bg-decoration {
    display: none;
  }

  .login-card {
    padding: 35px 25px;
    border-radius: 20px;
  }

  .icon-wrapper {
    width: 70px;
    height: 70px;
    border-radius: 16px;
  }

  .admin-icon {
    width: 35px;
    height: 35px;
  }

  .title {
    font-size: 26px;
  }

  .subtitle {
    font-size: 14px;
  }

  .login-form {
    gap: 20px;
  }

  .input-group label {
    font-size: 13px;
    margin-bottom: 8px;
  }

  input {
    padding: 12px 14px;
    font-size: 14px;
    border-radius: 10px;
  }

  .forgot-password-link {
    font-size: 13px;
  }

  .btn-continuar {
    padding: 14px 20px;
    font-size: 15px;
    border-radius: 10px;
  }

  /* Modal responsive */
  .modal-content {
    padding: 30px 20px;
    border-radius: 16px;
  }

  .modal-icon {
    width: 60px;
    height: 60px;
    border-radius: 14px;
    margin-bottom: 16px;
  }

  .modal-icon svg {
    width: 28px;
    height: 28px;
  }

  .modal-header h2 {
    font-size: 20px;
  }

  .modal-header p {
    font-size: 14px;
  }

  .code-input-group {
    gap: 8px;
  }

  .code-input {
    width: 48px;
    height: 56px;
    font-size: 20px;
    border-radius: 10px;
  }

  .modal-footer {
    flex-direction: column;
    gap: 10px;
  }

  .btn-modal {
    width: 100%;
    justify-content: center;
  }

  .btn-primary {
    min-width: auto;
  }
}

/* Responsive - Tablets */
@media (min-width: 601px) and (max-width: 900px) {
  .login-card {
    max-width: 420px;
  }

  .modal-content {
    max-width: 440px;
  }

  .code-input {
    width: 52px;
    height: 60px;
  }
}
</style>