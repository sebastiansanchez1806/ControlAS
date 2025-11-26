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
  </div>
</template>

<script setup>
import { API_BASE_URL } from '@/config/api';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useGestorPrincipalStore } from '@/stores/gestorPrincipal';  // ← IMPORTANTE
import Swal from 'sweetalert2';

const email = ref('');
const password = ref('');
const passwordFieldType = ref('password');
const isLoading = ref(false);

const router = useRouter();
const gestorStore = useGestorPrincipalStore();  // ← EL STORE

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
      // ¡LOGIN CORRECTO! Guardamos en el store
      gestorStore.login(data);  // ← Esto guarda en Pinia + localStorage

      // Mostrar mensaje bonito
      await Swal.fire({
        icon: 'success',
        title: '¡Bienvenido!',
        text: `Hola ${data.nombre || 'Gestor Principal'}`,
        confirmButtonColor: '#667eea',
        timer: 2000,
        timerProgressBar: true,
        willClose: () => {
          // Redirigir cuando se cierre el modal
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

/* Footer */
.card-footer {
  margin-top: 30px;
  padding-top: 25px;
  border-top: 1px solid #e5e7eb;
}

.help-text {
  font-size: 14px;
  color: #6b7280;
}

.help-text a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.help-text a:hover {
  color: #764ba2;
  text-decoration: underline;
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

  .btn-continuar {
    padding: 14px 20px;
    font-size: 15px;
    border-radius: 10px;
  }

  .card-footer {
    margin-top: 25px;
    padding-top: 20px;
  }

  .help-text {
    font-size: 13px;
  }
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
</style>