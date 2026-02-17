import { defineStore } from 'pinia';
import { piniaPersistCookie } from '@/src/plugins/pinia-persist-cookie';

export const useAdminStore = defineStore('admin', {
  state: () => ({
    id: null,
    nombre: '',
    telefono: '',
    foto: null,
    bar_id: null,
    dueno_id: null,
    bar_nombre: '',

    // Inicializamos en false (pero se sobreescribirán con lo real del backend)
    permiso_ver_productos: false,
    permiso_agregar_inventario: false,
    permiso_generar_facturas: false,
    permiso_agregar_personal_femenino: false,
  }),

  actions: {
    setAdmin(data) {
      console.log('📥 Datos CRUDOS que llegan del backend en setAdmin:', JSON.stringify(data, null, 2));

      this.id = data.id;
      this.nombre = data.nombre || '';
      this.telefono = data.telefono || '';
      this.foto = data.foto || null;
      this.bar_id = data.bar_id || null;
      this.dueno_id = data.dueno_id || null;
      this.bar_nombre = data.bar_nombre || '';

      // ── CORRECCIÓN: leer desde el objeto "permisos" que envía el backend ──
      if (data.permisos && typeof data.permisos === 'object') {
        this.permiso_ver_productos = data.permisos.ver_productos ?? false;
        this.permiso_agregar_inventario = data.permisos.agregar_inventario ?? false;
        this.permiso_generar_facturas = data.permisos.generar_facturas ?? false;
        this.permiso_agregar_personal_femenino = data.permisos.agregar_personal_femenino ?? false;
      } else {
        console.warn('⚠️ No se encontró el objeto "permisos" en la respuesta. Usando defaults false.');
      }

      // Log final con los valores reales que se guardaron
      console.log('✅ Store actualizado con permisos:', {
        permiso_ver_productos: this.permiso_ver_productos,
        permiso_agregar_inventario: this.permiso_agregar_inventario,
        permiso_generar_facturas: this.permiso_generar_facturas,
        permiso_agregar_personal_femenino: this.permiso_agregar_personal_femenino
      });
    },

    logout() {
      console.log('🔒 Logout ejecutado → reseteando store y permisos');
      this.id = null;
      this.nombre = '';
      this.telefono = '';
      this.foto = null;
      this.bar_id = null;
      this.dueno_id = null;
      this.bar_nombre = '';

      this.permiso_ver_productos = false;
      this.permiso_agregar_inventario = false;
      this.permiso_generar_facturas = false;
      this.permiso_agregar_personal_femenino = false;
    }
  },

  persist: {
    key: 'admin_pinia',
    storage: piniaPersistCookie.storage,
  },
});