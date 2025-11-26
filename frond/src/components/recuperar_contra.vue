<template>
  <div class="main-container">
    <!-- Particles Background -->
    <div class="particles-background"></div>
    
    <!-- Security Shield Animation -->
    <div class="security-shield">
      <div class="shield-icon">🛡️</div>
    </div>

    <header class="header">
      <div class="header-content">
        <button @click="goBack" class="back-button">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          <span class="back-text">Volver</span>
        </button>
        <h1 class="header-title glitch" data-text="VALKA">Control AS</h1>
        <div class="security-badge">
          <span class="security-text">SECURE</span>
          <div class="security-dot"></div>
        </div>
      </div>
    </header>

    <main class="content-container">
      <div class="card">
        <div class="card-header">
          <div class="lock-icon">🔐</div>
          <h2 class="card-title">Recuperar Contraseña</h2>
          <div class="security-line"></div>
        </div>
        
        <div class="warning-banner">
          <div class="warning-icon">⚠️</div>
          <p class="warning-text">
            Esta función es <strong>exclusiva</strong> para dueños de bar.<br>
            Si eres administrador, contacta al dueño para cambiar tu contraseña.
          </p>
        </div>

        <div v-if="!showResetForm" class="form-container">
          <div class="input-group">
            <label for="correo" class="form-label">
              <span class="label-icon">📧</span>
              Correo Electrónico
            </label>
            <div class="input-wrapper">
              <input
                id="correo"
                type="email"
                v-model="email"
                placeholder="ejemplo@dominio.com"
                class="form-input"
                :class="{ 'input-error': emailError }"
                @input="validateEmail"
                @blur="validateEmail"
                autocomplete="email"
                spellcheck="false"
              />
              <div v-if="emailError" class="error-message">
                {{ emailError }}
              </div>
            </div>
          </div>
          
          <button
            @click="requestResetCode"
            :disabled="isLoading || !isValidEmail"
            class="action-button primary-button"
          >
            <span v-if="isLoading" class="loading-spinner"></span>
            <span class="button-icon">🚀</span>
            {{ isLoading ? 'Enviando código...' : 'Enviar Código de Seguridad' }}
          </button>
        </div>

        <div v-else class="form-container">
          <div class="progress-bar">
            <div class="progress-step active">1</div>
            <div class="progress-line active"></div>
            <div class="progress-step active">2</div>
          </div>
          
          <div class="input-group">
            <label for="codigo" class="form-label">
              <span class="label-icon">🔢</span>
              Código de Verificación
            </label>
            <div class="input-wrapper">
              <input
                id="codigo"
                type="text"
                v-model="token"
                placeholder=""
                class="form-input code-input"
                maxlength="6"
                @input="formatCode"
                autocomplete="one-time-code"
              />
              <div class="input-help">Código de 6 dígitos enviado a tu email</div>
            </div>
          </div>
          
          <div class="input-group">
            <label for="nueva-contraseña" class="form-label">
              <span class="label-icon">🔒</span>
              Nueva Contraseña
            </label>
            <div class="input-wrapper">
              <input
                id="nueva-contraseña"
                :type="showPassword ? 'text' : 'password'"
                v-model="newPassword"
                placeholder="Mínimo 8 caracteres"
                class="form-input"
                :class="{ 'input-error': passwordError }"
                @input="validatePassword"
                autocomplete="new-password"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="password-toggle"
              >
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
              <div v-if="passwordError" class="error-message">
                {{ passwordError }}
              </div>
              <div class="password-strength">
                <div class="strength-bar" :class="passwordStrength"></div>
                <span class="strength-text">{{ getStrengthText() }}</span>
              </div>
            </div>
          </div>
          
          <button
            @click="resetPassword"
            :disabled="isLoading || !isValidPassword"
            class="action-button secondary-button"
          >
            <span v-if="isLoading" class="loading-spinner"></span>
            <span class="button-icon">✅</span>
            {{ isLoading ? 'Restableciendo...' : 'Restablecer Contraseña' }}
          </button>
          
          <button
            @click="goBackToEmail"
            class="link-button"
          >
            ← Cambiar correo electrónico
          </button>
        </div>
      </div>
    </main>

    <footer class="footer">
      <div class="footer-content">
        <p>&copy; 2024 Control AS. Todos los derechos reservados.</p>
        <div class="footer-security">
          <span class="security-badge-small">
            <span class="security-dot-small"></span>
            Conexión Segura SSL
          </span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Swal from 'sweetalert2';
// *** 1. IMPORTACIÓN DE LA CONSTANTE GLOBAL CON RUTA RELATIVA ***
import { API_BASE_URL } from '../config/api'; 
// *************************************************************

const router = useRouter();
const showResetForm = ref(false);
const email = ref('');
const token = ref('');
const newPassword = ref('');
const isLoading = ref(false);
const emailError = ref('');
const passwordError = ref('');
const showPassword = ref(false);

// Security validations
const isValidEmail = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email.value) && !emailError.value;
});

const isValidPassword = computed(() => {
  return newPassword.value.length >= 8 && !passwordError.value;
});

const passwordStrength = computed(() => {
  const password = newPassword.value;
  let score = 0;
  
  // Evaluación más flexible basada solo en longitud y variedad de caracteres
  if (password.length >= 8) score++;
  if (password.length >= 12) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;
  
  if (score <= 2) return 'weak';
  if (score <= 4) return 'medium';
  return 'strong';
});

// Eliminada: const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://192.168.100.37:8000';
// Ahora se usa la API_BASE_URL importada

// Security headers for requests
const secureHeaders = {
  'Content-Type': 'application/json',
  'X-Requested-With': 'XMLHttpRequest',
  'X-CSRF-Token': 'secure-token'
};

const goBack = () => {
  router.go(-1);
};

const goBackToEmail = () => {
  showResetForm.value = false;
  token.value = '';
  newPassword.value = '';
};

const validateEmail = () => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email.value) {
    emailError.value = 'El correo es obligatorio';
  } else if (!emailRegex.test(email.value)) {
    emailError.value = 'Formato de correo inválido';
  } else if (email.value.length > 254) {
    emailError.value = 'Correo demasiado largo';
  } else {
    emailError.value = '';
  }
};

const validatePassword = () => {
  if (!newPassword.value) {
    passwordError.value = 'La contraseña es obligatoria';
  } else if (newPassword.value.length < 8) {
    passwordError.value = 'Mínimo 8 caracteres';
  } else if (newPassword.value.length > 128) {
    passwordError.value = 'Máximo 128 caracteres';
  } else {
    passwordError.value = '';
  }
};

const formatCode = () => {
  // Only allow numbers
  token.value = token.value.replace(/\D/g, '').slice(0, 6);
};

const getStrengthText = () => {
  const strength = passwordStrength.value;
  if (strength === 'weak') return 'Débil';
  if (strength === 'medium') return 'Media';
  return 'Fuerte';
};

// Rate limiting protection
let requestCount = 0;
const maxRequests = 3;
const rateLimitReset = 5 * 60 * 1000; // 5 minutes

const requestResetCode = async () => {
  // Rate limiting check
  if (requestCount >= maxRequests) {
    Swal.fire({
      icon: 'warning',
      title: 'Demasiados intentos',
      text: 'Espera 5 minutos antes de intentar nuevamente.',
      confirmButtonColor: '#ff69b4',
    });
    return;
  }

  if (!isValidEmail.value) {
    validateEmail();
    return;
  }

  isLoading.value = true;
  requestCount++;
  
  try {
    // Input sanitization
    const sanitizedEmail = email.value.trim().toLowerCase();
    
    // *** USO DE LA CONSTANTE GLOBAL ***
    const response = await axios.post(`${API_BASE_URL}/dueno/forgot-password`, {
      correo: sanitizedEmail,
    }, {
      headers: secureHeaders,
      timeout: 10000 // 10 second timeout
    });

    Swal.fire({
      icon: 'success',
      title: 'Código enviado',
      html: `
        <p>Si el correo está registrado como <strong>dueño</strong>, recibirás un código.</p>
        <p>Revisa tu bandeja de entrada y spam.</p>
        <div style="background: #f0f8ff; padding: 10px; border-radius: 5px; margin-top: 10px;">
          <small>⏱️ El código expira en 15 minutos</small>
        </div>
      `,
      confirmButtonColor: '#ff69b4',
    });
    
    showResetForm.value = true;
    
    // Reset rate limiting after success
    setTimeout(() => {
      requestCount = Math.max(0, requestCount - 1);
    }, rateLimitReset);
    
  } catch (error) {
    console.error('Error al solicitar el código:', error);
    
    let errorMessage = 'Error de conexión. Verifica tu internet.';
    
    if (error.code === 'ECONNABORTED') {
      errorMessage = 'Tiempo de espera agotado. Intenta nuevamente.';
    } else if (error.response?.status === 429) {
      errorMessage = 'Demasiados intentos. Espera antes de intentar nuevamente.';
    } else if (error.response?.status === 422) {
      errorMessage = 'Datos inválidos. Verifica el formato del correo.';
    }
    
    Swal.fire({
      icon: 'error',
      title: 'Error de seguridad',
      text: errorMessage,
      confirmButtonColor: '#ff69b4',
    });
  } finally {
    isLoading.value = false;
  }
};

const resetPassword = async () => {
  if (!isValidPassword.value) {
    validatePassword();
    return;
  }
  
  if (!token.value || token.value.length !== 6) {
    Swal.fire({
      icon: 'warning',
      title: 'Código incompleto',
      text: 'Ingresa el código de 6 dígitos.',
      confirmButtonColor: '#ff69b4',
    });
    return;
  }

  isLoading.value = true;
  
  try {
    // Input sanitization
    const sanitizedToken = token.value.replace(/\D/g, '');
    const sanitizedPassword = newPassword.value.trim();
    
    // *** USO DE LA CONSTANTE GLOBAL ***
    const response = await axios.post(`${API_BASE_URL}/dueno/reset-password`, {
      token: sanitizedToken,
      nueva_contraseña: sanitizedPassword,
    }, {
      headers: secureHeaders,
      timeout: 10000
    });

    await Swal.fire({
      icon: 'success',
      title: '¡Contraseña actualizada!',
      html: `
        <p>Tu contraseña se ha actualizado exitosamente.</p>
        <div style="background: #e8f5e8; padding: 10px; border-radius: 5px; margin-top: 10px;">
          <small>🔒 Tu cuenta está ahora más segura</small>
        </div>
      `,
      confirmButtonColor: '#ff69b4',
    });

    // Clear sensitive data
    token.value = '';
    newPassword.value = '';
    email.value = '';
    
    router.push('/login');
    
  } catch (error) {
    console.error('Error al restablecer la contraseña:', error);
    
    let errorMessage = 'Error de conexión. Intenta nuevamente.';
    
    if (error.response?.status === 400) {
      errorMessage = 'Código inválido o expirado. Solicita uno nuevo.';
    } else if (error.response?.status === 422) {
      errorMessage = 'Datos inválidos. Verifica el código y contraseña.';
    }
    
    Swal.fire({
      icon: 'error',
      title: 'Error al restablecer',
      text: errorMessage,
      confirmButtonColor: '#ff69b4',
    });
  } finally {
    isLoading.value = false;
  }
};

// Cleanup sensitive data on component unmount
onUnmounted(() => {
  token.value = '';
  newPassword.value = '';
  email.value = '';
});
</script>
<style scoped>
* {
  box-sizing: border-box;
}

.main-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(135deg, #000000 0%, #1a1a2e 50%, #16213e 100%);
  color: #ffffff;
  overflow-x: hidden;
  position: relative;
}

/* ================ PARTICLES BACKGROUND ================ */
.particles-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-image: 
    radial-gradient(2px 2px at 20px 30px, #ff69b4, transparent),
    radial-gradient(2px 2px at 40px 70px, #007bff, transparent),
    radial-gradient(1px 1px at 90px 40px, #ffffff, transparent),
    radial-gradient(1px 1px at 130px 80px, #ff69b4, transparent),
    radial-gradient(2px 2px at 160px 30px, #007bff, transparent);
  animation: particles 20s linear infinite;
}

@keyframes particles {
  0% { transform: translate(0, 0) rotate(0deg); }
  33% { transform: translate(30px, -30px) rotate(120deg); }
  66% { transform: translate(-20px, 20px) rotate(240deg); }
  100% { transform: translate(0, 0) rotate(360deg); }
}

/* ================ SECURITY SHIELD ================ */
.security-shield {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 10;
  animation: securityPulse 3s infinite;
}

.shield-icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 0 10px #ff69b4);
}

@keyframes securityPulse {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.1); opacity: 1; }
}

/* ================ HEADER CON GLITCH ================ */
.header {
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 2px solid #ff69b4;
  padding: 1rem 1.5rem;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 30px rgba(255, 105, 180, 0.3);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(45deg, #ff69b4, #ff1493);
  border: none;
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
}

.back-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 105, 180, 0.6);
}

.back-text {
  font-size: 0.85rem;
  letter-spacing: 0.5px;
}

.header-title {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  margin: 0;
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  font-weight: 900;
  letter-spacing: 3px;
  color: #ff69b4;
}

/* GLITCH EFFECT */
.glitch {
  position: relative;
  animation: glitch 3s infinite;
}

.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.glitch::before {
  animation: glitch-1 0.5s infinite;
  color: #007bff;
  z-index: -1;
}

.glitch::after {
  animation: glitch-2 0.5s infinite;
  color: #ffffff;
  z-index: -2;
}

@keyframes glitch {
  0%, 98% { transform: translate(0); }
  1% { transform: translate(-2px, 2px); }
  2% { transform: translate(2px, -2px); }
  3% { transform: translate(0); }
}

@keyframes glitch-1 {
  0%, 98% { transform: translate(0); }
  1% { transform: translate(2px, -2px); }
  2% { transform: translate(-2px, 2px); }
  3% { transform: translate(0); }
}

@keyframes glitch-2 {
  0%, 98% { transform: translate(0); }
  1% { transform: translate(-1px, 1px); }
  2% { transform: translate(1px, -1px); }
  3% { transform: translate(0); }
}

.security-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 123, 255, 0.2);
  padding: 0.5rem 0.75rem;
  border-radius: 20px;
  border: 1px solid #007bff;
}

.security-text {
  font-size: 0.7rem;
  font-weight: 700;
  color: #007bff;
  letter-spacing: 1px;
}

.security-dot {
  width: 8px;
  height: 8px;
  background: #00ff00;
  border-radius: 50%;
  animation: securityBlink 2s infinite;
}

@keyframes securityBlink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0.3; }
}

/* ================ CONTENT CONTAINER ================ */
.content-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  position: relative;
}

.card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 105, 180, 0.3);
  border-radius: 20px;
  padding: 2.5rem;
  max-width: 500px;
  width: 100%;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.3),
    0 0 20px rgba(255, 105, 180, 0.2);
  color: #333;
  animation: cardFloat 6s ease-in-out infinite;
}

@keyframes cardFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.lock-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: lockPulse 2s infinite;
}

@keyframes lockPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.card-title {
  color: #333;
  margin: 0;
  font-size: clamp(1.5rem, 4vw, 2rem);
  font-weight: 700;
  margin-bottom: 1rem;
}

.security-line {
  width: 100px;
  height: 3px;
  background: linear-gradient(90deg, #ff69b4, #007bff);
  margin: 0 auto;
  border-radius: 2px;
}

/* ================ WARNING BANNER ================ */
.warning-banner {
  background: linear-gradient(135deg, #fff3cd, #ffeaa7);
  border: 2px solid #ffc107;
  border-radius: 15px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  animation: warningGlow 3s infinite;
}

@keyframes warningGlow {
  0%, 100% { box-shadow: 0 0 5px rgba(255, 193, 7, 0.3); }
  50% { box-shadow: 0 0 15px rgba(255, 193, 7, 0.6); }
}

.warning-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.warning-text {
  margin: 0;
  color: #856404;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* ================ PROGRESS BAR ================ */
.progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  gap: 1rem;
}

.progress-step {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #666;
  transition: all 0.3s ease;
}

.progress-step.active {
  background: linear-gradient(45deg, #ff69b4, #007bff);
  color: white;
  box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4);
}

.progress-line {
  width: 60px;
  height: 3px;
  background: #e0e0e0;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.progress-line.active {
  background: linear-gradient(90deg, #ff69b4, #007bff);
}

/* ================ FORM STYLES ================ */
.form-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.input-group {
  color: white;
  position: relative;
  
}

.form-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  
  margin-bottom: 0.75rem;
  color: #333;
  font-size: 0.95rem;
}

.label-icon {
  font-size: 1.1rem;
  
}

.input-wrapper {
  
  position: relative;
}

.form-input {
  width: 100%;
  padding: 1rem 1.25rem;
  border: 2px solid #e0e0e0;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  color: #333;
  
}

.form-input:focus {
  outline: none;
  border-color: #ff69b4;
  box-shadow: 0 0 0 3px rgba(255, 105, 180, 0.1);
  color: #000;
  transform: translateY(-1px);
}

.form-input.input-error {
  border-color: #dc3545;
  background-color: #fff5f5;
}

.code-input {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: 4px;
  font-family: 'Courier New', monospace;
}

.password-toggle {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.password-toggle:hover {
  background: rgba(0, 0, 0, 0.1);
}

.error-message {
  color: #dc3545;
  font-size: 0.85rem;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.error-message::before {
  content: "⚠️";
  font-size: 0.8rem;
}

.input-help {
  color: #666;
  font-size: 0.8rem;
  margin-top: 0.5rem;
  text-align: center;
}

/* ================ PASSWORD STRENGTH ================ */
.password-strength {
  margin-top: 0.75rem;
}

.strength-bar {
  height: 4px;
  border-radius: 2px;
  transition: all 0.3s ease;
  margin-bottom: 0.5rem;
}

.strength-bar.weak {
  width: 33%;
  background: linear-gradient(90deg, #dc3545, #ff6b6b);
}

.strength-bar.medium {
  width: 66%;
  background: linear-gradient(90deg, #ffc107, #ffeb3b);
}

.strength-bar.strong {
  width: 100%;
  background: linear-gradient(90deg, #28a745, #4caf50);
}

.strength-text {
  font-size: 0.8rem;
  font-weight: 600;
  color: #666;
}

/* ================ BUTTONS ================ */
.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1.25rem 2rem;
  font-size: 1rem;
  font-weight: 700;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

.action-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.action-button:hover::before {
  left: 100%;
}

.primary-button {
  background: linear-gradient(135deg, #ff69b4, #ff1493);
  color: white;
  box-shadow: 0 8px 25px rgba(255, 105, 180, 0.4);
}

.primary-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(255, 105, 180, 0.6);
}

.secondary-button {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.4);
}

.secondary-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 12px 35px rgba(0, 123, 255, 0.6);
}

.action-button:disabled {
  background: linear-gradient(135deg, #e0e0e0, #bdbdbd);
  color: #9e9e9e;
  cursor: not-allowed;
  transform: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.button-icon {
  font-size: 1.2rem;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.link-button {
  background: none;
  border: none;
  color: #007bff;
  font-size: 0.9rem;
  cursor: pointer;
  padding: 0.5rem;
  text-decoration: underline;
  transition: all 0.2s ease;
  margin-top: 1rem;
}

.link-button:hover {
  color: #0056b3;
  transform: translateX(-2px);
}

/* ================ FOOTER ================ */
.footer {
  background: rgba(0, 0, 0, 0.95);
  backdrop-filter: blur(10px);
  border-top: 2px solid rgba(255, 105, 180, 0.3);
  padding: 1.5rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

.footer-content p {
  margin: 0;
  color: #888;
  font-size: 0.9rem;
}

.footer-security {
  display: flex;
  align-items: center;
  justify-content: center;
}

.security-badge-small {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 123, 255, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 15px;
  border: 1px solid rgba(0, 123, 255, 0.3);
  font-size: 0.8rem;
  color: #007bff;
}

.security-dot-small {
  width: 6px;
  height: 6px;
  background: #00ff00;
  border-radius: 50%;
  animation: securityBlink 2s infinite;
}

/* ================ RESPONSIVE DESIGN ================ */
@media (max-width: 768px) {
  .header {
    padding: 0.75rem 1rem;
  }
  
  .header-content {
    gap: 1rem;
  }
  
  .header-title {
    position: static;
    transform: none;
    font-size: 1.5rem;
    letter-spacing: 2px;
  }
  
  .back-button {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }
  
  .back-text {
    display: none;
  }
  
  .security-badge {
    padding: 0.25rem 0.5rem;
  }
  
  .security-text {
    font-size: 0.6rem;
  }
  
  .card {
    padding: 1.5rem;
    margin: 1rem 0.5rem;
    border-radius: 15px;
  }
  
  .warning-banner {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.5rem;
  }
  
  .progress-bar {
    gap: 0.5rem;
  }
  
  .progress-step {
    width: 30px;
    height: 30px;
    font-size: 0.8rem;
  }
  
  .progress-line {
    width: 40px;
  }
  
  .action-button {
    padding: 1rem 1.5rem;
    font-size: 0.9rem;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .footer-content p {
    font-size: 0.8rem;
  }
}

@media (max-width: 480px) {
  .security-shield {
    top: 10px;
    right: 10px;
  }
  
  .shield-icon {
    font-size: 1.2rem;
  }
  
  .header {
    padding: 0.5rem 0.75rem;
  }
  
  .header-title {
    font-size: 1.3rem;
    letter-spacing: 1px;
  }
  
  .card {
    padding: 1rem;
    margin: 0.5rem;
  }
  
  .card-title {
    font-size: 1.3rem;
  }
  
  .lock-icon {
    font-size: 2rem;
  }
  
  .form-input {
    padding: 0.875rem 1rem;
    font-size: 0.9rem;
  }
  
  .code-input {
    font-size: 1.2rem;
    letter-spacing: 2px;
  }
  
  .action-button {
    padding: 0.875rem 1.25rem;
    font-size: 0.85rem;
  }
  
  .warning-banner {
    padding: 1rem;
  }
  
  .warning-text {
    font-size: 0.85rem;
  }
  
  .progress-step {
    width: 25px;
    height: 25px;
    font-size: 0.7rem;
  }
  
  .progress-line {
    width: 30px;
    height: 2px;
  }
}

/* ================ ACCESSIBILITY ================ */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  
  .particles-background {
    animation: none;
  }
  
  .glitch,
  .glitch::before,
  .glitch::after {
    animation: none;
  }
}

/* ================ HIGH CONTRAST MODE ================ */
@media (prefers-contrast: high) {
  .card {
    border-width: 3px;
    background: #ffffff;
  }
  
  .form-input {
    border-width: 3px;
  }
  
  .action-button {
    border: 3px solid currentColor;
  }
}

/* ================ DARK MODE SUPPORT ================ */
@media (prefers-color-scheme: dark) {
  .card {
    background: rgba(30, 30, 30, 0.95);
    color: #ffffff;
  }
  
  .form-input {
    background: rgba(50, 50, 50, 0.9);
    color: #ffffff;
    border-color: #555;
  }
  
  .form-input:focus {
    border-color: #ff69b4;
  }
  
  .form-label {
    color: #ffffff;
  }
  
  .card-title {
    color: #ffffff;
  }
}

/* ================ PRINT STYLES ================ */
@media print {
  .particles-background,
  .security-shield,
  .glitch::before,
  .glitch::after {
    display: none;
  }
  
  .main-container {
    background: white;
    color: black;
  }
  
  .card {
    box-shadow: none;
    border: 2px solid #000;
  }
}
</style>