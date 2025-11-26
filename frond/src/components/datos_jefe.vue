<template>
  <div class="settings-page">
    <div class="settings-container">
      <div class="back-button-container">
        <button @click="goBack" class="back-button">
          <svg xmlns="http://www.w3.org/2000/svg" class="back-icon" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd"
              d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
              clip-rule="evenodd" />
          </svg>
          <span>Volver</span>
        </button>
      </div>

      <div class="profile-section">
<div class="user-photo-container" @click="showPasswordPrompt('photo')">
  <!-- Si tiene foto → muestra la imagen, si no → muestra las iniciales -->
  <img 
    v-if="user.photoUrl" 
    :src="user.photoUrl" 
    alt="Imagen de Perfil" 
    class="user-photo"
  >
  
  <!-- Avatar por defecto con iniciales si no hay foto -->
  <div v-else class="default-avatar">
    {{ userInitials }}
  </div>

  <div class="photo-overlay">
    <span class="photo-overlay-text">Actualizar Imagen</span>
  </div>
</div>

        <div class="info-list">
          <div v-for="(field, key) in editableFields" :key="key" class="info-item">
            <div class="info-details">
              <span class="info-label">{{ field.label }}</span>
              <span class="info-value">{{ user[key] }}</span>
            </div>
            <button @click="showPasswordPrompt(key)" class="edit-button">
              Editar
            </button>
          </div>
        </div>
      </div>

      <button @click="showPasswordPrompt('password')" class="update-password-button">
        Actualizar Contraseña
      </button>

      <input type="file" ref="fileInput" @change="handleFileChange" style="display: none" accept="image/*">

      <div v-if="passwordPrompt.visible" class="modal-overlay">
        <div class="modal-content">
          <h3 class="modal-title">Verificar Contraseña</h3>
          <p class="modal-text">
            Introduce tu contraseña actual para continuar.
          </p>
          <div class="password-input-container">
            <input v-model="passwordPrompt.input" :type="passwordPrompt.show ? 'text' : 'password'"
              @keyup.enter="handlePasswordCheck" class="modal-input" placeholder="Contraseña actual" />
            <button @click="togglePasswordVisibility(passwordPrompt)" class="password-toggle-button">
              <svg v-if="passwordPrompt.show" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                class="password-icon">
                <path d="M12 15a3 3 0 100-6 3 3 0 000 6z" />
                <path fill-rule="evenodd"
                  d="M1.323 11.447C2.81 1.884 10.338 0 12 0c1.662 0 9.19 1.884 10.677 11.447a1.992 1.992 0 010 1.106C21.19 22.116 13.662 24 12 24c-1.662 0-9.19-1.884-10.677-11.447a1.992 1.992 0 010-1.106zm8.995 2.11C11.531 16.51 15 13.665 15 12c0-1.665-3.469-4.51-4.682-2.111A2.5 2.5 0 0112 8c1.38 0 2.5 1.12 2.5 2.5S13.38 13 12 13s-2.5-1.12-2.5-2.5a2.5 2.5 0 011.785-2.389z"
                  clip-rule="evenodd" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                class="password-icon">
                <path d="M12 4.5c-5 0-9.28 2.36-11.23 5.56a1 1 0 000 .88C2.72 17.14 7 19.5 12 19.5s9.28-2.36 11.23-5.56a1 1 0 000-.88C21.28 6.86 17 4.5 12 4.5zm0 13a4.5 4.5 0 110-9 4.5 4.5 0 010 9z" />
                <path d="M12 15.5a3.5 3.5 0 100-7 3.5 3.5 0 000 7z" />
              </svg>
            </button>
          </div>
          <div class="modal-buttons">
            <button @click="handlePasswordCheck" class="modal-confirm-button">
              Confirmar
            </button>
            <button @click="cancelPasswordPrompt" class="modal-cancel-button">
              Cancelar
            </button>
          </div>
        </div>
      </div>

      <div v-if="editFieldPrompt.visible" class="modal-overlay">
        <div class="modal-content">
          <h3 class="modal-title">Actualizar {{ editFieldPrompt.label }}</h3>
          <p class="modal-text">
            Introduce el nuevo {{ editFieldPrompt.label.toLowerCase() }}.
          </p>
          <div class="password-input-container">
            <input v-model="editFieldPrompt.value" :type="editFieldPrompt.type"
              :placeholder="`Nuevo ${editFieldPrompt.label.toLowerCase()}`" class="modal-input" />
          </div>
          <div class="modal-buttons">
            <button @click="updateData(editFieldPrompt.key)" class="modal-confirm-button">
              Guardar
            </button>
            <button @click="cancelEditField" class="modal-cancel-button">
              Cancelar
            </button>
          </div>
        </div>
      </div>

      <div v-if="passwordUpdatePrompt.visible" class="modal-overlay">
        <div class="modal-content">
          <h3 class="modal-title">Actualizar Contraseña</h3>
          <p class="modal-text">
            Introduce y confirma tu nueva contraseña.
          </p>
          <div class="password-input-container">
            <input v-model="passwordUpdatePrompt.newPassword" :type="passwordUpdatePrompt.showNew ? 'text' : 'password'"
              class="modal-input" placeholder="Nueva contraseña" />
            <button @click="togglePasswordVisibility(passwordUpdatePrompt, 'showNew')" class="password-toggle-button">
              <svg v-if="passwordUpdatePrompt.showNew" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                fill="currentColor" class="password-icon">
                <path d="M12 15a3 3 0 100-6 3 3 0 000 6z" />
                <path fill-rule="evenodd"
                  d="M1.323 11.447C2.81 1.884 10.338 0 12 0c1.662 0 9.19 1.884 10.677 11.447a1.992 1.992 0 010 1.106C21.19 22.116 13.662 24 12 24c-1.662 0-9.19-1.884-10.677-11.447a1.992 1.992 0 010-1.106zm8.995 2.11C11.531 16.51 15 13.665 15 12c0-1.665-3.469-4.51-4.682-2.111A2.5 2.5 0 0112 8c1.38 0 2.5 1.12 2.5 2.5S13.38 13 12 13s-2.5-1.12-2.5-2.5a2.5 2.5 0 011.785-2.389z"
                  clip-rule="evenodd" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                class="password-icon">
                <path d="M12 4.5c-5 0-9.28 2.36-11.23 5.56a1 1 0 000 .88C2.72 17.14 7 19.5 12 19.5s9.28-2.36 11.23-5.56a1 1 0 000-.88C21.28 6.86 17 4.5 12 4.5zm0 13a4.5 4.5 0 110-9 4.5 4.5 0 010 9z" />
                <path d="M12 15.5a3.5 3.5 0 100-7 3.5 3.5 0 000 7z" />
              </svg>
            </button>
          </div>
          <div class="password-input-container">
            <input v-model="passwordUpdatePrompt.confirmPassword"
              :type="passwordUpdatePrompt.showConfirm ? 'text' : 'password'" class="modal-input"
              placeholder="Confirmar nueva contraseña" />
            <button @click="togglePasswordVisibility(passwordUpdatePrompt, 'showConfirm')"
              class="password-toggle-button">
              <svg v-if="passwordUpdatePrompt.showConfirm" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"
                fill="currentColor" class="password-icon">
                <path d="M12 15a3 3 0 100-6 3 3 0 000 6z" />
                <path fill-rule="evenodd"
                  d="M1.323 11.447C2.81 1.884 10.338 0 12 0c1.662 0 9.19 1.884 10.677 11.447a1.992 1.992 0 010 1.106C21.19 22.116 13.662 24 12 24c-1.662 0-9.19-1.884-10.677-11.447a1.992 1.992 0 010-1.106zm8.995 2.11C11.531 16.51 15 13.665 15 12c0-1.665-3.469-4.51-4.682-2.111A2.5 2.5 0 0112 8c1.38 0 2.5 1.12 2.5 2.5S13.38 13 12 13s-2.5-1.12-2.5-2.5a2.5 2.5 0 011.785-2.389z"
                  clip-rule="evenodd" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                class="password-icon">
                <path d="M12 4.5c-5 0-9.28 2.36-11.23 5.56a1 1 0 000 .88C2.72 17.14 7 19.5 12 19.5s9.28-2.36 11.23-5.56a1 1 0 000-.88C21.28 6.86 17 4.5 12 4.5zm0 13a4.5 4.5 0 110-9 4.5 4.5 0 010 9z" />
                <path d="M12 15.5a3.5 3.5 0 100-7 3.5 3.5 0 000 7z" />
              </svg>
            </button>
          </div>
          <div class="modal-buttons">
            <button @click="updatePassword" class="modal-confirm-button">
              Guardar
            </button>
            <button @click="cancelPasswordUpdate" class="modal-cancel-button">
              Cancelar
            </button>
          </div>
        </div>
      </div>

      <div v-if="messageBox.visible" class="modal-overlay">
        <div class="modal-content-message">
          <h3 class="modal-title">Notificación</h3>
          <p class="modal-text">{{ messageBox.text }}</p>
          <button @click="closeMessageBox" class="modal-confirm-button">
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useUserStore } from '@/stores/user';
// SweetAlert2 CDN import
import Swal from 'https://cdn.jsdelivr.net/npm/sweetalert2@11.12.2/src/sweetalert2.js';

const userStore = useUserStore();

const user = computed(() => ({
  name: userStore.nombre,
  phone: userStore.telefono,
  email: userStore.correo,
  photoUrl: userStore.imagen,
}));
const userInitials = computed(() => {
  const name = user.value.name || 'Usuario';
  const names = name.trim().split(' ');
  if (names.length === 1) {
    return names[0].charAt(0).toUpperCase();
  }
  return (names[0].charAt(0) + (names[names.length - 1].charAt(0) || '')).toUpperCase();
});
const editableFields = reactive({
  name: { label: 'Nombre', type: 'text' },
  phone: { label: 'Teléfono', type: 'tel' },
  email: { label: 'Correo', type: 'email' },
});

const passwordPrompt = reactive({
  visible: false,
  input: '',
  target: '',
  show: false,
});

const editFieldPrompt = reactive({
  visible: false,
  key: '',
  label: '',
  value: '',
  type: 'text'
});

const passwordUpdatePrompt = reactive({
  visible: false,
  newPassword: '',
  confirmPassword: '',
  showNew: false,
  showConfirm: false,
});

const messageBox = reactive({
  visible: false,
  text: '',
});

const fileInput = ref(null);

const goBack = () => {
  window.history.back();
};

const showPasswordPrompt = (targetField) => {
  passwordPrompt.input = '';
  passwordPrompt.visible = true;
  passwordPrompt.target = targetField;
  passwordPrompt.show = false;
};

const togglePasswordVisibility = (prompt, key = 'show') => {
  prompt[key] = !prompt[key];
};

const showMessageBox = (text) => {
  messageBox.text = text;
  messageBox.visible = true;
};

const closeMessageBox = () => {
  messageBox.visible = false;
  messageBox.text = '';
};

// Helper para mostrar un SweetAlert2 normal
const showSwalAlert = (title, text, icon) => {
  Swal.fire({
    title,
    text,
    icon,
    confirmButtonText: 'Ok',
    customClass: {
      popup: 'swal2-popup-custom',
      title: 'swal2-title-custom',
      content: 'swal2-text-custom',
      confirmButton: 'swal2-confirm-button-custom',
    },
    background: '#0f172a',
    color: '#fff'
  });
};

// Helper para mostrar un toast de SweetAlert2
const showToast = (icon, title) => {
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
      toast.addEventListener('mouseenter', Swal.stopTimer);
      toast.addEventListener('mouseleave', Swal.resumeTimer);
    }
  });

  Toast.fire({
    icon: icon,
    title: title
  });
};

const handlePasswordCheck = async () => {
  const verificationResult = await userStore.verifyPassword(passwordPrompt.input);

  if (verificationResult.success) {
    showToast('success', 'Contraseña verificada correctamente');
    passwordPrompt.visible = false;

    if (passwordPrompt.target === 'password') {
      passwordUpdatePrompt.visible = true;
      passwordUpdatePrompt.newPassword = '';
      passwordUpdatePrompt.confirmPassword = '';
      passwordUpdatePrompt.showNew = false;
      passwordUpdatePrompt.showConfirm = false;
    } else if (passwordPrompt.target === 'photo') {
      fileInput.value.click();
    } else {
      const key = passwordPrompt.target;
      editFieldPrompt.key = key;
      editFieldPrompt.label = editableFields[key].label;
      editFieldPrompt.value = user.value[key];
      editFieldPrompt.type = editableFields[key].type;
      editFieldPrompt.visible = true;
    }
  } else {
    showToast('error', verificationResult.message);
  }
};

const updateData = async (key) => {
  const updatedData = {
    nombre: key === 'name' ? editFieldPrompt.value : user.value.name,
    telefono: key === 'phone' ? editFieldPrompt.value : user.value.phone,
    correo: key === 'email' ? editFieldPrompt.value : user.value.email,
  };

  const result = await userStore.updateUserData(updatedData);

  if (result.success) {
    showSwalAlert('¡Actualizado!', `El campo ${editableFields[key].label} ha sido actualizado.`, 'success');
    editFieldPrompt.visible = false;
  } else {
    showSwalAlert('Error', result.message, 'error');
  }
};

const updatePassword = async () => {
  if (passwordUpdatePrompt.newPassword && passwordUpdatePrompt.newPassword === passwordUpdatePrompt.confirmPassword) {
    const passwordData = {
      current_password: passwordPrompt.input,
      new_password: passwordUpdatePrompt.newPassword
    };

    const result = await userStore.updateUserPassword(passwordData);

    if (result.success) {
      showSwalAlert('¡Actualizado!', 'La contraseña ha sido actualizada con éxito.', 'success');
      passwordUpdatePrompt.visible = false;
    } else {
      showSwalAlert('Error', result.message, 'error');
    }
  } else {
    showMessageBox('Las contraseñas no coinciden. Inténtalo de nuevo.');
  }
};

const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = async (e) => {
      const photoUrl = e.target.result;
      const result = await userStore.updateUserPhoto(photoUrl);

      if (result.success) {
        showSwalAlert('¡Actualizado!', 'La imagen de perfil ha sido actualizada con éxito.', 'success');
      } else {
        showSwalAlert('Error', result.message, 'error');
      }
    };
    reader.readAsDataURL(file);
  }
};

const cancelPasswordPrompt = () => {
  passwordPrompt.visible = false;
  passwordPrompt.input = '';
};

const cancelEditField = () => {
  editFieldPrompt.visible = false;
};

const cancelPasswordUpdate = () => {
  passwordUpdatePrompt.visible = false;
};
</script>
<style scoped>
/* General styles for the page */
.settings-page {
  background-color: #000;
  color: #fff;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  box-sizing: border-box; /* Ensures padding is included in the element's total width and height */
}

.settings-container {
  max-width: 42rem; /* 672px */
  width: 100%;
  background-color: #0f172a;
  border-radius: 1.5rem; /* 24px */
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  padding: 1.5rem; /* Reduced padding for mobile */
  border: 1px solid #ec4899;
  display: flex;
  flex-direction: column;
  gap: 1.5rem; /* Reduced gap for mobile */
}

@media (min-width: 768px) {
  .settings-container {
    padding: 2rem;
    gap: 2rem;
  }
}

/* Back button */
.back-button-container {
  display: flex;
  align-items: center;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #fff;
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
  border-radius: 9999px; /* full circle */
  padding: 0.5rem 1rem;
  transition: all 0.3s ease-in-out;
  text-decoration: none;
  font-weight: 600;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.back-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 10px -2px rgba(0, 0, 0, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
}

.back-button:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 3px;
}

.back-icon {
  height: 1.25rem; /* 20px */
  width: 1.25rem; /* 20px */
}

/* Profile section */
.profile-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.user-photo-container {
  position: relative;
  width: 8rem; /* 128px for mobile */
  height: 8rem;
  cursor: pointer;
  transition: transform 0.3s ease-in-out;
}

@media (min-width: 768px) {
  .user-photo-container {
    width: 10rem;
    height: 10rem;
  }
}

.user-photo-container:hover {
  transform: scale(1.05);
}

.user-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 9999px; /* full circle */
  border: 4px solid #ec4899;
  transition-property: border-color;
  transition-duration: 300ms;
}

.user-photo-container:hover .user-photo {
  border-color: #3b82f6;
}

.photo-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition-property: opacity;
  transition-duration: 300ms;
}

.user-photo-container:hover .photo-overlay {
  opacity: 1;
}

.photo-overlay-text {
  color: #fff;
  font-size: 0.75rem; /* 12px for mobile */
  font-weight: 600;
  text-align: center;
  padding: 0 0.5rem;
}

@media (min-width: 768px) {
  .photo-overlay-text {
    font-size: 0.875rem;
  }
}

/* User info list */
.info-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1rem;
  background-color: #1e293b;
  border-radius: 0.75rem; /* 12px */
}

@media (min-width: 768px) {
  .info-item {
    flex-direction: row;
    align-items: center;
    gap: 1rem;
  }
}

.info-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex-grow: 1;
}

.info-label {
  font-size: 0.75rem;
  color: #94a3b8;
}

.info-value {
  font-size: 1rem;
  font-weight: 600;
  word-break: break-word; /* Prevents overflow on small screens */
}

@media (min-width: 768px) {
  .info-label {
    font-size: 0.875rem;
  }
  .info-value {
    font-size: 1.125rem;
  }
}

.edit-button {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #3b82f6;
  color: #fff;
  font-weight: bold;
  border-radius: 0.5rem;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1-px rgba(0, 0, 0, 0.06);
  border: none;
  cursor: pointer;
  white-space: nowrap; /* Prevents text from wrapping on small buttons */
}

.edit-button:hover {
  background-color: #60a5fa; /* Lighter blue */
  transform: scale(1.05);
}

.edit-button:focus {
  outline: none;
}

@media (min-width: 768px) {
  .edit-button {
    margin-top: 0;
  }
}

/* Update password button */
.update-password-button {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background-color: #ec4899;
  color: #fff;
  font-weight: 800; /* extrabold */
  border-radius: 0.75rem;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  border: none;
  cursor: pointer;
}

.update-password-button:hover {
  background-color: #ec4899; /* Lighter pink */
  transform: scale(1.05);
}

.update-password-button:focus {
  outline: none;
}

/* Modals */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  z-index: 50;
  box-sizing: border-box;
}

.modal-content, .modal-content-message {
  background-color: #0f172a;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  max-width: 24rem; /* 384px */
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  border: 1px solid #3b82f6;
  text-align: center;
  box-sizing: border-box;
}

.modal-content-message {
  border: 1px solid #ec4899;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
  text-align: center;
}

.modal-text {
  font-size: 0.875rem;
  color: #94a3b8;
  text-align: center;
}

.password-input-container {
  position: relative;
  width: 100%;
}

.modal-input {
  width: 100%;
  background-color: #334155;
  color: #fff;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  transition: all 0.3s;
  padding-right: 3rem; /* Make space for the eye icon */
  box-sizing: border-box;
}

.modal-input:focus {
  outline: none;
  box-shadow: 0 0 0 2px #ec4899;
}

.password-toggle-button {
  position: absolute;
  top: 50%;
  right: 0.75rem;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0.25rem;
  transition: color 0.3s;
}

.password-toggle-button:hover {
  color: #fff;
}

.password-icon {
  width: 1.25rem; /* 20px */
  height: 1.25rem;
}

.modal-buttons {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

@media (min-width: 480px) {
  .modal-buttons {
    flex-direction: row;
  }
}

.modal-confirm-button, .modal-cancel-button {
  flex: 1;
  padding: 0.75rem 1rem;
  font-weight: bold;
  border-radius: 0.5rem;
  transition: all 0.3s ease-in-out;
  border: none;
  cursor: pointer;
}

.modal-confirm-button {
  background-color: #3b82f6;
  color: #fff;
}

.modal-confirm-button:hover {
  background-color: #60a5fa;
  transform: scale(1.05);
}

.modal-cancel-button {
  background-color: #334155;
  color: #d1d5db; /* A lighter gray for text */
}

.modal-cancel-button:hover {
  background-color: #4b5563; /* Lighter gray */
}

/* SweetAlert2 Custom Styles */
.swal2-popup-custom {
  background-color: #0f172a !important;
  border: 1px solid #3b82f6 !important;
  border-radius: 1rem !important;
}

.swal2-title-custom {
  color: #fff !important;
}

.swal2-text-custom {
  color: #94a3b8 !important;
}

.swal2-confirm-button-custom {
  background-color: #3b82f6 !important;
  color: #fff !important;
  border-radius: 0.5rem !important;
  font-weight: bold !important;
}

.swal2-confirm-button-custom:hover {
  background-color: #60a5fa !important;
}
.default-avatar {
  width: 100%;
  height: 100%;
  border-radius: 9999px;
  background: linear-gradient(135deg, #ec4899, #3b82f6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem; /* Ajusta según el tamaño del círculo */
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
  border: 4px solid #ec4899;
  transition: border-color 300ms;
}

@media (min-width: 768px) {
  .default-avatar {
    font-size: 3rem;
  }
}

.user-photo-container:hover .default-avatar {
  border-color: #3b82f6;
}
</style>
