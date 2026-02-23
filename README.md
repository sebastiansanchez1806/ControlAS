# 🍸 ControlAS Bar - Sistema Integral de Gestión para Bares

¡Proyecto en producción! Actualmente, **ControlAS Bar** optimiza la operación diaria de **6 establecimientos**, brindando control total sobre inventarios, personal y facturación.

## 🚀 Vista General del Proyecto
Este sistema fue diseñado para resolver la complejidad administrativa de los establecimientos nocturnos. Ofrece una interfaz intuitiva respaldada por una arquitectura robusta y escalable.

### ✨ Funcionalidades Clave
* **Seguridad y Acceso:** Login moderno con flujo completo de recuperación de contraseña.
* **Gestión Jerárquica:** Paneles administrativos para Gestor Principal, Dueños y Administradores.
* **Control de Personal:** Sistema de alertas para exámenes de salud y gestión de tareas.
* **Inventario Digital:** Gestión de productos y stock con soporte para carga de documentos PDF.
* **Finanzas Automatizadas:** Facturación diaria, control de gastos y resúmenes mensuales automáticos vía email.
* **Mantenimiento:** Backups automáticos y limpieza programada de historial.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
| :--- | :--- |
| **Frontend** | Vue 3 (Composition API), Vite, Tailwind CSS, SweetAlert2 |
| **Backend** | FastAPI (Python 3.12) + Uvicorn |
| **Base de Datos** | MySQL |
| **Servidor** | Nginx (Proxy Reverso) sobre Ubuntu LTS |
| **Seguridad** | SSL Let's Encrypt + Cloudflare Proxy |

---

## 📁 Estructura del Proyecto

```plaintext
ControlAS/
├── bar_backend/          # API REST con FastAPI (Modelos, Vistas y Schemas)
└── frond/                # Interfaz de usuario en Vue 3 + Stores (Pinia)


🔧 Flujo de Trabajo (CI/CD)
El proyecto cuenta con un flujo de despliegue continuo optimizado:

Desarrollo: Actualización de código en el repositorio central.

Despliegue: Script automatizado en el servidor para ejecución de git pull y build del frontend.

Distribución: Purga de caché en Cloudflare para asegurar la disponibilidad inmediata de los cambios.

📊 Estado Actual
Frontend: Interfaz moderna, animada y 100% responsive.

Backend: Procesamiento estable de endpoints y envío de correos.

Producción: Operando con certificados de seguridad activos y alto rendimiento.

👤 Autor
Diego Sánchez Desarrollador enfocado en soluciones tecnológicas para la gestión operativa.
