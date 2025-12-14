<template>
  <div class="settings-container">
    <!-- Botón de configuración -->
    <button @click="toggleMenu" class="settings-btn" :class="{ active: isMenuOpen }">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"></path>
        <circle cx="12" cy="12" r="3"></circle>
      </svg>
    </button>

    <!-- Modal de opciones principales -->
    <transition name="modal">
      <div v-if="isMenuOpen" class="modal-overlay" @click.self="toggleMenu">
        <div class="options-modal">
          <div class="modal-header">
            <h3>Configuración</h3>
            <button @click="toggleMenu" class="close-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="options-body">
            <button 
              v-for="option in menuOptions" 
              :key="option.id"
              @click="handleOptionClick(option.id)"
              class="menu-option"
            >
              <component :is="option.icon" />
              <span>{{ option.label }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="arrow-icon">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Modal de actualización -->
    <transition name="modal">
      <div v-if="activeModal" class="modal-overlay" @click.self="closeModal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>{{ getModalTitle() }}</h3>
            <button @click="closeModal" class="close-btn">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <!-- Mensaje de error -->
            <div v-if="error" class="alert alert-error">{{ error }}</div>
            
            <!-- Mensaje de éxito -->
            <div v-if="success" class="alert alert-success">{{ success }}</div>

            <!-- Campo para nuevo nombre -->
            <div v-if="activeModal === 'name'" class="form-group">
              <label>Nuevo nombre</label>
              <input 
                v-model="newValue" 
                type="text" 
                placeholder="Ingresa tu nuevo nombre"
                class="form-input"
                @keyup.enter="handleSubmit"
              />
            </div>

            <!-- Campo para nuevo correo -->
            <div v-if="activeModal === 'email'" class="form-group">
              <label>Nuevo correo</label>
              <input 
                v-model="newValue" 
                type="email" 
                placeholder="Ingresa tu nuevo correo"
                class="form-input"
                @keyup.enter="handleSubmit"
              />
            </div>

            <!-- Campos para nueva contraseña -->
            <div v-if="activeModal === 'password'">
              <div class="form-group">
                <label>Nueva contraseña</label>
                <input 
                  v-model="newValue" 
                  type="password" 
                  placeholder="Ingresa tu nueva contraseña"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label>Confirmar contraseña</label>
                <input 
                  v-model="confirmValue" 
                  type="password" 
                  placeholder="Confirma tu nueva contraseña"
                  class="form-input"
                  @keyup.enter="handleSubmit"
                />
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="closeModal" class="btn btn-secondary">Cancelar</button>
            <button @click="handleSubmit" class="btn btn-primary">Actualizar</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>
<script setup>
import { ref, h } from 'vue';
import Swal from 'sweetalert2';

const isMenuOpen = ref(false);
const activeModal = ref(null);
const newValue = ref('');
const confirmValue = ref('');
const error = ref('');
const success = ref('');

// Iconos SVG como componentes Vue
const UserIcon = () => h('svg', {
  xmlns: 'http://www.w3.org/2000/svg',
  width: 20,
  height: 20,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 2,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
  class: 'w-5 h-5'
}, [
  h('path', { d: 'M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2' }),
  h('circle', { cx: 12, cy: 7, r: 4 })
]);

const MailIcon = () => h('svg', {
  xmlns: 'http://www.w3.org/2000/svg',
  width: 20,
  height: 20,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 2,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
  class: 'w-5 h-5'
}, [
  h('rect', { width: 20, height: 16, x: 2, y: 4, rx: 2 }),
  h('path', { d: 'm22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7' })
]);

const LockIcon = () => h('svg', {
  xmlns: 'http://www.w3.org/2000/svg',
  width: 20,
  height: 20,
  viewBox: '0 0 24 24',
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 2,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
  class: 'w-5 h-5'
}, [
  h('rect', { width: 18, height: 11, x: 3, y: 11, rx: 2, ry: 2 }),
  h('path', { d: 'M7 11V7a5 5 0 0 1 10 0v4' })
]);

const menuOptions = [
  { id: 'name', label: 'Actualizar nombre', icon: UserIcon },
  { id: 'email', label: 'Actualizar correo', icon: MailIcon },
  { id: 'password', label: 'Actualizar contraseña', icon: LockIcon }
];

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const handleOptionClick = (optionId) => {
  // Pedir contraseña actual por seguridad
  const currentPassword = prompt('Por seguridad, ingresa tu contraseña actual:');

  if (!currentPassword) {
    return;
  }

  // Simulación de validación (en producción validarías contra el backend)
  if (currentPassword.length < 4) {
    alert('Contraseña incorrecta');
    return;
  }

  // Si pasa la validación, abrir el modal correspondiente
  activeModal.value = optionId;
  isMenuOpen.value = false;
  resetForm();
};

const closeModal = () => {
  activeModal.value = null;
  resetForm();
};

const resetForm = () => {
  newValue.value = '';
  confirmValue.value = '';
  error.value = '';
  success.value = '';
};

const getModalTitle = () => {
  const titles = {
    name: 'Actualizar Nombre',
    email: 'Actualizar Correo',
    password: 'Actualizar Contraseña'
  };
  return titles[activeModal.value] || '';
};

const handleSubmit = () => {
  error.value = '';
  success.value = '';

  if (!newValue.value.trim()) {
    error.value = 'Debes ingresar el nuevo valor';
    return;
  }

  // Validaciones específicas
  if (activeModal.value === 'password') {
    if (newValue.value !== confirmValue.value) {
      error.value = 'Las contraseñas no coinciden';
      return;
    }
    if (newValue.value.length < 6) {
      error.value = 'La contraseña debe tener al menos 6 caracteres';
      return;
    }
  }

  if (activeModal.value === 'email') {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(newValue.value)) {
      error.value = 'Ingresa un correo electrónico válido';
      return;
    }
  }

  // Aquí iría la petición real al backend
  // Simulamos éxito

  closeModal();

  const updateMessages = {
    name: 'Tu nombre ha sido actualizado correctamente',
    email: 'Tu correo electrónico ha sido actualizado correctamente',
    password: 'Tu contraseña ha sido actualizada correctamente'
  };

  Swal.fire({
    icon: 'success',
    title: '¡Actualización exitosa!',
    text: updateMessages[activeModal.value],
    confirmButtonText: 'Perfecto',
    confirmButtonColor: '#ff69b4',
    timer: 3000,
    timerProgressBar: true
  });
};
</script>
<style scoped>
* {
  box-sizing: border-box;
}

.settings-container {
  position: relative;
}

.settings-btn {
  background: #fff;
  border: 2px solid #000;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #000;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

.settings-btn:hover {
  background: #ff69b4;
  border-color: #ff69b4;
  color: #fff;
  transform: rotate(90deg);
}

.settings-btn.active {
  background: #000;
  color: #fff;
}

.settings-btn:active {
  transform: scale(0.95);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
  overflow-y: auto;
}

.options-modal {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 3px solid #000;
  animation: scaleIn 0.3s ease;
  margin: auto;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 3px solid #000;
  animation: scaleIn 0.3s ease;
  margin: auto;
  max-height: 90vh;
  overflow-y: auto;
}

@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.modal-header {
  padding: 20px;
  border-bottom: 2px solid #000;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 10;
  border-radius: 16px 16px 0 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  color: #000;
  line-height: 1.2;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: #000;
  transition: all 0.2s ease;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  min-width: 40px;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.close-btn:hover {
  color: #ff69b4;
  background: rgba(255, 105, 180, 0.1);
}

.close-btn:active {
  transform: scale(0.9);
}

.options-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.menu-option {
  width: 100%;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  background: #fff;
  border: 2px solid #000;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #000;
  font-size: 15px;
  text-align: left;
  font-weight: 600;
  position: relative;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  min-height: 60px;
}

.menu-option span {
  flex: 1;
  line-height: 1.3;
}

.arrow-icon {
  opacity: 0.5;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.menu-option:active {
  transform: scale(0.98);
  background: #ff69b4;
  color: #fff;
  border-color: #ff69b4;
}

.menu-option:active .arrow-icon {
  opacity: 1;
}

.modal-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #000;
  font-size: 14px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #000;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.2s ease;
  box-sizing: border-box;
  -webkit-appearance: none;
  appearance: none;
}

.form-input:focus {
  outline: none;
  border-color: #4169e1;
  box-shadow: 0 0 0 3px rgba(65, 105, 225, 0.1);
}

.alert {
  padding: 12px 14px;
  border-radius: 8px;
  margin-bottom: 16px;
  font-size: 14px;
  line-height: 1.4;
}

.alert-error {
  background: #ffe0e0;
  color: #c00;
  border: 2px solid #c00;
}

.alert-success {
  background: #e0ffe0;
  color: #0a0;
  border: 2px solid #0a0;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 2px solid #000;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  position: sticky;
  bottom: 0;
  background: #fff;
  border-radius: 0 0 16px 16px;
}

.btn {
  padding: 14px 20px;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid #000;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
  min-height: 48px;
  flex: 1;
  max-width: 150px;
}

.btn-secondary {
  background: #fff;
  color: #000;
}

.btn-secondary:active {
  background: #f5f5f5;
  transform: scale(0.98);
}

.btn-primary {
  background: #ff69b4;
  color: #fff;
  border-color: #ff69b4;
}

.btn-primary:active {
  background: #ff1493;
  border-color: #ff1493;
  transform: scale(0.98);
}

/* Animaciones */
.modal-enter-active, .modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-from .options-modal,
.modal-enter-from .modal-content {
  transform: scale(0.9);
}

.modal-leave-to .options-modal,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}

/* Media Queries para Mobile */
@media screen and (max-width: 640px) {
  .settings-btn {
    width: 48px;
    height: 48px;
  }

  .modal-overlay {
    padding: 0;
    align-items: flex-end;
  }

  .options-modal,
  .modal-content {
    border-radius: 24px 24px 0 0;
    max-width: 100%;
    width: 100%;
    max-height: 90vh;
    border: none;
    border-top: 3px solid #000;
  }

  .modal-header {
    padding: 18px 16px;
    border-radius: 24px 24px 0 0;
  }

  .modal-header h3 {
    font-size: 18px;
  }

  .options-body {
    padding: 16px;
    gap: 12px;
  }

  .menu-option {
    padding: 16px 18px;
    font-size: 15px;
    gap: 12px;
    min-height: 64px;
  }

  .modal-body {
    padding: 16px;
  }

  .form-group {
    margin-bottom: 16px;
  }

  .form-group label {
    font-size: 14px;
    margin-bottom: 6px;
  }

  .form-input {
    padding: 14px 16px;
    font-size: 16px;
    border-radius: 10px;
  }

  .alert {
    padding: 12px 14px;
    font-size: 14px;
    margin-bottom: 16px;
  }

  .modal-footer {
    padding: 16px;
    gap: 10px;
  }

  .btn {
    padding: 14px 18px;
    font-size: 15px;
    min-height: 52px;
    flex: 1;
    max-width: none;
    border-radius: 10px;
  }

  .close-btn:hover {
    background: none;
  }

  .menu-option:hover {
    transform: none;
  }
}

@media screen and (max-width: 375px) {
  .settings-btn {
    width: 44px;
    height: 44px;
  }

  .modal-header {
    padding: 16px 14px;
  }

  .modal-header h3 {
    font-size: 17px;
  }

  .options-body {
    padding: 14px;
    gap: 10px;
  }

  .menu-option {
    padding: 14px 16px;
    font-size: 14px;
    min-height: 60px;
  }

  .modal-body {
    padding: 14px;
  }

  .form-input {
    padding: 12px 14px;
    font-size: 16px;
  }

  .btn {
    padding: 12px 16px;
    font-size: 14px;
    min-height: 48px;
  }

  .modal-footer {
    padding: 14px;
  }
}

/* iPhone SE y pantallas muy pequeñas */
@media screen and (max-width: 320px) {
  .settings-btn {
    width: 42px;
    height: 42px;
  }

  .modal-header h3 {
    font-size: 16px;
  }

  .menu-option {
    padding: 12px 14px;
    font-size: 13px;
    min-height: 56px;
  }

  .form-input {
    padding: 11px 12px;
    font-size: 16px;
  }

  .btn {
    padding: 11px 14px;
    font-size: 13px;
    min-height: 46px;
  }
}

/* Landscape Mobile */
@media screen and (max-height: 600px) and (orientation: landscape) {
  .modal-overlay {
    align-items: center;
    padding: 12px;
  }

  .options-modal,
  .modal-content {
    max-height: 95vh;
    border-radius: 16px;
    border: 3px solid #000;
  }

  .modal-header {
    padding: 12px 16px;
    border-radius: 16px 16px 0 0;
  }

  .options-body {
    padding: 12px 16px;
  }

  .modal-body {
    padding: 12px 16px;
  }

  .modal-footer {
    padding: 12px 16px;
  }

  .menu-option {
    min-height: 52px;
    padding: 12px 16px;
  }

  .btn {
    min-height: 44px;
    padding: 10px 16px;
  }
}

/* Tablet */
@media screen and (min-width: 641px) and (max-width: 1024px) {
  .options-modal {
    max-width: 500px;
  }

  .modal-content {
    max-width: 550px;
  }

  .menu-option:hover {
    background: #ff69b4;
    color: #fff;
    border-color: #ff69b4;
    transform: translateX(8px);
  }

  .menu-option:hover .arrow-icon {
    opacity: 1;
    transform: translateX(4px);
  }

  .btn-secondary:hover {
    background: #f5f5f5;
  }

  .btn-primary:hover {
    background: #ff1493;
    border-color: #ff1493;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);
  }
}

/* Desktop */
@media screen and (min-width: 1025px) {
  .menu-option:hover {
    background: #ff69b4;
    color: #fff;
    border-color: #ff69b4;
    transform: translateX(8px);
  }

  .menu-option:hover .arrow-icon {
    opacity: 1;
    transform: translateX(4px);
  }

  .close-btn:hover {
    transform: rotate(90deg);
  }

  .btn-secondary:hover {
    background: #f5f5f5;
  }

  .btn-primary:hover {
    background: #ff1493;
    border-color: #ff1493;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);
  }
}

/* iPad específico */
@media screen and (min-width: 768px) and (max-width: 1024px) {
  .modal-overlay {
    padding: 20px;
  }

  .options-modal,
  .modal-content {
    border-radius: 16px;
    border: 3px solid #000;
  }

  .modal-header {
    border-radius: 16px 16px 0 0;
  }
}

/* Mejoras para touch devices */
@media (hover: none) and (pointer: coarse) {
  .settings-btn:hover {
    transform: none;
    background: #fff;
    color: #000;
    border-color: #000;
  }

  .menu-option:hover {
    transform: none;
    background: #fff;
    color: #000;
    border-color: #000;
  }

  .close-btn:hover {
    transform: none;
    background: none;
  }

  .btn-secondary:hover {
    background: #fff;
    transform: none;
  }

  .btn-primary:hover {
    background: #ff69b4;
    border-color: #ff69b4;
    transform: none;
    box-shadow: none;
  }
}
</style>